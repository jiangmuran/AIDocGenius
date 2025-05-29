from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import uvicorn
from typing import Optional
from pydantic import BaseModel

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

class TranslationRequest(BaseModel):
    target_language: str
    source_language: Optional[str] = None

class SummaryRequest(BaseModel):
    max_length: Optional[int] = None
    min_length: Optional[int] = None

@app.get("/health")
async def health_check():
    """
    健康检查端点
    """
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/")
async def read_root():
    """
    返回主页
    """
    return FileResponse(static_path / "index.html")

@app.post("/summarize")
async def summarize_document(
    params: Optional[SummaryRequest] = None,
    file: UploadFile = File(...)
):
    """
    生成文档摘要
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        summary = processor.generate_summary(
            temp_path,
            max_length=params.max_length if params else None,
            min_length=params.min_length if params else None
        )

        Path(temp_path).unlink()
        return JSONResponse(content={"summary": summary})

    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_document(
    target_language: str,
    file: UploadFile = File(...),
    source_language: Optional[str] = None
):
    """
    翻译文档
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        translation = processor.translate(
            temp_path,
            target_language=target_language,
            source_language=source_language
        )

        Path(temp_path).unlink()
        return JSONResponse(content={"translation": translation})

    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    分析文档
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        analysis = processor.analyze(temp_path)
        Path(temp_path).unlink()
        return JSONResponse(content=analysis)

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert")
async def convert_document(
    output_format: str,
    file: UploadFile = File(...)
):
    """
    转换文档格式
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_input:
            content = await file.read()
            temp_input.write(content)
            input_path = temp_input.name

        output_path = Path(input_path).with_suffix(f".{output_format}")
        processor.convert(input_path, str(output_path))

        with open(output_path, "rb") as f:
            content = f.read()

        Path(input_path).unlink()
        Path(output_path).unlink()

        return JSONResponse(content={"converted_content": content.decode()})

    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported-formats")
async def get_supported_formats():
    """
    获取支持的文件格式
    """
    return {
        "formats": processor.converter.get_supported_formats()
    }

@app.get("/supported-languages")
async def get_supported_languages():
    """
    获取支持的语言
    """
    return {
        "languages": processor.translator.get_supported_languages()
    }

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """
    启动API服务器
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server() 