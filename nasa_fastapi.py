from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates= Jinja2Templates(directory="templates")
@app.get("/rover/{rover_name}/photos")
async def get_rover_photos(request:Request,rover_name: str, sol: int =  1000):
    api_key = 'Replace with your actual API key'  
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/"
    url = f"{base_url}{rover_name}/photos?sol={sol}&api_key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code ==  200:
            data = response.json()
            photos = data.get("photos", [])
            image_urls = [photo['img_src'] for photo in photos]
            return templates.TemplateResponse("nasa.html",{ "request":request, "image_urls":image_urls})     
        else:
            return {"error": "Failed to fetch photos", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}