from pydantic import BaseModel
from enum import Enum


class ReferenceString(BaseModel):
    ReferenceString: str
    Locality: bool

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
    
class PRAlgorithm(str, Enum):
    FIFO = "FIFO"
    SC = "SC"
    LRU = "LRU"
    OPT = "OPT"

class FaultsFrame(BaseModel):
    Index: int 
    NeededPage: str
    MemoryView: list[str | None]
    PageFault: bool = False
    
class FaultsTable(BaseModel):
    PageReplaceAlgorithm: PRAlgorithm 
    MemoryTable: list[FaultsFrame]


