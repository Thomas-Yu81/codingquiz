import io
import threading
from datetime import datetime, UTC
from typing import Dict, List, Optional, Tuple, TypedDict

from fastapi import FastAPI, UploadFile, File, Path, Query, HTTPException
from fastapi.responses import Response
from PIL import Image


#app configuration
class Config:
    api_path = "/api/v1/image"
    max_image_size = 10 * 1024 * 1024
    allowed_formats = {"jpg", "jpeg", "png"}
    host = "0.0.0.0"
    port = 5001
    debug = True


#utils function
def check_image_valid(filename: str, file_size: int) -> None:
    if "." not in filename:
        raise HTTPException(status_code=400, detail="file is not valid")

    suffix = filename.rsplit(".", 1)[1].lower()
    if suffix not in Config.allowed_formats:
        raise HTTPException(status_code=400, detail="Only allowed files are supported")

    if file_size <= 0:
        raise HTTPException(status_code=400, detail="file is empty ")

    if file_size > Config.max_image_size:
        raise HTTPException(status_code=413, detail="file size > 10MB limit")


def make_unique_filename(orig_filename: str) -> str:
    suffix = orig_filename.rsplit(".", 1)[1].lower()
    time_str = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    return f"img_comp_{time_str}.{suffix}"


def compress_image_simple(orig_bytes: bytes, orig_filename: str) -> Tuple[bytes, str]:
    try:
        with Image.open(io.BytesIO(orig_bytes)) as img:
            output = io.BytesIO()
            suffix = orig_filename.rsplit(".", 1)[1].lower()

            if suffix in ["jpg", "jpeg"]:
                img.save(output, "JPEG", quality=30)
                return output.getvalue(), "image/jpeg"
            else:
                img.save(output, "PNG", compress_level=1)
                return output.getvalue(), "image/png"
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compression failed: {str(e)}") from e


#memory storage
compressed_imgs: Dict[str, bytes] = {}


class HistoryRecord(TypedDict):
    id: int
    upload_time: str
    orig_name: str
    comp_name: str
    orig_size_kb: int
    comp_size_kb: int


history_list: List[HistoryRecord] = []
next_history_id = 1
lock = threading.Lock()


#FastAPI
app = FastAPI(
    title="image upload and compress",
    description="upload + compress + history query + download",
    version="1.0"
)


#API endpoint
@app.post("/api/v1/image/upload", summary="upload and compress image")
async def upload_image(image: UploadFile = File(...)):
    #Validation
    check_image_valid(image.filename, image.size)

    #read file
    orig_bytes = await image.read()
    await image.close()

    #compress
    comp_bytes, mime_type = compress_image_simple(orig_bytes, image.filename)

    #save and record history
    comp_filename = make_unique_filename(image.filename)
    with lock:
        global next_history_id
        compressed_imgs[comp_filename] = comp_bytes
        history = HistoryRecord(
            id=next_history_id,
            upload_time=datetime.now(UTC).isoformat(),
            orig_name=image.filename,
            comp_name=comp_filename,
            orig_size_kb=len(orig_bytes) // 1024,
            comp_size_kb=len(comp_bytes) // 1024
        )
        history_list.append(history)
        next_history_id += 1

    #return compressed image
    return Response(
        content=comp_bytes,
        media_type=mime_type,
        headers={"Comp-Filename": comp_filename}
    )


@app.get("/api/v1/image/history", summary="Query processing history")
def get_history(limit: Optional[int] = Query(None, ge=1)):
    with lock:
        sorted_history = sorted(history_list, key=lambda x: x["upload_time"], reverse=True)
        if limit:
            sorted_history = sorted_history[:limit]

    return {
        "success": True,
        "total_count": len(history_list),
        "return_count": len(sorted_history),
        "history": sorted_history
    }


@app.get(f"/api/v1/image/download/{'{comp_filename}'}", summary="download compressed image")
def download_image(comp_filename: str = Path(...)):
    with lock:
        if comp_filename not in compressed_imgs:
            raise HTTPException(status_code=404, detail=f"compressed image '{comp_filename}' not found")
        img_bytes = compressed_imgs[comp_filename]

    mime_type = "image/jpeg" if comp_filename.lower().endswith(("jpg", "jpeg")) else "image/png"
    return Response(
        content=img_bytes,
        media_type=mime_type,
        headers={"Content-Disposition": f"attachment; filename={comp_filename}"}
    )


#run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=Config.host,
        port=Config.port,
        reload=Config.debug,
        workers=1
    )