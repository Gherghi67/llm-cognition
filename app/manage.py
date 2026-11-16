#!/usr/bin/env python3
"""Host-side service maintenance and daily SQLite backups. No host mounts needed."""

import argparse
from contextlib import closing
from datetime import datetime, timezone
import fcntl
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
BACKUPS = ROOT / "data" / "backups"
DOCKER = shutil.which("docker") or "/usr/local/bin/docker"
PROJECT = "layer-atlas"


def network_env(project=PROJECT):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", project):
        raise ValueError("Invalid Compose project name")
    return ROOT / "data" / "networks" / f"{project}.env"


def compose_command(project=PROJECT):
    return [DOCKER, "compose", "--env-file", str(network_env(project)),
            "-p", project, "-f", str(ROOT / "compose.yaml")]


COMPOSE = compose_command()


def backend_address(network, project, previous=None):
    labels = network.get("Labels") or {}
    if (not network.get("Internal") or network.get("Driver") != "bridge"
            or labels.get("com.docker.compose.project") != project
            or labels.get("com.docker.compose.network") != "isolated"):
        raise RuntimeError("Refusing a network that is not this project's internal bridge")
    subnets = [ipaddress.ip_network(entry["Subnet"]) for entry in network["IPAM"]["Config"]]
    ipv4 = [subnet for subnet in subnets if subnet.version == 4]
    if len(ipv4) != 1 or ipv4[0].prefixlen > 30:
        raise RuntimeError("Expected one usable private backend IPv4 subnet")
    subnet = ipv4[0]
    occupied = {}
    for peer in (network.get("Containers") or {}).values():
        if peer.get("IPv4Address"):
            occupied[ipaddress.ip_interface(peer["IPv4Address"]).ip] = peer["Name"]
    gateways = {ipaddress.ip_address(entry["Gateway"]) for entry in network["IPAM"]["Config"]
                if entry.get("Gateway")}
    atlas = [address for address, name in occupied.items() if name == f"{project}-atlas-1"]
    if atlas:
        address = atlas[0]
    elif previous and previous.get("LAYER_ATLAS_NETWORK_ID") == network["Id"]:
        address = ipaddress.IPv4Address(previous["LAYER_ATLAS_BACKEND_IPV4"])
    else:
        address = next((item for item in subnet.hosts() if item not in gateways and item not in occupied), None)
    if (address is None or address not in subnet or address in gateways
            or address in {subnet.network_address, subnet.broadcast_address}
            or (address in occupied and occupied[address] != f"{project}-atlas-1")):
        raise RuntimeError("Reserved backend address is invalid or belongs to another container")
    return str(address)


def prepare_network(project=PROJECT):
    destination = network_env(project)
    name = f"{project}_isolated"
    existing = subprocess.check_output(
        [DOCKER, "network", "ls", "--filter", f"name=^{name}$", "-q"], text=True, timeout=20).strip()
    if not existing:
        subprocess.run([DOCKER, "network", "create", "--internal",
                        "--label", f"com.docker.compose.project={project}",
                        "--label", "com.docker.compose.network=isolated", name],
                       check=True, capture_output=True, timeout=30)
    network = json.loads(subprocess.check_output([DOCKER, "network", "inspect", name], timeout=20))[0]
    previous = dict(line.split("=", 1) for line in destination.read_text().splitlines()) if destination.exists() else None
    address = backend_address(network, project, previous)
    content = (f"LAYER_ATLAS_NETWORK_NAME={name}\nLAYER_ATLAS_NETWORK_ID={network['Id']}\n"
               f"LAYER_ATLAS_BACKEND_IPV4={address}\n")
    if destination.exists() and destination.read_text() == content:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(prefix=".network-", dir=destination.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return destination

SNAPSHOT = """
from contextlib import closing
import os, sqlite3, sys, tempfile
fd, name = tempfile.mkstemp(prefix='.snapshot-', suffix='.sqlite3', dir='/data')
os.close(fd)
try:
    with closing(sqlite3.connect('file:/data/layer-atlas.sqlite3?mode=ro', uri=True)) as source:
        with closing(sqlite3.connect(name)) as target:
            source.backup(target)
    with open(name, 'rb') as snapshot:
        while block := snapshot.read(1024 * 1024):
            sys.stdout.buffer.write(block)
finally:
    os.unlink(name)
"""


def verify_backup(path):
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise RuntimeError("SQLite integrity check failed")
        db.execute("SELECT id, payload, revision FROM runs LIMIT 1").fetchall()
        db.execute("SELECT id, done FROM tasks LIMIT 1").fetchall()


def backup(force=False):
    BACKUPS.mkdir(parents=True, exist_ok=True, mode=0o700)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    destination = BACKUPS / f"layer-atlas-{today}.sqlite3"
    if destination.exists() and not force:
        verify_backup(destination)
        return
    fd, temporary = tempfile.mkstemp(prefix=".backup-", suffix=".sqlite3", dir=BACKUPS)
    temporary = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as output:
            subprocess.run(COMPOSE + ["exec", "-T", "atlas", "python", "-c", SNAPSHOT],
                           stdout=output, check=True, timeout=180)
            output.flush()
            os.fsync(output.fileno())
        verify_backup(temporary)
        os.replace(temporary, destination)
        for old in sorted(BACKUPS.glob("layer-atlas-????-??-??.sqlite3"), reverse=True)[30:]:
            old.unlink()
        print(f"Verified backup: {destination}", flush=True)
    finally:
        temporary.unlink(missing_ok=True)


def docker_ready():
    ready = subprocess.run([DOCKER, "info", "--format", "{{.ServerVersion}}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
    if ready.returncode:
        subprocess.run([DOCKER, "desktop", "start", "--timeout", "60"], check=True, timeout=75)


def maintain(build=False):
    docker_ready()
    prepare_network()
    if build:
        running = subprocess.check_output(COMPOSE + ["ps", "--status", "running", "-q", "atlas"],
                                          text=True, timeout=20).strip()
        if running:
            backup(force=True)
        subprocess.run(COMPOSE + ["build"], check=True, timeout=300)
    result = subprocess.run(COMPOSE + ["up", "-d", "--no-build", "--wait", "--wait-timeout", "45"],
                            capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError(result.stderr)
    backup()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["maintain", "backup", "prepare", "deploy"])
    parser.add_argument("--project", default=PROJECT, help="Project for prepare; other actions use the live project")
    args = parser.parse_args()
    if args.project != PROJECT and args.action != "prepare":
        parser.error("Only prepare accepts a different project")
    network_env(args.project)
    os.umask(0o077)
    (ROOT / "data").mkdir(exist_ok=True)
    lock_name = "maintenance.lock" if args.project == PROJECT else f"{args.project}.maintenance.lock"
    with (ROOT / "data" / lock_name).open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            if args.action == "maintain":
                return
            parser.exit(1, "Another Layer Atlas operation holds the maintenance lock; try again when it finishes.\n")
        if args.action in {"maintain", "deploy"}:
            maintain(build=args.action == "deploy")
            if args.action == "deploy":
                print("Layer Atlas deployment is healthy")
        elif args.action == "prepare":
            docker_ready()
            print(f"Prepared network settings: {prepare_network(args.project)}")
        else:
            prepare_network()
            backup(force=True)


if __name__ == "__main__":
    main()
