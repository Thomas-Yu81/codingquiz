# webapp
# Features
- Image upload and compression
- History Query
- Memory Storage
- Syetem Logs

# Tech
Framework: FastAPI
Server: Uvicorn 
Image: Pillow
File: python-multipart

# Install
clone or download the project
- main.py (core service code)
- requirements.txt (dependency lsit)
- README.md

# Create and ativate ven, then install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Dependencies
fastapi=0.110.3
uvicorn=0.29.0
pillow=10.3.0
python-multipart=0.0.9

# Run 
Command 1:
python main.py

Command 2:
uvicorn main:app --host 0.0.0.0 --port 5001 --reload

--host 0.0.0.0: allows external to access the service (not just localhost)
--port 5001: Uses port 5001 or others
--reload: development model

# API Documentation and Test

Swagger UI: Visit http://<your-ip>:5001/docs
use <your-ip> or 127.0.0.1

For testing, click "Try it out" on each of endpoint session

# API endpoints
POST /api/v1/image/upload
GET /api/v1/image/history
GET /api/v1/image/download/{filename}

# API configration
class Config:
    api_path = "/api/v1/image"
    max_image_size = 10 * 1024 * 1024
    allowed_formats = {"jpg", "jpeg", "png"}
    host = "0.0.0.0"
    port = 5001
    debug = True