import random
from collections import deque
from response_models import FaultsMemoryFrame, FaultsMemoryView, PRAlgorithm


def refStringGen(length, locality_mode):
    reference_string = ""

    N = 10 if length < 10 else length

    if locality_mode:
        base_page = random.randint(0, N)

        for _ in range(length):
            if random.random() < 0.8:
                reference_string += str(base_page) + ','
            else:
                reference_string += str(random.randint(0, N)) + ','

            # Change base page sometimes
            if random.random() < 0.20:
                base_page = random.randint(0, N)
    else:
        for _ in range(length):
            reference_string += str(random.randint(0, N)) + ','

    return reference_string[:-1]


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


# New version will be used after @masterYoda8's review
def opt(frames, referenceString):
    page_faults = 0
    frame_list = []
    for i in range(0, frames):
        frame_list.append(None)
    for i in range(0, len(referenceString)):
        flag = False
        # Check if page is already present in frame
        for j in range(0, frames):
            if frame_list[j] == referenceString[i]:
                flag = True
                break
        # Find victim page
        if flag == False:
            max = -1
            index = -1
            for j in range(0, frames):
                # If frame is empty, replace it
                if frame_list[j] == None:
                    index = j
                    break
                else:
                    temp = 0
                    for k in range(i + 1, len(referenceString)):
                        if frame_list[j] == referenceString[k]:
                            break
                        else:
                            temp += 1
                    if temp > max:
                        max = temp
                        index = j
            # Replace victim page with new page
            frame_list[index] = referenceString[i]
            page_faults += 1
    return page_faults
