from pyzerox import zerox
import os
import asyncio
import dotenv
from PIL import Image

dotenv.load_dotenv()

## system prompt to use for the vision model
custom_system_prompt = None

model = "gpt-4o-mini" 
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Convert image to PDF
def convert_image_to_pdf(image_path, output_pdf_path="./docs/converted.pdf"):
    try:
        with Image.open(image_path) as img:
            img.convert("RGB").save(output_pdf_path, "PDF")  # Convert and save as PDF
        print(f"Image successfully converted to PDF: {output_pdf_path}")
        return output_pdf_path
    except Exception as e:
        print(f"Error converting image to PDF: {e}")
        return None


async def main():
    file_path = "./docs/testing.jpg"  # Local file path or file URL
    select_pages = [1]  # Specify pages to process (use `None` for all pages)
    output_dir = "./output_test" 

    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        file_path = convert_image_to_pdf(file_path)
        if not file_path:
            print('Failed converting image to pdf')
            return None
    try:
        result = await zerox(
            file_path=file_path,
            model=model,
            output_dir=output_dir,
            custom_system_prompt=custom_system_prompt,
            maintain_format=False,  # Disable for single images
            select_pages=[1],
            cleanup=True,  # Clean up temporary files
        )
        return result
    except Exception as e:
        print(f"Error during processing: {e}")
        return None

# run the main function:
result = asyncio.run(main())

# print markdown result
print(result)
