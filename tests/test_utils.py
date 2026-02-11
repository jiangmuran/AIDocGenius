#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试工具函数
"""
import unittest
import tempfile
from pathlib import Path

from AIDocGenius.utils import load_config, ensure_text


class TestUtils(unittest.TestCase):
    def test_load_config_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "config.json"
            path.write_text('{"summarizer": {"use_simple": true}}', encoding="utf-8")
            config = load_config(path)
            self.assertIn("summarizer", config)

    def test_ensure_text(self):
        self.assertEqual(ensure_text("hello"), "hello")
        self.assertIn("a", ensure_text({"a": 1}))


if __name__ == '__main__':
    unittest.main()
