

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
    if (state_list[5]) and not (state_list[6] or state_list[7] or state_list[8] or state_list[9]):
        return 1
    elif (state_list[6]) and not (state_list[5] or state_list[7] or state_list[8] or state_list[9]):
        return 2
    elif (state_list[5] and state_list[6]) and not (state_list[7] or state_list[8] or state_list[9]):
        return 3
    elif (state_list[5] and state_list[6] and state_list[7]) and not (state_list[8] or state_list[9]):
        return 4
    elif (state_list[6] and state_list[7]) and not (state_list[5] or state_list[8] or state_list[9]):
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
        return 19
    else:
        return -1

def get_selecting_key(state_list):
    left_id = get_left_id(state_list)
    right_id = get_right_id(state_list)

    if left_id == 1:
        if right_id == 1:
            return 'a'
        elif right_id == 2:
            return 'e'
        elif right_id == 3:
            return 'o'
        elif right_id == 4:
            return 't'
        elif right_id == 5:
            return 'r'
        elif right_id == 6:
            return 's'
        elif right_id == 7:
            return 'u'
        elif right_id == 8:
            return 'd'
        elif right_id == 9:
            return 'b'
        elif right_id == 10:
            return 'c'
        elif right_id == 19:
            return ' '
    elif left_id == 2:
        if right_id == 1:
            return 'h'
        elif right_id == 2:
            return 'i'
        elif right_id == 3:
            return 'y'
        elif right_id == 4:
            return 'l'
        elif right_id == 5:
            return 'm'
        elif right_id == 6:
            return 'n'
        elif right_id == 7:
            return 'w'
        elif right_id == 8:
            return 'f'
        elif right_id == 9:
            return 'g'
        elif right_id == 10:
            return 'k'
        elif right_id == 19:
            return '\n'
    elif left_id == 3:
        if right_id == 1:
            return '\''
        elif right_id == 2:
            return ','
        elif right_id == 3:
            return '?'
        elif right_id == 4:
            return '!'
        elif right_id == 5:
            return '-'
        elif right_id == 6:
            return 'p'
        elif right_id == 7:
            return 'v'
        elif right_id == 8:
            return 'j'
        elif right_id == 9:
            return 'x'
        elif right_id == 10:
            return 'z'
        elif right_id == 19:
            return ''
    return ''

def get_output(markers_info, output):
    selecting = ""
    state_list = get_state_list(markers_info)

    selecting = get_selecting_key(state_list)

    if not state_list[4] and markers_info[4]["state_history"][0]:
        output += selecting
    
    if not state_list[0] and markers_info[0]["state_history"][0]:
        if len(output) > 1:
            output = output[:-1]
        else:
            output = ""

    return output, selecting
