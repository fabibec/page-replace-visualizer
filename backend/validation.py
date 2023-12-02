import base64
import constants as c

async def validateRefString(refStr: str, encoded: bool):
    """Decodes and validates the reference string received by the Endpoint
    It checks the data against the thresholds defined in the constants file.
    Moreover the function cleans any empty strings that are part of the string "1,,," -> ["1"]

    Parameters
    ----------
    refStr : str
        Utf-8 encoded base64 string / string
    encoded : bool
        Flag to signal if the string is base64 encoded or not
    
        
    Returns
    -------
    refList 
        List of strings that were comma separated in the original string 
    """
    # Decode base64 string
    if encoded:
        try:
            decodedData = base64.b64decode(refStr).decode("utf-8")
        except ValueError:
            # reraise with proper message
            raise ValueError(
                f"Base64 decoding of reference string failed. Please provide an utf-8 encoded string."
            )
    else:
        decodedData = refStr
    
    # String processing
    refList = decodedData.split(",")
    refList = [d for d in refList if d.strip()]
    
    # Check for correct values
    if len(refList) > c.REF_STRING_MAX_VALUE:
        raise ValueError(
            f"Maximum length of Reference String exceeded! Allowed: {c.REF_STRING_MAX_VALUE}, current: {len(refList)}."
        )
    elif not refList:
        raise ValueError(
            f"Received string {decodedData}, which is empty."
        )
    
    return refList
