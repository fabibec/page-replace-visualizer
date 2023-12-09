def fifo(frames, reference_string):
    from collections import deque
    frame_list = deque(([None] * frames), maxlen=frames)
    page_faults = 0
    for i in reference_string:
        if i not in frame_list:
            frame_list.appendleft(i)
            page_faults += 1
    return page_faults

def fifoTest():
    test_frames = [3, 4, 5, 6]
    test_referenceStrings = [
                ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5'],
                ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5'],
                ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5'],
                ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5']
            ]
    expected_results = [9, 10, 5, 5]
    for i in range(0, len(test_frames)):
        result = fifo(test_frames[i], test_referenceStrings[i])
        print("Test", i+1, ":", "PASS" if result == expected_results[i] else "FAIL")

if __name__ == '__main__':
    fifoTest()
