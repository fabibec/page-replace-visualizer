from pydantic import BaseModel
from enum import Enum

class FaultsArray(BaseModel):
    InputReferenceString: str | None = None
    FIFO: list[int] | None = None
    SC: list[int] | None = None
    LRU: list[int] | None = None
    OPT: list[int] | None = None

class Faults(BaseModel):
    InputReferenceString: str | None = None
    FIFO: int | None = None
    SC: int | None = None
    LRU: int | None = None
    OPT: int | None = None
    
class Algorithm(str, Enum):
    FIFO = "FIFO"
    SC = "SC"
    LRU = "LRU"
    OPT = "OPT"
    
class FaultsTable(BaseModel):
    # TODO: build the response model for the memory visualization
    PageReplaceAlgorithm: Algorithm 
    MemoryTable: list[str] | None = None

