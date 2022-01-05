from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket
from starlette.templating import Jinja2Templates
from service.visual_manipulation import grayscale

templates = Jinja2Templates(directory='client')

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text( grayscale(data) )

@app.route('/')
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})