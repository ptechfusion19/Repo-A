# Run command:
# uvicorn HTTP_Methods:app --reload
# Open in browser:
# http://127.0.0.1:8000/docs

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI(title="Black & White Image Converter API")

# -----------------------------
# 🏠 Root route (GET)
# -----------------------------
@app.get("/")
def root():
    """Root route: basic welcome message."""
    return {
        "message": "Welcome to the Black & White Image Converter API!",
        "usage": "Use POST /convert to upload an image."
    }


# -----------------------------
# 🎨 Image conversion function
# -----------------------------
def convert_to_black_white(image_file: UploadFile):
    """Convert the uploaded image to black and white (grayscale)."""
    try:
        # Open the uploaded image
        image = Image.open(image_file.file)

        # Convert to black and white
        bw_image = image.convert("L")

        # Save it to an in-memory buffer
        buffer = io.BytesIO()
        bw_image.save(buffer, format="JPEG")
        buffer.seek(0)

        return buffer

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


# -----------------------------
# 📤 POST Method (Convert image)
# -----------------------------
@app.post("/convert")
async def convert_image(file: UploadFile = File(...)):
    """Upload an image and get its black & white version."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file.")

    # Convert the image
    bw_buffer = convert_to_black_white(file)

    # Return the black & white image
    return StreamingResponse(bw_buffer, media_type="image/jpeg")


# -----------------------------
# 📥 GET Method (Sample message)
# -----------------------------
@app.get("/convert")
def get_info():
    """Get info about the conversion API."""
    return {
        "message": "Use POST /convert to upload and convert an image to black & white.",
        "methods_available": ["GET", "POST", "PATCH", "DELETE"]
    }


# -----------------------------
# 🛠️ PATCH Method (Simulated update)
# -----------------------------
@app.patch("/convert")
def update_conversion_settings(setting: str = "grayscale"):
    """Simulate updating conversion settings."""
    return {"message": f"Conversion setting updated to '{setting}' successfully."}


# -----------------------------
# ❌ DELETE Method (Simulated delete)
# -----------------------------
@app.delete("/convert")
def delete_conversion():
    """Simulate deleting previous conversion data (demo purpose)."""
    return {"message": "Previous conversion data (if any) deleted successfully."}