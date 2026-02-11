#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API 端点测试
"""
import unittest

try:
    from fastapi.testclient import TestClient
    from AIDocGenius.api import app
    FASTAPI_AVAILABLE = True
except ImportError:
    TestClient = None
    app = None
    FASTAPI_AVAILABLE = False


@unittest.skipIf(not FASTAPI_AVAILABLE, "fastapi not available")
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), "ok")
        self.assertEqual(body.get("data", {}).get("status"), "healthy")

    def test_summarize(self):
        files = {"file": ("doc.txt", "这是一个测试文档。它包含两句话。", "text/plain")}
        response = self.client.post("/summarize?max_length=50", files=files)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), "ok")
        self.assertIn("summary", body.get("data", {}))

    def test_analyze(self):
        files = {"file": ("doc.txt", "这是一个测试文档。", "text/plain")}
        response = self.client.post("/analyze", files=files)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), "ok")
        self.assertIn("statistics", body.get("data", {}))

    def test_compare(self):
        files = {
            "file1": ("doc1.txt", "第一段内容。", "text/plain"),
            "file2": ("doc2.txt", "第二段内容。", "text/plain")
        }
        response = self.client.post("/compare", files=files)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), "ok")
        self.assertIn("similarity", body.get("data", {}))

    def test_merge(self):
        files = [
            ("files", ("doc1.txt", "第一段内容。", "text/plain")),
            ("files", ("doc2.txt", "第二段内容。", "text/plain"))
        ]
        response = self.client.post("/merge?output_format=txt", files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("content-type"), "application/octet-stream")

    def test_batch_json(self):
        files = [
            ("files", ("doc1.txt", "第一段内容。", "text/plain")),
            ("files", ("doc2.txt", "第二段内容。", "text/plain"))
        ]
        response = self.client.post(
            "/batch?operations=summarize,analyze&zip_output=false&report=true&report_formats=json",
            files=files
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), "ok")
        self.assertIsInstance(body.get("data"), dict)


if __name__ == '__main__':
    unittest.main()
