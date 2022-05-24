from io import BytesIO
from typing import Optional
from urllib.parse import urlparse
 
import numpy as np
from PIL import Image, ImageSequence
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.param_functions import Query
 
 
SQUARE_YARDS_LOGO = Image.open('api/images/slogo.png')
IC_LOGO = Image.open('api/images/iclogo2.png')
POSI_LIST = ["centre", "bottom_left", "bottom_right", "bottom"]
 
app = FastAPI(
    title="sqy-watermark-engine",
    description="Use this API to paste Square Yards logo as a watermark at the center of input images",
    version="2.0.1",
)

class ImageDetails(BaseModel):
    url_: str
    
 
@app.post("/addWatermark_by_file")
async def add_watermark_by_file(position: str = Query("centre", enum=["centre", "bottom_right","bottom_left","bottom"]),width_percentage: Optional[float] = Query("0.2"),original_image: UploadFile=File(...),watermark_image: UploadFile=File(...)):

    contents = await original_image.read() #Building image
    original_image = Image.open(BytesIO(contents))

    contents2 = await watermark_image.read() #Building image
    logo = Image.open(BytesIO(contents2))
    
    logo_width = int(original_image.size[0]*width_percentage)
    logo_height = int(logo.size[1]*(logo_width/logo.size[0]))
 

    if logo_height > original_image.size[1]:
        logo_height = original_image.size[1]
    

    if position == "centre":
        logo = logo.resize((logo_width, logo_height))
 
        top = (original_image.size[1]//2) - (logo_height//2)
        left = (original_image.size[0]//2) - (logo_width//2)
        original_image.paste(logo, (left, top), mask=logo)
 

    elif position == "bottom_right":
        logo = logo.resize((logo_width, logo_height))
 
        top = original_image.size[1] - logo_height
        left = original_image.size[0] - logo_width
        original_image.paste(logo, (left, top), mask=logo)
 

    elif position == "bottom_left":
        logo = logo.resize((logo_width, logo_height))
 
        top = original_image.size[1] - logo_height
        left = 0
        original_image.paste(logo, (left, top), mask=logo)
    elif position == "bottom":
        logo = logo.resize((logo_width, logo_height))
 
        top = original_image.size[1] - logo_height
        left = (original_image.size[0]//2) - (logo_width//2)
        original_image.paste(logo, (left, top), mask=logo)
 
    buf = BytesIO()
    original_image.save(buf, format="jpeg", quality=100)
    buf.seek(0)

    return StreamingResponse(buf,media_type="image/jpg")

@app.post("/addWatermark_by_URL")
async def add_watermark_by_file(original_image:str,watermark_image:str,position: str = Query("centre", enum=["centre", "bottom_right","bottom_left","bottom"]),width_percentage: Optional[float] = Query("0.2")):

    contents = await original_image.read() #Building image
    original_image = Image.open(BytesIO(contents))

    contents2 = await watermark_image.read() #Building image
    logo = Image.open(BytesIO(contents2))
    
    logo_width = int(original_image.size[0]*width_percentage)
    logo_height = int(logo.size[1]*(logo_width/logo.size[0]))
 

    if logo_height > original_image.size[1]:
        logo_height = original_image.size[1]
    

    if position == "centre":
        logo = logo.resize((logo_width, logo_height))
 
        top = (original_image.size[1]//2) - (logo_height//2)
        left = (original_image.size[0]//2) - (logo_width//2)
        original_image.paste(logo, (left, top), mask=logo)
 

    elif position == "bottom_right":
        logo = logo.resize((logo_width, logo_height))
 
        top = original_image.size[1] - logo_height
        left = original_image.size[0] - logo_width
        original_image.paste(logo, (left, top), mask=logo)
 

    elif position == "bottom_left":
        logo = logo.resize((logo_width, logo_height))
 
        top = original_image.size[1] - logo_height
        left = 0
        original_image.paste(logo, (left, top), mask=logo)
    elif position == "bottom":
        logo = logo.resize((logo_width, logo_height))
 
        top = original_image.size[1] - logo_height
        left = (original_image.size[0]//2) - (logo_width//2)
        original_image.paste(logo, (left, top), mask=logo)
 
    buf = BytesIO()
    original_image.save(buf, format="jpeg", quality=100)
    buf.seek(0)

    return StreamingResponse(buf,media_type="image/jpg")