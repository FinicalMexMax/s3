from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)
    return {"message": f"File '{file.filename}' uploaded successfully"}

@app.get("/download/{filename}")
def download_file(filename: str):
    s3_client.download_file(S3_BUCKET_NAME, filename, filename)
    return FileResponse(path=filename)

@app.delete("/delete/{filename}")
def delete_file(filename: str):
    s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=filename)
    return {"message": f"File '{filename}' deleted successfully"}
