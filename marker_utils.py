import numpy as np

def init_markers_info():
    markers_info = {}

    for i in range(10):
        markers_info[i] = {
            "corners": [],
            "center": (None, None),
            "y_history": [None, None, None, None, None],
            "size": None,
            "detected": False,
            "state": False,
            "state_history": [False, False]
        }
    
    return markers_info

def get_marker_state(state, y_history, center_y, size, id, threshold=1):
    # 比較対象のフレームがない場合はそのまま返す
    if y_history[0] is None:
        return state
    
    if id == 0 or id == 1 or id == 4 or id == 5 or id == 8 or id == 9:
        threshold *= 0.5
    
    if y_history[0] - size * threshold > center_y:
        return True
    elif y_history[0] + size * threshold < center_y:
        return False
    else:
        return state

def get_markers_info(markers_info, corners, ids):
    flat_ids = ids.flatten()

    for num in range(10):
        if num not in flat_ids:
            markers_info[num]["corners"] = []
            markers_info[num]["center"] = (None, None)
            markers_info[num]["y_history"].pop(0)
            markers_info[num]["y_history"].append(None)
            markers_info[num]["size"] = None
            markers_info[num]["detected"] = False
            markers_info[num]["state_history"].pop(0)
            markers_info[num]["state_history"].append(markers_info[num]["state"])

    for i, corner in enumerate(corners):
        marker_id = flat_ids[i]  # マーカーID
        if marker_id > 9:
            continue
        
        # 各マーカーの隅の座標
        corner_points = corner[0]
        
        # 中心座標を計算
        center_x = np.mean(corner_points[:, 0])
        center_y = np.mean(corner_points[:, 1])

        # サイズを計算
        edge_lengths = [
            np.linalg.norm(corner_points[0] - corner_points[1]),  # 左上 → 右上
            np.linalg.norm(corner_points[1] - corner_points[2]),  # 右上 → 右下
            np.linalg.norm(corner_points[2] - corner_points[3]),  # 右下 → 左下
            np.linalg.norm(corner_points[3] - corner_points[0])   # 左下 → 左上
        ]
        size = np.mean(edge_lengths)
        
        # 情報を辞書に格納
        markers_info[marker_id]["corners"] = corner_points.tolist()
        markers_info[marker_id]["center"] = (int(center_x), int(center_y))
        markers_info[marker_id]["y_history"].pop(0)
        markers_info[marker_id]["y_history"].append(center_y)
        markers_info[marker_id]["size"] = size
        markers_info[marker_id]["detected"] = True
        markers_info[marker_id]["state"] = get_marker_state(markers_info[marker_id]["state"], markers_info[marker_id]["y_history"], center_y, size, marker_id)
        markers_info[marker_id]["state_history"].pop(0)
        markers_info[marker_id]["state_history"].append(markers_info[marker_id]["state"])

    return markers_info
