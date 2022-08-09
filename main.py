import io
import PIL

from io import BytesIO
from typing import Optional
from urllib.parse import urlparse

from PIL import Image
from pydantic import BaseModel
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.param_functions import Query
 
app = FastAPI(
    title="sqy-watermark-engine",
    description="Use this API to paste user logo as a watermark at the center of input images",
    version="2.0.1",
)

class ImageDetails(BaseModel):
    url_: str


@app.get("/")
async def root():
    return "Hello World!!!"

    
@app.post("/addWatermark_by_file")
async def add_watermark_by_file(position: str = Query("centre", enum=["centre", "bottom_right","bottom_left","bottom"]),width_percentage: Optional[float] = Query("0.2"),insert_image: UploadFile=File(...),logo_image: UploadFile=File(...)):

    contents = await insert_image.read() #Building image
    original_image = Image.open(BytesIO(contents))
    format_ = original_image.format.lower()
    
    def get_content_type(format_):

        type_ = "image/jpg"
        
        if format_ == "gif":
            type_ = "image/gif"
        elif format_ == "webp":
            type_ = "image/webp"
        elif format_ == "png":
            type_ = "image/png"
        elif format_ == "jpeg":
            type_ = "image/jpeg"
        
        return type_
    
    contents2 = await logo_image.read() #Building image
    logo = Image.open(BytesIO(contents2))
    
    # logo = logo.convert("RGB")
    # logo.save("img1g.png")
    # logo = Image.open("img1g.png")

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
    original_image.save(buf,format=format_.lower(), quality=100)
    buf.seek(0)
    
    return StreamingResponse(buf,media_type=get_content_type(format_))

@app.post("/addWatermark_by_URL")
async def add_watermark_by_URL(insert_image:str,logo_image:str,position: str = Query("centre", enum=["centre", "bottom_right","bottom_left","bottom"]),width_percentage: Optional[float] = Query("0.2")):
    
    response = requests.get(insert_image)
    image_bytes = io.BytesIO(response.content)
    
    original_image = Image.open(image_bytes)
    format_ = original_image.format.lower()
    
    response = requests.get(logo_image.lower())
    image_bytes2 = io.BytesIO(response.content) 
    logo = Image.open(image_bytes2).convert("RGBA")
    

    filename = insert_image.lower()
    print(filename)
    #print(filename)
    #this function get the format type of input image
    
    def get_format(format_):  

        if format_ == "jpg":
            format_ = "jpg"
        elif format_== "jpeg":
            format_ = "jpeg"
        elif format_ == "webp":
            format_ = "WebP"
        elif format_ == "gif":
            format_ = "gif"
    
        return format_
 
   
    # #this function for gave the same type of format to output
    def get_content_type(format_):
        
        if format_ == "gif":
            type_ = "image/gif"
        elif format_ == "webp":
            type_ = "image/webp"
        elif format_ == "png":
            type_ = "image/png"
        elif format_ == "jpg":
            type_ = "image/jpg"
        elif format_ == "jpeg":
            type_ = "image/jpeg"
        #print(type_)
        return type_

    format_ = get_format(format_.lower())#here format_ store the type of image by filename
    
    
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
        original_image.paste(logo,(left, top), mask=logo)
 
    buf = BytesIO()
    original_image.save(buf, format=format_.lower(), quality=100)
    buf.seek(0)

    return StreamingResponse(buf,media_type=get_content_type(format_))