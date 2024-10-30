from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Initialize the FastAPI app
app = FastAPI()

# Set up Jinja2 templates in the "templates" folder
templates = Jinja2Templates(directory="templates")

# Define a route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Welcome to FastAPI"})
