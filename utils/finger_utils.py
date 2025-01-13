

def get_state_list(markers_info):
    state_list = [False] * 10
    for id, info in markers_info.items():
        state_list[id] = info["state"]
    return state_list

def get_left_id(state_list):
    if (state_list[3]) and not (state_list[2]):
        return 2
    elif (state_list[2]) and not (state_list[3]):
        return 3
    else:
        return 1

def get_right_id(state_list):
    if (state_list[5]) and not (state_list[6]):
        return 1
    elif (state_list[6]) and not (state_list[5] or state_list[7]):
        return 2
    elif (state_list[5] and state_list[6]) and not (state_list[7]):
        return 3
    elif (state_list[5] and state_list[6] and state_list[7]) and not (state_list[8]):
        return 4
    elif (state_list[6] and state_list[7]) and not (state_list[5] or state_list[8]):
        return 5
    elif (state_list[6] and state_list[7] and state_list[8]) and not (state_list[5] or state_list[9]):
        return 6
    elif (state_list[5] and state_list[6] and state_list[7] and state_list[8]) and not (state_list[9]):
        return 7
    elif (state_list[6] and state_list[7] and state_list[8] and state_list[9]) and not (state_list[5]):
        return 8
    elif (state_list[7] and state_list[8] and state_list[9]) and not (state_list[5] or state_list[6]):
        return 9
    elif (state_list[7] and state_list[8]) and not (state_list[5] or state_list[6] or state_list[9]):
        return 10
    elif state_list[5] and state_list[6] and state_list[7] and state_list[8] and state_list[9]:
        return 11
    else:
        return 0

def get_selecting_key(left_id, right_id):
    right_map_1 = {
        1: 'a', 2: 'e', 3: 'o', 4: 't', 5: 'r',
        6: 's', 7: 'u', 8: 'd', 9: 'b', 10: 'c',
        11: ' '
    }
    right_map_2 = {
        1: 'h', 2: 'i', 3: 'y', 4: 'l', 5: 'm',
        6: 'n', 7: 'w', 8: 'f', 9: 'g', 10: 'k',
        11: '.'
    }
    right_map_3 = {
        1: '\'', 2: ',', 3: '?', 4: '!', 5: '-',
        6: 'p', 7: 'v', 8: 'j', 9: 'x', 10: 'z',
        11: '\n'
    }

    if right_id == 0:
        return ''
    if left_id == 1:
        return right_map_1[right_id]   
    elif left_id == 2:
        return right_map_2[right_id]
    elif left_id == 3:
        return right_map_3[right_id]
    return ''

def key_to_id(key):
    if key == '_':
        key = ' '
    right_map_1 = {
        'a': 1, 'e': 2, 'o': 3, 't': 4, 'r': 5,
        's': 6, 'u': 7, 'd': 8, 'b': 9, 'c': 10,
        ' ': 11
    }
    right_map_2 = {
        'h': 1, 'i': 2, 'y': 3, 'l': 4, 'm': 5,
        'n': 6, 'w': 7, 'f': 8, 'g': 9, 'k': 10,
        '.': 11
    }
    right_map_3 = {
        '\'': 1, ',': 2, '?': 3, '!': 4, '-': 5,
        'p': 6, 'v': 7, 'j': 8, 'x': 9, 'z': 10,
        '\n': 11
    }
    if key in right_map_1:
        return 1, right_map_1[key]
    elif key in right_map_2:
        return 2, right_map_2[key]
    elif key in right_map_3:
        return 3, right_map_3[key]
    return 1, 0

def get_output(markers_info, output):
    selecting = ""
    state_list = get_state_list(markers_info)
    left_id = get_left_id(state_list)
    right_id = get_right_id(state_list)

    selecting = get_selecting_key(left_id, right_id)

    if not state_list[4] and markers_info[4]["state_history"][0] and not markers_info[1]["state_history"][0]:
        output += selecting
    
    if not state_list[0] and markers_info[0]["state_history"][0] and not markers_info[1]["state_history"][0]:
        if len(output) > 1:
            output = output[:-1]
        else:
            output = ""

    return output, selecting
