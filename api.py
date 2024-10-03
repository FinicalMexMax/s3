from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import uvicorn
import boto3


# Настройки для S3
S3_BUCKET_NAME = "bucket"
S3_REGION = "ch"
S3_ACCESS_KEY = "admin"
S3_SECRET_KEY = "xvS4'Zt;yfv(vh>!~xGNNBJOzNZ.O|Kl-_Q4z4z|3aA2cj4Rl^"


# Настройка клиента S3
s3_client = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите разрешенные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)
        return {"message": f"File '{file.filename}' uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download/{filename}")
def download_file(filename: str):
    try:
        s3_client.download_file(S3_BUCKET_NAME, filename, filename)
        return FileResponse(path=filename)
    except Exception as e:
        return {"error": str(e)}

@app.delete("/delete/{filename}")
def delete_file(filename: str):
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=filename)
        return {"message": f"File '{filename}' deleted successfully"}
    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    uvicorn.run(app)