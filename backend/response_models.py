from typing_extensions import Unpack
from pydantic import BaseModel, Field
from enum import Enum
from pydantic.config import ConfigDict


class ReferenceString(BaseModel):
    ReferenceString: str = Field(description = "Generated reference string")
    Locality: bool = Field(description = "Flag if locality has been used")


class FaultsRange(BaseModel):
    InputReferenceString: str | None = Field(default = None, description = "Returned if debug flag is set")
    FIFO: list[int] | None = Field(default = None, description = "Range of page faults for FIFO")
    SC: list[int] | None = Field(default = None, description = "Range of page faults for SC")
    LRU: list[int] | None = Field(default = None, description = "Range of page faults for LRU")
    OPT: list[int] | None = Field(default = None, description = "Range of page faults for OPT")


class Faults(BaseModel):
    InputReferenceString: str | None = Field(default = None, description = "Returned if debug flag is set")
    FIFO: int | None = Field(default = None, description = "Page faults for FIFO")
    SC: int | None = Field(default = None, description = "Page faults for SC")
    LRU: int | None = Field(default = None, description = "Page faults for LRU")
    OPT: int | None = Field(default = None, description = "Page faults for OPT")


class PRAlgorithm(str, Enum):
    FIFO = "FIFO"
    SC = "SC"
    LRU = "LRU"
    OPT = "OPT"


class FaultsMemoryFrame(BaseModel):
    Index: int = Field(description = "Index of current frame")
    NeededPage: str = Field(description = "Page that should be accessed in the current Frame")
    MemoryView: list[str | None] = Field(description = "Current allocation of the memory")
    PageFault: bool = Field(default = False, description = "Flag if a page fault occurred in current frame")


class FaultsMemoryFrameSC(FaultsMemoryFrame):
    CursorPosition: int = Field(description = "Position of the SC cursor after performing the current operation")
    ModifiedBit: int = Field(description = "Value of the modified bit")

   
class FaultsMemoryView(BaseModel):
    PageReplaceAlgorithm: PRAlgorithm = Field(description = "Name of the page replacement algorithm used")
    MemoryTable: list[FaultsMemoryFrame] = Field(description = "List of the memory frames")


