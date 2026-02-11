from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import uvicorn
from typing import Optional, List, Any, Dict
from starlette.background import BackgroundTask
import shutil
import zipfile
import uuid

from .processor import DocProcessor
from .utils import logger

app = FastAPI(
    title="AIDocGenius API",
    description="AI驱动的文档处理API",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

processor = DocProcessor()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

def _success(data: Any, request_id: str, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ok",
            "data": data,
            "error": None,
            "request_id": request_id
        }
    )

def _error(code: str, message: str, request_id: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "data": None,
            "error": {
                "code": code,
                "message": message,
                "details": details or {}
            },
            "request_id": request_id
        }
    )

def _cleanup_files(*paths: str) -> None:
    for path in paths:
        try:
            Path(path).unlink()
        except FileNotFoundError:
            continue

def _cleanup_dirs(*paths: str) -> None:
    for path in paths:
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            continue

def _parse_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

async def _save_upload_files(files: List[UploadFile], target_dir: Path) -> List[Path]:
    saved_paths = []
    for upload in files:
        suffix = Path(upload.filename).suffix
        file_path = target_dir / f"{Path(upload.filename).stem}{suffix}"
        content = await upload.read()
        file_path.write_bytes(content)
        saved_paths.append(file_path)
    return saved_paths

@app.get("/health")
async def health_check(request: Request):
    """
    健康检查端点
    """
    return _success({"status": "healthy", "version": "0.1.0"}, request.state.request_id)

@app.get("/")
async def read_root():
    """
    返回主页
    """
    return FileResponse(static_path / "index.html")

