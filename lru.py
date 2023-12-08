def lru(frames, referenceString):
    pageFaults = 0
    frameList = [None] * frames

    for page in referenceString:

        if page not in frameList:
            pageFaults += 1

            if None in frameList:
                frameList.pop(frameList.index(None))

            else:
                frameList.pop(len(frameList) - 1)

            frameList.insert(0, page)

        else:
            currentlyUsedPage = frameList.pop(frameList.index(page))
            frameList.insert(0, currentlyUsedPage)

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


