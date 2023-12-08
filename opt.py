def optimal(frames, reference_string):
    page_faults = 0
    frame_list = []
    for i in range(0, frames):
        frame_list.append(None)
    for i in range(0, len(reference_string)):
        flag = False
        # Check if page is already present in frame
        for j in range(0, frames):
            if frame_list[j] == reference_string[i]:
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
                    for k in range(i + 1, len(reference_string)):
                        if frame_list[j] == reference_string[k]:
                            break
                        else:
                            temp += 1
                    if temp > max:
                        max = temp
                        index = j
            # Replace victim page with new page
            frame_list[index] = reference_string[i]
            page_faults += 1
    return page_faults


def optimalTest():
    test_frames = [3, 4, 2, 1, 7]
    test_reference_strings = [
        ['1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5'],
        ['7', '0', '1', '2', '0', '3', '0', '4', '2', '3', '0', '3', '2'],
        ['0', '1', '2', '3', '0', '4', '5', '2', '3', '2', '1', '0', '1', '7', '0', '1'],
        ['2', '3', '2', '1', '5', '2', '4', '5', '3', '2', '5', '2'],
        ['1', '2', '3', '4', '5', '7', '8', '9', '7', '8', '9', '5', '4', '5', '4', '2']
    ]
    test_expected_results = [7, 6, 11, 12, 8]
    for i in range(0, len(test_frames)):
        result = optimal(test_frames[i], test_reference_strings[i])
        print("Test", i + 1, ":", "PASS" if result == test_expected_results[i] else "FAIL")

if __name__ == '__main__':
    optimalTest()

