from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import constants as c
from validation import validateRefString
from algorithms import fifo, lru
import asyncio

# API Specification
app = FastAPI(
    title="Page Fault API", 
    version="0.0.1",
    summary="An API thats calculates page faults for different page replacement algorithms.",
    license_info=
    {
        "name": "MIT License",
        "identifier": "MIT",
        "url": "https://mit-license.org/"     
    },
    openapi_url="/openapi.json"
)


'''
This section handles the Frontend Endpoints
'''

# Mounting the "frontend" directory to serve static files(HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="../frontend"), name="/static")

# Template configuration for Jinja2
# templates = Jinja2Templates(directory="../frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content="/static/index.html", status_code=200)

'''
This section handles the Backend Endpoints
'''
@app.get("/api/refString/")
async def apiRefString(
        locality: Annotated[bool, Query(title="Locality creates more realistic Reference String")] = True,
        length: Annotated[int, Query(title="The length of the Reference String", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE
    ):
    raise NotImplementedError


@app.get("/api/faults/")
async def apiFaults(
        referenceString: str, 
        frames: Annotated[int, Query(title="The maximum Number of Frames", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE, 
        FIFO: Annotated[bool, Query(title="First-in-First-out Algorithm")] = True, 
        SC: Annotated[bool, Query(title="Second-Chance Algorithm")] = True, 
        LRU: Annotated[bool, Query(title="Least Recent Use Algorithm")] = False, 
        OPT: Annotated[bool, Query(title="Optimal Algorithm")] = False,
        base64: Annotated[bool, Query(title="Uses base64 encoded string as input")] = True,
        debug: Annotated[bool, Query(title="Includes decoded string in response")] = False
    ):

    # Validating and decoding reference string
    try:
        refStr = await validateRefString(referenceString, encoded=base64)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))

    # Create Response
    resp = dict()

    # Print string in debug mode
    if debug:
        resp["InputReferenceString"] = refStr

    # This executes the functions concurrently 
    result_keys = ["LRU", "FIFO"]
    resultLRU, resultFIFO = await asyncio.gather(
        lru(frames, refStr) if LRU else asyncio.sleep(0),
        fifo(frames, refStr) if FIFO else asyncio.sleep(0)
    )
    results = list()
    results.append(resultLRU)
    results.append(resultFIFO)
    for index, entry in enumerate(results):
        if entry:
            resp[result_keys[index]] = entry
    
    return resp
    

@app.get("/api/faults/array")
async def apiFaultsArray(
        referenceString: str, 
        maxFrames: Annotated[int, Query(title="Number of Frames", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE, 
        FIFO: Annotated[bool, Query(title="First-in-First-out Algorithm")] = True, 
        SC: Annotated[bool, Query(title="Second-Chance Algorithm")] = True, 
        LRU: Annotated[bool, Query(title="Least Recent Use Algorithm")] = False, 
        OPT: Annotated[bool, Query(title="Optimal Algorithm")] = False,
        base64: Annotated[bool, Query(title="Uses base64 encoded string as input")] = True,
        debug: Annotated[bool, Query(title="Includes decoded string in response")] = False
    ):

    # Validating and decoding reference string
    try:
        refStr = await validateRefString(referenceString)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))

    # Create Response
    resp = dict()

    # Print string in debug mode
    if debug:
        resp["InputReferenceString"] = refStr


    return resp