@app.post("/summarize")
async def summarize_document(
    request: Request,
    file: UploadFile = File(...),
    max_length: Optional[int] = Query(default=None),
    min_length: Optional[int] = Query(default=None)
):
    """
    生成文档摘要
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        summary = processor.generate_summary(
            temp_path,
            max_length=max_length,
            min_length=min_length
        )

        Path(temp_path).unlink()
        return _success({"summary": summary}, request.state.request_id)

    except ImportError as e:
        logger.error(f"Summarization error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.post("/translate")
async def translate_document(
    request: Request,
    target_language: str,
    file: UploadFile = File(...),
    source_language: Optional[str] = Query(default=None)
):
    """
    翻译文档
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        translation = processor.translate(
            temp_path,
            target_language=target_language,
            source_language=source_language
        )

        Path(temp_path).unlink()
        return _success({"translation": translation}, request.state.request_id)

    except ImportError as e:
        logger.error(f"Translation error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.post("/analyze")
async def analyze_document(request: Request, file: UploadFile = File(...)):
    """
    分析文档
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        analysis = processor.analyze(temp_path)
        Path(temp_path).unlink()
        return _success(analysis, request.state.request_id)

    except ImportError as e:
        logger.error(f"Analysis error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.post("/compare")
async def compare_documents(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """
    比较两个文档
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file1.filename).suffix) as temp_file1:
            temp_file1.write(await file1.read())
            path1 = temp_file1.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file2.filename).suffix) as temp_file2:
            temp_file2.write(await file2.read())
            path2 = temp_file2.name

        result = processor.compare_documents(path1, path2)
        _cleanup_files(path1, path2)
        return _success(result, request.state.request_id)

    except ImportError as e:
        logger.error(f"Comparison error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.post("/merge")
async def merge_documents(
    request: Request,
    files: List[UploadFile] = File(...),
    output_format: str = Query(default="txt"),
    smart_merge: bool = Query(default=False)
):
    """
    合并多个文档
    """
    input_dir = None
    output_path = None
    try:
        input_dir = tempfile.mkdtemp()
        input_path = Path(input_dir)
        saved_files = await _save_upload_files(files, input_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as temp_output:
            output_path = temp_output.name

        processor.merge_documents([str(p) for p in saved_files], output_path, smart_merge=smart_merge)

        output_name = f"merged.{output_format}"
        return FileResponse(
            output_path,
            filename=output_name,
            media_type="application/octet-stream",
            background=BackgroundTask(_cleanup_dirs, input_dir)
        )

    except ImportError as e:
        if input_dir:
            _cleanup_dirs(input_dir)
        if output_path:
            _cleanup_files(output_path)
        logger.error(f"Merge error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        if input_dir:
            _cleanup_dirs(input_dir)
        if output_path:
            _cleanup_files(output_path)
        logger.error(f"Merge error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.post("/batch")
async def batch_process(
    request: Request,
    files: List[UploadFile] = File(...),
    operations: str = Query(..., description="Comma-separated operations"),
    output_format: Optional[str] = Query(default=None),
    target_language: Optional[str] = Query(default=None),
    source_language: Optional[str] = Query(default=None),
    report: bool = Query(default=True),
    report_formats: Optional[str] = Query(default="json"),
    zip_output: bool = Query(default=True)
):
    """
    批量处理文档
    """
    input_dir = None
    output_dir = None
    zip_path = None
    try:
        input_dir = tempfile.mkdtemp()
        output_dir = tempfile.mkdtemp()
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        await _save_upload_files(files, input_path)
        ops = _parse_list(operations)
        report_format_list = _parse_list(report_formats)

        results = processor.batch_process(
            input_dir=input_path,
            output_dir=output_path,
            operations=ops,
            output_format=output_format,
            target_language=target_language,
            source_language=source_language,
            report=report,
            report_formats=report_format_list
        )

        if not zip_output:
            return _success(results, request.state.request_id)

        zip_path = Path(output_dir) / "batch_results.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in output_path.rglob("*"):
                if file.is_file():
                    zipf.write(file, arcname=file.relative_to(output_path))

        return FileResponse(
            zip_path,
            filename="batch_results.zip",
            media_type="application/zip",
            background=BackgroundTask(_cleanup_dirs, input_dir, output_dir)
        )

    except ImportError as e:
        if input_dir:
            _cleanup_dirs(input_dir)
        if output_dir:
            _cleanup_dirs(output_dir)
        if zip_path:
            _cleanup_files(str(zip_path))
        logger.error(f"Batch error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        if input_dir:
            _cleanup_dirs(input_dir)
        if output_dir:
            _cleanup_dirs(output_dir)
        if zip_path:
            _cleanup_files(str(zip_path))
        logger.error(f"Batch error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.post("/convert")
async def convert_document(
    request: Request,
    output_format: str,
    file: UploadFile = File(...)
):
    """
    转换文档格式
    """
    input_path = None
    output_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_input:
            content = await file.read()
            temp_input.write(content)
            input_path = temp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as temp_output:
            output_path = temp_output.name

        processor.convert(input_path, output_path)

        output_name = f"{Path(file.filename).stem}.{output_format}"
        return FileResponse(
            output_path,
            filename=output_name,
            media_type="application/octet-stream",
            background=BackgroundTask(_cleanup_files, input_path, output_path)
        )

    except ImportError as e:
        if input_path:
            _cleanup_files(input_path)
        if output_path:
            _cleanup_files(output_path)
        logger.error(f"Conversion error: {str(e)}")
        return _error("DEPENDENCY_MISSING", str(e), request.state.request_id, status_code=500)
    except Exception as e:
        if input_path:
            _cleanup_files(input_path)
        if output_path:
            _cleanup_files(output_path)
        logger.error(f"Conversion error: {str(e)}")
        return _error("PROCESS_FAILED", str(e), request.state.request_id, status_code=500)

@app.get("/supported-formats")
async def get_supported_formats(request: Request):
    """
    获取支持的文件格式
    """
    return _success({"formats": processor.converter.get_supported_formats()}, request.state.request_id)

@app.get("/supported-languages")
async def get_supported_languages(request: Request):
    """
    获取支持的语言
    """
    return _success({"languages": processor.translator.get_supported_languages()}, request.state.request_id)

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """
    启动API服务器
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server() 
