from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("manage", Path(__file__).resolve().parents[1] / "manage.py")
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)


class BackendNetworkTests(unittest.TestCase):
    def setUp(self):
        self.network = {
            "Id": "network-a", "Internal": True, "Driver": "bridge",
            "Labels": {"com.docker.compose.project": "test-atlas", "com.docker.compose.network": "isolated"},
            "IPAM": {"Config": [{"Subnet": "172.30.0.0/24", "Gateway": "172.30.0.1"}]},
            "Containers": {},
        }

    def test_adopts_existing_backend_address(self):
        self.network["Containers"]["atlas"] = {"Name": "test-atlas-atlas-1", "IPv4Address": "172.30.0.9/24"}
        self.assertEqual(manage.backend_address(self.network, "test-atlas"), "172.30.0.9")

    def test_reserves_free_address_and_retains_it_when_backend_is_stopped(self):
        self.assertEqual(manage.backend_address(self.network, "test-atlas"), "172.30.0.2")
        previous = {"LAYER_ATLAS_NETWORK_ID": "network-a", "LAYER_ATLAS_BACKEND_IPV4": "172.30.0.9"}
        self.assertEqual(manage.backend_address(self.network, "test-atlas", previous), "172.30.0.9")

    def test_reallocated_network_discards_old_address(self):
        previous = {"LAYER_ATLAS_NETWORK_ID": "removed-network", "LAYER_ATLAS_BACKEND_IPV4": "172.29.0.9"}
        self.assertEqual(manage.backend_address(self.network, "test-atlas", previous), "172.30.0.2")

    def test_conflicting_or_invalid_reservation_is_rejected(self):
        self.network["Containers"]["gateway"] = {"Name": "test-atlas-gateway-1", "IPv4Address": "172.30.0.2/24"}
        for address in ["172.30.0.2", "172.30.0.0", "172.30.0.255", "172.30.0.1", "192.0.2.1"]:
            with self.subTest(address=address), self.assertRaises(RuntimeError):
                manage.backend_address(self.network, "test-atlas", {
                    "LAYER_ATLAS_NETWORK_ID": "network-a", "LAYER_ATLAS_BACKEND_IPV4": address})

    def test_foreign_or_non_internal_network_is_rejected(self):
        for change in [{"Internal": False}, {"Driver": "host"}, {"Labels": {}}]:
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                manage.backend_address({**deepcopy(self.network), **change}, "test-atlas")

    def test_project_name_cannot_escape_state_directory(self):
        for project in ["../live", "/tmp/other", "test;command"]:
            with self.subTest(project=project), self.assertRaises(ValueError):
                manage.network_env(project)
