#!/usr/bin/env python3
"""Disposable gateway firewall experiment. Never operates on the live project."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import ipaddress
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
spec = importlib.util.spec_from_file_location("manage", APP / "manage.py")
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)
STATE = APP.parent / ".cs/local/gateway-egress-verify"
PROJECT = "layer-atlas-egress-verify"
PORT = 18786
PORTS = [9222, 3306, 6379, 8765, 63342]
DOCKER = shutil.which("docker") or "/usr/local/bin/docker"
COMPOSE = [DOCKER, "compose", "-p", PROJECT, "-f", str(STATE / "protected.json")]
DROP = ["/usr/local/bin/unprivileged.sh"]


def run(*args, check=True, timeout=90, **kwargs):
    return subprocess.run(list(args), check=check, timeout=timeout, text=True,
                          capture_output=True, **kwargs)


def docker(*args, **kwargs):
    return run(DOCKER, *args, **kwargs).stdout.strip()


def compose(*args, variant="protected", **kwargs):
    command = [*COMPOSE]
    command[-1] = str(STATE / f"{variant}.json")
    result = run(*command, *args, **kwargs)
    if result.stdout:
        print(result.stdout, flush=True)
    if result.stderr:
        print(result.stderr, flush=True)
    return result


def inspect(identifier):
    return json.loads(docker("inspect", identifier))[0]


def container(service="gateway"):
    identifier = run(*COMPOSE, "ps", "-a", "-q", service).stdout.strip()
    assert identifier and "\n" not in identifier
    details = inspect(identifier)
    assert details["Config"]["Labels"]["com.docker.compose.project"] == PROJECT
    return identifier


def execute(*args, unprivileged=False, **kwargs):
    prefix = DROP if unprivileged else []
    return run(DOCKER, "exec", container(), *prefix, *args, **kwargs)


def save(name, value):
    (STATE / name).write_text(json.dumps(value, indent=2) + "\n")


def live_snapshot():
    result = {}
    for service in ["atlas", "gateway"]:
        d = inspect(f"layer-atlas-{service}-1")
        result[service] = {"id": d["Id"], "image": d["Image"],
                           "started": d["State"]["StartedAt"]}
    return result


def prepare():
    for project in [PROJECT, "layer-atlas-verify"]:
        existing = docker("ps", "-aq", "--filter", f"label=com.docker.compose.project={project}")
        if existing:
            raise RuntimeError(f"Inspect/reuse the existing {project} stack first: {existing}")
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", PORT))
    STATE.mkdir(parents=True, exist_ok=True)
    save("live-before.json", live_snapshot())
    context = STATE / "build"
    context.mkdir(exist_ok=True)
    for name in ["Dockerfile", "start.sh", "unprivileged.sh", "verify-unprivileged.sh"]:
        shutil.copyfile(APP / "gateway" / name, context / name)
    shutil.copyfile(APP / "gateway/nginx.conf", context / "nginx.conf")
    network_name = PROJECT + "_isolated"
    env_file = manage.prepare_network(PROJECT)
    previous_mtime = env_file.stat().st_mtime_ns
    manage.prepare_network(PROJECT)
    assert env_file.stat().st_mtime_ns == previous_mtime
    config = json.loads(run(*manage.compose_command(PROJECT), "config", "--format", "json").stdout)
    config["name"] = PROJECT
    config["volumes"] = {"results": {"name": PROJECT + "_results"}}
    config["networks"] = {
        "isolated": {"external": True, "name": network_name},
        "ingress": {"name": PROJECT + "_ingress", "enable_ipv6": True},
    }
    for name, service in config["services"].items():
        service["image"] = f"{PROJECT}-{name}:local"
        service["restart"] = "no"
        service["healthcheck"]["interval"] = "3s"
    gateway = config["services"]["gateway"]
    gateway.update({
        "build": {"context": str(context)},
        "ports": [{"target": 8786, "published": str(PORT), "host_ip": "127.0.0.1", "protocol": "tcp"}],
    })
    save("protected.json", config)
    baseline = deepcopy(config)
    g = baseline["services"]["gateway"]
    g.update({"user": "101:101", "init": True, "cap_add": [], "entrypoint": ["nginx", "-g", "daemon off;"]})
    g["healthcheck"]["test"] = ["CMD", "wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8786/api/health"]
    save("baseline.json", baseline)
    for name, change in [
        ("no-net-admin", {"cap_add": ["SETUID", "SETGID", "SETPCAP"]}),
        ("no-setpcap", {"cap_add": ["NET_ADMIN", "SETUID", "SETGID"]}),
        ("missing-address", {"environment": {}}),
        ("invalid-address", {"environment": {"ATLAS_IPV4": "999.999.999.999"}}),
    ]:
        invalid = deepcopy(config)
        invalid["services"]["gateway"].update(change)
        save(name + ".json", invalid)
    print("Prepared isolated Compose files; backend address reserved from Docker IPAM", flush=True)


def fixture():
    script = """
