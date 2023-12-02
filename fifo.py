
# Page replacement algorithm FIFO which takes the number of frames and an array of strings (reference strin) as input and returns the number of page faults.
def fifo(frames, reference_string):
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
