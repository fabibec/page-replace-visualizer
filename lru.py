
def lru(frames, referenceString):
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


def lruTest():
    test_frames = [3, 4, 5]
    test_referenceStrings = [
                ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5'],
                ['7', '0', '3', '2', '1', '2', '0', '1', '7', '0', '1'],
                ['2', '3', '2', '1', '5', '2', '4', '5', '3', '2', '5', '2']
            ]
    expected_results = [10, 6, 5]

    for i in range(len(test_frames)):
        result = lru(test_frames[i], test_referenceStrings[i])
        print("Test", i + 1, ":", "PASS" if result == expected_results[i] else "FAIL")



if __name__ == "__main__":
    lruTest()


