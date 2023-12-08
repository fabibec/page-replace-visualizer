from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from typing import Annotated

from algorithms import refStringGen, fifo, lru, opt
import constants as c
from response_models import ReferenceString, Faults, FaultsArray
from validation import validateRefString

# Meta Data for documentation
tags_metadata = [
    {
        "name": "referenceString",
        "description": "#TODO Description",
    },
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
    return FileResponse("../frontend/index.html")


'''
This section handles the Backend Endpoints
'''
@app.get("/api/refString/", tags=["referenceString"], response_model=ReferenceString)
async def generate_Reference_String(
        length: Annotated[int, Query(title="The length of the Reference String", \
                                    ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE,
        locality: Annotated[bool, Query(title="Locality creates more realistic Reference String")] = True
    ):

    # Building response model
    return ReferenceString(
        ReferenceString=refStringGen(length, locality),
        Locality=locality
    )


@app.get("/api/faults/", tags=["faults"], response_model=Faults, response_model_exclude_none=True)
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


    # Building response model
    return Faults(
        InputReferenceString=refStr if debug else None,
        FIFO=fifo(frames, refStr) if FIFO else None,
        #SC=sc(frames,refStr) if SC else None
        LRU=lru(frames, refStr) if LRU else None,
        OPT=opt(frames, refStr) if OPT else None 
    )
    

@app.get("/api/faults/compareFrames", tags=["faultsArray"], response_model=FaultsArray, response_model_exclude_none=True)
async def Page_Faults_compare_Frames(
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

    # Building response model
    return FaultsArray(
        InputReferenceString=refStr if debug else None,
        FIFO = [result for result in (fifo(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))] \
            # This uses the input flag 
            if FIFO else None,
        # SC = [result for result in (sc(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))] \
        #    if SC else None,
        LRU = [result for result in (lru(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))] \
            # This uses the input flag 
            if LRU else None,
        OPT = [result for result in (opt(f, refStr) for f in range(c.FRAMES_MIN_VALUE, maxFrames + 1))] \
            # This uses the input flag 
            if OPT else None,        
    )

@app.get("/api/faults/memory")
async def Page_Faults_get_memory_view(
        referenceString: str, 
        frames: Annotated[int, Query(title="Number of Frames", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE, 
        FIFO: Annotated[bool, Query(title="First-in-First-out Algorithm")] = True, 
        SC: Annotated[bool, Query(title="Second-Chance Algorithm")] = True, 
        LRU: Annotated[bool, Query(title="Least Recent Use Algorithm")] = False, 
        OPT: Annotated[bool, Query(title="Optimal Algorithm")] = False,
        base64: Annotated[bool, Query(title="Uses base64 encoded string as input")] = True
    ):

    # Validating and decoding reference string
    try:
        refStr = await validateRefString(referenceString, encoded=base64)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))
    
    return fifo(frames, refStr, True)
