#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIDocGenius Web 应用启动文件
"""
import uvicorn
from AIDocGenius.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