import socket, threading, time
def listen(family, address):
    s = socket.socket(family)
    if family == socket.AF_INET6:
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
    s.bind((address, 9222)); s.listen()
    def accept():
        while True:
            c, _ = s.accept(); c.close()
    threading.Thread(target=accept, daemon=True).start()
listen(socket.AF_INET, '0.0.0.0')
listen(socket.AF_INET6, '::')
print('ready', flush=True)
while True: time.sleep(60)
"""
    identifier = docker("run", "-d", "--name", PROJECT + "-probe", "--label",
                        f"com.docker.compose.project={PROJECT}", "--network", PROJECT + "_ingress",
                        "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges:true",
                        "--user=10001:10001", "--memory=64m", "--pids-limit=16", "--cpus=0.1",
                        "--entrypoint=python", PROJECT + "-atlas:local", "-u", "-c", script)
    for _ in range(30):
        if "ready" in docker("logs", identifier):
            return
        time.sleep(0.1)
    raise RuntimeError("IPv4/IPv6 probe fixture did not start")


def targets():
    result = [("host-name", "host.docker.internal", p) for p in PORTS]
    result += [("host-gateway-name", "gateway.docker.internal", p) for p in PORTS]
    raw = execute("nslookup", "host.docker.internal").stdout
    addresses = set()
    for word in raw.split():
        try:
            address = ipaddress.ip_address(word)
        except ValueError:
            continue
        if not address.is_loopback:
            addresses.add(str(address))
    for address in sorted(addresses):
        result += [("host-numeric", address, p) for p in PORTS]
        if ipaddress.ip_address(address).version == 4:
            result += [("host-mapped-ipv6", "::ffff:" + address, p) for p in PORTS]
    assert addresses, raw
    for name, network in inspect(container())["NetworkSettings"]["Networks"].items():
        for key in ["Gateway", "IPv6Gateway"]:
            if network[key]:
                result += [(name.rsplit("_", 1)[-1] + "-" + key, network[key], p) for p in PORTS]
    if Path("/usr/sbin/ipconfig").exists():
        lan = run("/usr/sbin/ipconfig", "getifaddr", "en0", check=False).stdout.strip()
        if lan:
            ipaddress.ip_address(lan)
            result += [("mac-lan", lan, p) for p in PORTS]
    tailscale = shutil.which("tailscale")
    if tailscale:
        status = run(tailscale, "status", "--json", check=False)
        if status.returncode == 0:
            for address in json.loads(status.stdout)["Self"]["TailscaleIPs"]:
                result += [("mac-tailscale", address, p) for p in PORTS]
    network = inspect(PROJECT + "-probe")["NetworkSettings"]["Networks"][PROJECT + "_ingress"]
    result += [("fixture-ipv4", network["IPAddress"], 9222),
               ("fixture-ipv6", network["GlobalIPv6Address"], 9222)]
    assert all(address for _, address, _ in result)
    return result


def probe(target_list, *, protected):
    identifier = container()
    def blocked_counts():
        rules = run(DOCKER, "exec", identifier, "nft", "-y", "list", "table", "inet", "atlas_egress").stdout
        return {family: int(re.search(rf"meta nfproto {family} counter packets (\d+)", rules)[1])
                for family in ["ipv4", "ipv6"]}
    before = blocked_counts() if protected else None
    def connect(target):
        label, address, port = target
        result = run(DOCKER, "exec", identifier, *(DROP if protected else []),
                     "nc", "-z", "-w", "1", address, str(port), check=False, timeout=10)
        assert result.returncode in (0, 1), result.stderr
        return {"label": label, "address": address, "port": port, "connected": result.returncode == 0}
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(connect, target_list))
    save("protected-probes.json" if protected else "baseline-probes.json", rows)
    if protected:
        assert not any(row["connected"] for row in rows), rows
        after = blocked_counts()
        assert all(after[family] > before[family] for family in after), (before, after)
        save("denied-counters.json", {"before": before, "after": after})
    else:
        for label in ["host-name", "host-numeric", "fixture-ipv4", "fixture-ipv6"]:
            selected = [row for row in rows if row["label"] == label]
            assert selected and all(row["connected"] for row in selected), selected
    print(f"{'Protected' if protected else 'Baseline'}: {sum(r['connected'] for r in rows)}/{len(rows)} TCP handshakes connected", flush=True)


def healthy():
    for _ in range(60):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/health", timeout=2) as response:
                assert json.load(response) == {"ok": True}
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError("Disposable app did not become healthy")


def runtime_checks():
    gateway = inspect(container())
    host = gateway["HostConfig"]
    assert host["ReadonlyRootfs"] and host["CapDrop"] == ["ALL"]
    assert set(host["CapAdd"]) == {"CAP_NET_ADMIN", "CAP_SETUID", "CAP_SETGID", "CAP_SETPCAP"}
    assert "no-new-privileges:true" in host["SecurityOpt"]
    assert gateway["Config"]["Healthcheck"]["Test"][:2] == ["CMD", *DROP]
    assert not host["Init"] and not host["Privileged"] and not gateway["Mounts"]
    assert host["PortBindings"]["8786/tcp"] == [{"HostIp": "127.0.0.1", "HostPort": str(PORT)}]
    assert host["Memory"] == host["MemorySwap"] == 192 * 1024**2
    assert host["NanoCpus"] == 500_000_000 and host["PidsLimit"] == 32
    children = execute("cat", "/proc/1/task/1/children").stdout.split()
    statuses = {}
    for pid in ["1", *children]:
        status = execute("cat", f"/proc/{pid}/status").stdout
        fields = dict(line.split(":", 1) for line in status.splitlines())
        assert fields["Name"].strip() == "nginx", fields
        assert fields["Uid"].split() == ["101"] * 4
        assert fields["Gid"].split() == ["101"] * 4
        for key in ["CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb"]:
            assert int(fields[key].strip(), 16) == 0, (pid, key, fields[key])
        assert fields["NoNewPrivs"].strip() == "1"
        statuses[pid] = {key: fields[key].strip() for key in ["Name", "Uid", "Gid", "CapEff", "CapBnd", "NoNewPrivs"]}
    assert children
    save("nginx-processes.json", statuses)
    test = """
