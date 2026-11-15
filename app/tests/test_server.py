import copy
from contextlib import closing
import http.client
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest

spec = importlib.util.spec_from_file_location("layer_atlas_server", Path(__file__).parents[1] / "server.py")
server_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server_module)


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "results.sqlite3"
        self.server = server_module.make_server(0, self.path, ["atlas.example"])
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.example = json.loads((Path(__file__).parents[1] / "examples/example.json").read_text())

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.directory.cleanup()

    def request(self, method, path, payload=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        request_headers = {"Content-Type": "application/json"}
        request_headers.update(headers or {})
        data = json.dumps(payload) if payload is not None else None
        connection.request(method, path, data, request_headers)
        response = connection.getresponse()
        body = response.read()
        status = response.status
        connection.close()
        return status, body

    def test_import_notes_exports_and_tasks(self):
        status, body = self.request("POST", "/api/runs", self.example)
        self.assertEqual(status, 201)
        run = json.loads(body)
        identifier = run["id"]
        self.assertNotIn("demo", run)
        status, body = self.request("PATCH", f"/api/runs/{identifier}", {"notes": "Saved note", "revision": 1})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["revision"], 2)
        self.assertEqual(self.request("PATCH", f"/api/runs/{identifier}", {"notes": "Stale note", "revision": 1})[0], 409)
        status, body = self.request("GET", f"/api/runs/{identifier}/export.json")
        self.assertEqual(status, 200)
        exported = json.loads(body)
        self.assertEqual(exported["notes"], "Saved note")
        self.assertNotIn("id", exported)
        self.assertEqual(server_module.validate_run(exported)["matrix"], self.example["matrix"])
        status, body = self.request("GET", f"/api/runs/{identifier}/matrix.csv")
        self.assertEqual(status, 200)
        self.assertIn(b"label,L0,L1,L2", body)
        self.assertEqual(self.request("PATCH", "/api/tasks/1", {"done": True})[0], 200)
        with closing(server_module.sqlite3.connect(self.path)) as db:
            self.assertEqual(db.execute("SELECT done FROM tasks WHERE id=1").fetchone()[0], 1)
            self.assertIn("Saved note", db.execute("SELECT payload FROM runs").fetchone()[0])
        self.assertEqual(self.request("DELETE", f"/api/runs/{identifier}", {})[0], 200)
        self.assertEqual(self.request("GET", f"/api/runs/{identifier}")[0], 404)

    def test_validation_and_failed_import_atomicity(self):
        invalid = [
            ("metric", []), ("sample_count", True), ("sample_count", 0),
            ("labels", ["L0", "L0", "L2"]), ("accuracy", 10**400),
            ("matrix", [[1, 10**400, .2], [10**400, 1, .8], [.2, .8, 1]]),
            ("matrix", [[1, True, .2], [True, 1, .8], [.2, .8, 1]]),
            ("matrix", [[1, .4, .2], [.5, 1, .8], [.2, .8, 1]]),
            ("name", "\ud800"),
        ]
        for field, value in invalid:
            with self.subTest(field=field, value=str(value)[:30]):
                payload = copy.deepcopy(self.example)
                payload[field] = value
                self.assertEqual(self.request("POST", "/api/runs", payload)[0], 400)
        self.assertEqual(json.loads(self.request("GET", "/api/runs")[1]), [])

    def test_proxy_origin_and_static_allowlist(self):
        self.assertEqual(self.request("POST", "/api/runs", self.example, {"Host": "atlas.example:8443", "Origin": "https://atlas.example:8443"})[0], 201)
        self.assertEqual(self.request("POST", "/api/runs", self.example, {"Origin": "https://external.example"})[0], 403)
        self.assertEqual(self.request("POST", "/api/runs", self.example, {"Host": "evil.example"})[0], 403)
        self.assertEqual(self.request("POST", "/api/runs", self.example, {"Content-Type": "text/plain"})[0], 415)
        for path in ["/server.py", "/data/layer-atlas.sqlite3", "/../server.py"]:
            self.assertEqual(self.request("GET", path)[0], 404)
        self.assertEqual(self.request("GET", "/")[0], 200)

    def test_oversized_body_rejected_before_read(self):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request("POST", "/api/runs", b"", {"Content-Type": "application/json", "Content-Length": str(server_module.MAX_BODY + 1)})
        response = connection.getresponse()
        self.assertEqual(response.status, 413)
        response.read()
        connection.close()


if __name__ == "__main__":
    unittest.main()
