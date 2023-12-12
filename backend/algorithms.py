import random
from collections import deque
from response_models import FaultsMemoryFrame, FaultsMemoryView, PRAlgorithm


def refStringGen(length, localityMode):
    referenceString = ""

    N = 10 if length < 10 else length

    if localityMode:
        basePage = random.randint(0, N)

        for _ in range(length):
            if random.random() < 0.8:
                referenceString += str(basePage) + ','
            else:
                referenceString += str(random.randint(0, N)) + ','

            # Change base page sometimes
            if random.random() < 0.20:
                basePage = random.randint(0, N)
    else:
        for _ in range(length):
            referenceString += str(random.randint(0, N)) + ','

    return referenceString[:-1]


def fifo(frames : int, referenceString : list[str], memoryView = False) -> int | FaultsMemoryView :
    frameList = deque(([None] * frames), maxlen = frames)
    pageFaults = 0 

    if memoryView:
        # create list to store memory table
        memTable = []

    for i in referenceString:
        isPageFault = False
        if i not in frameList:
            frameList.appendleft(i)
            pageFaults += 1
            isPageFault = True
        
        if memoryView:
            f = FaultsMemoryFrame(
                Index = len(memTable),
                NeededPage = i,
                MemoryView = list(frameList),
                PageFault = isPageFault
            )
            memTable.append(f)

    return pageFaults if not memoryView \
        else FaultsMemoryView(PageReplaceAlgorithm = PRAlgorithm.FIFO, MemoryTable = memTable)


def lru(frames : int, referenceString : list[str], memoryView = False) -> int | FaultsMemoryView :
    pageFaults = 0
    frameList = [None] * frames

    if memoryView:
        # create list to store memory table
        memTable = []

    for page in referenceString:
        isPageFault = False

        if page not in frameList:
            pageFaults += 1
            isPageFault = True

            if None in frameList:
                frameList.pop(frameList.index(None))
            else:
                frameList.pop(len(frameList) - 1)
            frameList.insert(0, page)
        else:
            currentlyUsedPage = frameList.pop(frameList.index(page))
            frameList.insert(0, currentlyUsedPage)

        if memoryView:
            f = FaultsMemoryFrame(
                Index = len(memTable),
                NeededPage = page,
                MemoryView = frameList,
                PageFault = isPageFault
            )
            memTable.append(f)

    return pageFaults if not memoryView \
        else FaultsMemoryView(PageReplaceAlgorithm = PRAlgorithm.LRU, MemoryTable = memTable)


def opt(frames : int, referenceString : list[str], memoryView = False) -> int | FaultsMemoryView:
    pageFaults = 0
    frameList = [None] * frames

    if memoryView:
        # create list to store memory table
        memTable = []

    # Iterate through the reference string
    for i, page in enumerate(referenceString):
        isPageFault = False

        if page not in frameList:

            # If there is an empty frame, replace it
            if None in frameList:
                frameList[frameList.index(None)] = page

            else:
                max = -1
                index = -1
                # Find the page that will not be used for the longest time
                for j, p in enumerate(frameList):
                    temp = 0
                    for s in referenceString[i+1:]:
                        if s == p:
                            break
                        else:
                            temp += 1
                        if temp > max:
                            max = temp
                            index = j
                # Replace victim page with new page
                frameList[index] = page
            
            pageFaults += 1
            isPageFault = True

        if memoryView:
            f = FaultsMemoryFrame(
                Index = len(memTable),
                NeededPage = page,
                MemoryView = frameList,
                PageFault = isPageFault
            )
            memTable.append(f)
    
    return pageFaults if not memoryView \
        else FaultsMemoryView(PageReplaceAlgorithm = PRAlgorithm.OPT, MemoryTable = memTable)