set -eu
test "$(id -u)" = 101
test "$(id -g)" = 101
grep -q 'CapBnd:.*0000000000000000' /proc/self/status
grep -q 'NoNewPrivs:.*1' /proc/self/status
if nft list table inet atlas_egress 2>/dev/null; then exit 1; fi
if setpriv --reuid=0 true 2>/dev/null; then exit 1; fi
for path in /etc/should-not-write /usr/local/bin/should-not-write; do
    if touch "$path" 2>/dev/null; then exit 1; fi
done
test ! -e /var/run/docker.sock
test ! -e /Users
wget -q -O /dev/null http://127.0.0.1:8786/api/health
"""
    execute("sh", "-c", test, unprivileged=True)
    execute("nslookup", "atlas", unprivileged=True)
    rules = execute("nft", "-a", "-y", "list", "ruleset").stdout
    (STATE / "ruleset.txt").write_text(rules)
    assert "priority -110" in rules and "priority -100" in rules
    print("PASS: non-root Nginx master/workers, zero capability sets, protected health check, read-only filesystem, local DNS", flush=True)


def acceptance():
    path = APP / "tests/container_acceptance.py"
    result = run(sys.executable, str(path), env={**os.environ, "LAYER_ATLAS_VERIFY_PROJECT": PROJECT,
                                               "LAYER_ATLAS_VERIFY_CONFIG": str(STATE / "protected.json")})
    print(result.stdout, flush=True)
    print(result.stderr, flush=True)


def lifecycle():
    env_file = manage.prepare_network(PROJECT)
    previous = env_file.read_text()
    before = inspect(container("atlas"))["NetworkSettings"]["Networks"][PROJECT + "_isolated"]["IPAddress"]
    compose("up", "-d", "--no-build", "--force-recreate", "--wait", "--wait-timeout", "45", "atlas")
    after = inspect(container("atlas"))["NetworkSettings"]["Networks"][PROJECT + "_isolated"]["IPAddress"]
    assert before == after
    manage.prepare_network(PROJECT)
    assert env_file.read_text() == previous
    healthy()
    compose("restart", "gateway")
    healthy()
    runtime_checks()
    probe(json.loads((STATE / "targets.json").read_text()), protected=True)
    compose("up", "-d", "--no-build", "--force-recreate", "--wait", "--wait-timeout", "45", "gateway")
    healthy()
    runtime_checks()
    probe(json.loads((STATE / "targets.json").read_text()), protected=True)
    print("PASS: backend recreation retains reserved address; firewall survives gateway restart/recreation", flush=True)


def failures():
    outcomes = {}
    for variant in ["no-net-admin", "no-setpcap", "missing-address", "invalid-address"]:
        compose("up", "-d", "--no-build", "--no-deps", "--force-recreate", "gateway", variant=variant)
        for _ in range(30):
            state = inspect(container())["State"]
            if state["Status"] == "exited":
                break
            time.sleep(0.1)
        assert state["Status"] == "exited" and state["ExitCode"] != 0, (variant, state)
        with socket.socket() as sock:
            sock.settimeout(1)
            assert sock.connect_ex(("127.0.0.1", PORT)) != 0, variant
        logs = run(DOCKER, "logs", container())
        outcomes[variant] = {"exit_code": state["ExitCode"], "logs": logs.stdout + logs.stderr}
    save("failure-tests.json", outcomes)
    compose("up", "-d", "--no-build", "--wait", "--wait-timeout", "45")
    healthy()
    print("PASS: missing privileges/address or invalid rules prevent the gateway from listening", flush=True)


def cleanup():
    assert live_snapshot() == json.loads((STATE / "live-before.json").read_text()), "Live deployment changed"
    probe_container = run(DOCKER, "inspect", PROJECT + "-probe", check=False)
    if probe_container.returncode == 0:
        d = json.loads(probe_container.stdout)[0]
        assert d["Config"]["Labels"]["com.docker.compose.project"] == PROJECT
        docker("rm", "-f", d["Id"])
    if (STATE / "protected.json").exists():
        compose("down", "--volumes")
    network_result = run(DOCKER, "network", "inspect", PROJECT + "_isolated", check=False)
    if network_result.returncode == 0:
        network = json.loads(network_result.stdout)[0]
        assert network["Labels"]["com.docker.compose.project"] == PROJECT and not network["Containers"]
        docker("network", "rm", network["Id"])
    assert not docker("ps", "-aq", "--filter", f"label=com.docker.compose.project={PROJECT}")
    assert live_snapshot() == json.loads((STATE / "live-before.json").read_text())
    with urllib.request.urlopen("http://127.0.0.1:8786/api/health", timeout=3) as response:
        assert response.status == 200
    print("PASS: disposable containers/networks/database removed; live containers untouched and healthy", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "build", "baseline", "protected", "acceptance", "lifecycle", "failures", "cleanup"])
    action = parser.parse_args().action
    if action == "build":
        for name in ["Dockerfile", "start.sh", "unprivileged.sh", "verify-unprivileged.sh"]:
            shutil.copyfile(APP / "gateway" / name, STATE / "build" / name)
        shutil.copyfile(APP / "gateway/nginx.conf", STATE / "build/nginx.conf")
        compose("build", timeout=300)
    elif action == "baseline":
        compose("up", "-d", "--no-build", "--wait", "--wait-timeout", "45", variant="baseline")
        fixture()
        target_list = targets()
        save("targets.json", target_list)
        probe(target_list, protected=False)
    elif action == "protected":
        compose("up", "-d", "--no-build", "--wait", "--wait-timeout", "45")
        healthy()
        runtime_checks()
        probe(json.loads((STATE / "targets.json").read_text()), protected=True)
    else:
        globals()[action]()


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(error.stdout or "", flush=True)
        print(error.stderr or "", flush=True)
        raise
