import random
from collections import deque


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


def fifo(frames, referenceString):
    frame_list = deque(([None] * frames), maxlen=frames)
    page_faults = 0
    for i in referenceString:
        if i not in frame_list:
            frame_list.appendleft(i)
            page_faults += 1
    return page_faults


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

            # If there are no empty frames, remove the first element in the frame list and add the element to the end of the frame list
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
