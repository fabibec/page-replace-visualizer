from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
        title="Page Fault API", openapi_url="/openapi.json")

# Mounting the "frontend" directory to serve static files(HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="../frontend"), name="/static")

# Template configuration for Jinja2
# templates = Jinja2Templates(directory="../frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content="/static/index.html", status_code=200)




