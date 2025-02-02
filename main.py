from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import matplotlib.pyplot as plt
from fastapi.responses import Response

app = FastAPI()

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Read image from uploaded file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    canny = cv2.Canny(blur, 10, 150)
    
    # Encode processed image to return as response
    _, encoded_img = cv2.imencode('.png', canny)
    return Response(content=encoded_img.tobytes(), media_type="image/png")
