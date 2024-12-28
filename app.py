from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from PIL import Image
from pyzerox import zerox
import shutil
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# CORS settings - adjust 'allow_origins' to your frontend's URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL (e.g., "https://yourdomain.com") in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model setup
model = "gpt-4o-mini"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Helper function to convert images to PDFs
def convert_image_to_pdf(image_path, output_pdf_path):
    try:
        with Image.open(image_path) as img:
            img.convert("RGB").save(output_pdf_path, "PDF")
        return output_pdf_path
    except Exception as e:
        print(f"Error converting image to PDF: {e}")
        return None

# Endpoint to handle file upload and processing
@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    # Create temporary storage directories
    upload_dir = "./uploads"
    output_dir = "./output_test"
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate unique filenames to avoid conflicts
    unique_id = uuid.uuid4().hex
    original_filename = f"{unique_id}_{file.filename}"
    file_path = os.path.join(upload_dir, original_filename)
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Check if the file is an image and convert to PDF if necessary
    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        pdf_path = os.path.join(upload_dir, f"{unique_id}_converted.pdf")
        converted_path = convert_image_to_pdf(file_path, pdf_path)
        if not converted_path:
            return JSONResponse({"error": "Failed to convert image to PDF"}, status_code=400)
        # Optionally, remove the original image file
        os.remove(file_path)
        file_path = converted_path
    
    # Process the file with Zerox
    try:
        result = await zerox(
            file_path=file_path,
            model=model,
            output_dir=output_dir,
            maintain_format=False,  # Disable format maintenance for single documents
            cleanup=True,           # Clean up temporary files after processing
            select_pages=[1]
        )
        
        # Aggregate Markdown content
        print(result.pages[0].content)
        markdown_content = "\n\n".join([page.content for page in result.pages])
        os.remove(file_path)
        
        return {"markdown": markdown_content}
    except Exception as e:
        print(f"Error during processing: {e}")
        return JSONResponse({"error": "Processing failed"}, status_code=500)
