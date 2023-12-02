from fastapi import FastAPI, HTTPException
import base64

app = FastAPI()

REF_STRING_MAX_VALUE = 12;
FRAMES_MAX_VALUE = 12;

async def validateRefString(refStr: str):
    # Decode base64 string
    refData = base64.b64decode(refStr).decode()
    refList = refData.split(",")
    # Check for Max Value
    if len(refList) > REF_STRING_MAX_VALUE:
        raise ValueError(f"Reference String is contains more than {REF_STRING_MAX_VALUE} values!")
    # Strip unnecessary spaces away
    return [d.split() for d in refList]
    

@app.get("/api/refString/")
async def apiRefString(locality: bool = False, length: int = 10):
    pass


@app.get("/api/faults/")
async def apiFaults(referenceString: str, maxFrames: int = 9, FIFO: bool = True, SC: bool = True, LRU: bool = False, OPT: bool = False):
    # Validating Input
    try:
        refStr = validateRefString(referenceString)
        if maxFrames > FRAMES_MAX_VALUE:
            raise ValueError(f"Frame Size exceeded maximum of {FRAMES_MAX_VALUE}!")
    except ValueError as v:
        raise HTTPException(status_code=404, detail=str(v))
    

@app.get("/api/faults/array")
async def apiFaultsArray(referenceString: str, Frames: int = 9, FIFO: bool = True, SC: bool = True, LRU: bool = False, OPT: bool = False):
    # Validating Input
    try:
        refStr = validateRefString(referenceString)
        if Frames > FRAMES_MAX_VALUE:
            raise ValueError(f"Frame Size exceeded maximum of {FRAMES_MAX_VALUE}!")
    except ValueError as v:
        raise HTTPException(status_code=404, detail=str(v))