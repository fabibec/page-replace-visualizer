async def lru(frames, referenceString):
    pageFaults = 0
    frameList = []
    # Create empty frames list
    for i in range(frames):
        frameList.append(None)

    # Iterate through reference string
    for i in range(len(referenceString)):

        # If reference string element is not in frames list, add it to frames list
        if referenceString[i] not in frameList:
            pageFaults += 1

            # If there is an empty frame, add the element to the first empty frame
            if None in frameList:
                frameList[frameList.index(None)] = referenceString[i]

            # If there are no emtpy frames, remove the first element in the frame list and add the element to the end of the frame list
            else:
                for j in range(len(frameList) - 1):
                    frameList[j] = frameList[j + 1]
                frameList[len(frameList)-1] = referenceString[i]

        # If reference string element is in frames list, move it to the end of the frames list
        else:

            # If there is an empty frame, move the element just before the first empty frame
            if None in frameList:
                lastElement = frameList.index(None)
                firstElement = frameList.index(referenceString[i])
                for j in range(firstElement, lastElement - 1):
                    frameList[j] = frameList[j + 1]
                frameList[lastElement-1] = referenceString[i]

            # If there are no empty frames, move the element to the end of the frames list
            else:
                frameList.remove(referenceString[i])
                frameList.append(referenceString[i])
    return pageFaults


# Page replacement algorithm FIFO which takes the number of frames and an array of strings (reference string) as input and returns the number of page faults.
async def fifo(frames, reference_string):
    page_faults = 0
    frame_list = []
    for i in range(frames):
        frame_list.append(None)
    frame_index = 0
    for i in range(len(reference_string)):
        if reference_string[i] not in frame_list:
            frame_list[frame_index] = reference_string[i]
            frame_index = (frame_index + 1) % frames
            page_faults += 1
    return page_faults
