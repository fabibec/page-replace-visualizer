from fastapi import FastAPI, Request, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

import sys
sys.path.append('./backend')
from algorithms import refStringGen, fifo, lru, opt
import constants as c
from response_models import ReferenceString, Faults, FaultsRange, FaultsMemoryView, FaultsRangeItem
from validation import validateRefString, validateRange

# Meta Data for documentation
tags_metadata = [
    {
        "name": "referenceString",
        "description": "Generates a random reference string.",
    },
    {
        "name": "compareFaults",
        "description": "Compare the faults for different algorithms based on a certain number of frames.",
    },
    {
        "name": "compareFaultsRange",
        "description": "Compare Page faults between different algorithms over a specified range of frames.",
    },
    {
        "name": "memoryView",
        "description": "See how an algorithm utilizes the memory given a reference string.",
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
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class = HTMLResponse, include_in_schema= False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/visualize", response_class = HTMLResponse, include_in_schema= False)
async def visualize(request: Request):
    return templates.TemplateResponse("visualize.html", {"request": request})

@app.get("/algorithms", response_class = HTMLResponse, include_in_schema= False)
async def algorithms(request: Request):
    return templates.TemplateResponse("algorithms.html", {"request": request})

@app.get("/imprint", response_class = HTMLResponse, include_in_schema= False)
async def imprint(request: Request):
    return templates.TemplateResponse("imprint.html", {"request": request})

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request})


'''
This section handles the Backend Endpoints
'''
@app.get("/api/refString/", tags=["referenceString"], response_model=ReferenceString)
async def generate_Reference_String(
        length: Annotated[int, Query(title="The length of the Reference String", \
                                    ge=c.REF_STRING_MIN_VALUE, le=c.REF_STRING_MAX_VALUE)] = c.REF_STRING_DEFAULT_VALUE,
        locality: Annotated[bool, Query(title="Locality creates more realistic Reference String")] = True
    ):

    # Building response model
    return ReferenceString(
        ReferenceString=refStringGen(length, locality),
        Locality=locality
    )


@app.get("/api/faults/compare", tags=["compareFaults"], response_model=Faults, response_model_exclude_none=True)
async def Page_Faults_compare(
        referenceString: str,
        frames: Annotated[int, Query(title="The maximum Number of Frames", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE,
        FIFO: Annotated[bool, Query(title="First-in-First-out Algorithm")] = True,
        SC: Annotated[bool, Query(title="Second-Chance Algorithm")] = True,
        LRU: Annotated[bool, Query(title="Least Recent Use Algorithm")] = False,
        OPT: Annotated[bool, Query(title="Optimal Algorithm")] = False,
        base64: Annotated[bool, Query(title="Uses base64 encoded string as input")] = False,
        debug: Annotated[bool, Query(title="Includes decoded string in response")] = False
    ):

    # Validating and decoding reference string
    try:
        refStr = await validateRefString(referenceString, encoded=base64)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))


    # Building response model
    return Faults(
        InputReferenceString = ','.join(refStr) if debug else None,
        FIFO = fifo(frames, refStr) if FIFO else None,
        #SC=sc(frames,refStr) if SC else None
        LRU = lru(frames, refStr) if LRU else None,
        OPT = opt(frames, refStr) if OPT else None
    )


@app.get("/api/faults/compare/range", tags=["compareFaultsRange"], response_model=FaultsRange, response_model_exclude_none=True)
async def Page_Faults_compare_over_Range(
        referenceString: str,
        minFrames: Annotated[int, Query(title="Maximum number of Frames", ge=c.FRAMES_MIN_VALUE, lt=c.FRAMES_MAX_VALUE)] = c.FRAMES_MIN_VALUE,
        maxFrames: Annotated[int, Query(title="Maximum number of Frames", gt=c.FRAMES_MIN_VALUE,le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE,
        FIFO: Annotated[bool, Query(title="First-in-First-out Algorithm")] = True,
        SC: Annotated[bool, Query(title="Second-Chance Algorithm")] = True,
        LRU: Annotated[bool, Query(title="Least Recent Use Algorithm")] = False,
        OPT: Annotated[bool, Query(title="Optimal Algorithm")] = False,
        base64: Annotated[bool, Query(title="Uses base64 encoded string as input")] = False,
        debug: Annotated[bool, Query(title="Includes decoded string in response")] = False
    ):

    # Validating and decoding reference string
    try:
        refStr = await validateRefString(referenceString, encoded=base64)
        await validateRange(minFrames, maxFrames)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))

    # Building response model
    return FaultsRange(
        InputReferenceString= ','.join(refStr) if debug else None,
        FIFO = [FaultsRangeItem(Frames = f, Faults = result) \
                for f, result in enumerate((fifo(f, refStr) for f in range(minFrames, maxFrames + 1)), start = minFrames)] \
                # This uses the input flag
                if FIFO else None,
        # SC = [result for result in (sc(f, refStr) for f in range(minFrames, maxFrames + 1))] \
        #    if SC else None,
        LRU = [FaultsRangeItem(Frames = f, Faults = result) \
               for f, result in enumerate((lru(f, refStr) for f in range(minFrames, maxFrames + 1)), start = minFrames)] \
                # This uses the input flag
                if LRU else None,
        OPT = [FaultsRangeItem(Frames = f, Faults = result) \
               for f, result in enumerate((opt(f, refStr) for f in range(minFrames, maxFrames + 1)), start = minFrames)] \
                # This uses the input flag
                if OPT else None,
    )

@app.get("/api/faults/memory", tags=["memoryView"], response_model=FaultsMemoryView)
async def Page_Faults_get_memory_view(
        referenceString: str,
        frames: Annotated[int, Query(title="Number of Frames", ge=c.FRAMES_MIN_VALUE, le=c.FRAMES_MAX_VALUE)] = c.FRAMES_DEFAULT_VALUE,
        FIFO: Annotated[bool, Query(title="First-in-First-out Algorithm")] = True,
        SC: Annotated[bool, Query(title="Second-Chance Algorithm")] = False,
        LRU: Annotated[bool, Query(title="Least Recent Use Algorithm")] = False,
        OPT: Annotated[bool, Query(title="Optimal Algorithm")] = False,
        base64: Annotated[bool, Query(title="Uses base64 encoded string as input")] = False
    ):

    # Validating and decoding reference string
    try:
        refStr = await validateRefString(referenceString, encoded=base64)
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=str(ex))

    # The user checks more than one algorithm just return the first one
    if FIFO:
        return fifo(frames, refStr, True)

    if SC:
        raise NotImplementedError

    if LRU:
        return lru(frames, refStr, True)

    if OPT:
        return opt(frames, refStr, True)
