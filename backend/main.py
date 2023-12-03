from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

from algorithms import fifo, lru
import constants as c
from validation import validateRefString

# Meta Data for documentation
tags_metadata = [
    {
        "name": "faults",
        "description": "#TODO Description",
    },
    {
        "name": "faultsArray",
        "description": "#TODO Description",
    },
]


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
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata
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
    return HTMLResponse(content="static/index.html", status_code=200)

'''
This section handles the Backend Endpoints
'''
@app.get("/api/refString/")
async def generate_Reference_String(
        locality: Annotated[bool, Query(title="Locality creates more realistic Reference String")] = True,
        length: Annotated[int, Query(title="The length of the Reference String", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE
    ):
    # return {"ReferenceString" : refStr(locality, length)}
    raise NotImplementedError


@app.get("/api/faults/", tags=["faults"])
async def calculate_Page_Faults(
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

    # Execute LRU
    if LRU:
        resp["LRU"] = lru(frames, refStr)

    # Execute FIFO
    if FIFO:
        resp["FIFO"] = fifo(frames, refStr)

    # Execute OPT
    if OPT:
        # resp["OPT"] = opt(frames, refStr)
        pass

    # Execute SC
    if SC:
        # resp["SC"] = sc(frames, refStr)
        pass
    
    return resp
    

@app.get("/api/faults/array", tags=["faultsArray"])
async def calculate_Page_Faults_Array(
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
        refStr = await validateRefString(referenceString, encoded=base64)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))

    # Create Response
    resp = dict()

    # Print string in debug mode
    if debug:
        resp["InputReferenceString"] = refStr

    # Execute LRU
    if LRU:
        resp["LRU"] = \
            [result for result in (lru(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))]

    # Execute FIFO
    if FIFO:
        resp["FIFO"] = \
            [result for result in (fifo(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))]

    # Execute OPT
    if OPT:
        # resp["OPT"] = \
        # [result for result in (opt(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))]
        pass

    # Execute SC
    if SC:
        # resp["SC"] = \
        # [result for result in (sc(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))]
        pass

    return resp
