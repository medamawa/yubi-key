import cv2
from cv2 import aruco
import numpy as np
import finger_utils as fu

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

def get_marker_state(state, y_history, center_y, size, threshold=1):
    # 比較対象のフレームがない場合はそのまま返す
    if y_history[0] is None:
        return state
    
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
        markers_info[marker_id]["state"] = get_marker_state(markers_info[marker_id]["state"], markers_info[marker_id]["y_history"], center_y, size)
        markers_info[marker_id]["state_history"].pop(0)
        markers_info[marker_id]["state_history"].append(markers_info[marker_id]["state"])

    return markers_info

def main():
    # マーカーの情報
    markers_info = init_markers_info()

    # マーカー種類を定義
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()

    # ArucoDetectorオブジェクトを作成
    detector = aruco.ArucoDetector(dictionary, parameters)

    # Webカメラをキャプチャ
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Webカメラが見つかりません")
        exit()

    # 入力文字の保管
    output = ""

    while True:
        # フレームを取得
        ret, frame = cap.read()
        if not ret:
            break

        # グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # マーカーを検出
        corners, ids, rejectedCandidates = detector.detectMarkers(gray)

        # マーカーを検出した場合
        if ids is not None:
            # 検出したマーカーを描画
            # frame = aruco.drawDetectedMarkers(frame, corners, ids)

            # マーカーの情報を取得
            get_markers_info(markers_info, corners, ids)
            for marker_id, info in markers_info.items():
                if not info["detected"]:
                    continue
                center_x, center_y = info["center"]
                size = info["size"]
                
                # 中心座標を描画(stateによって色を変える)0
                if (info["state"]):
                    cv2.circle(frame, (center_x, center_y), 15, (0, 255, 0), -1)
                else:
                    cv2.circle(frame, (center_x, center_y), 15, (0, 0, 255), -1)
                
                # サイズを中心座標に表示
                # cv2.putText(frame, f"[{marker_id}] {size:.2f}px ({center_x}, {center_y})", (center_x - 30, center_y - 10), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

        # フレームを水平方向に反転
        frame = cv2.flip(frame, 1)

        tmp, selecting = fu.get_output(markers_info, output)
        if tmp != "":
            output = tmp
        cv2.putText(frame, f"output: {output}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"selecting: {selecting}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)


        # フレームを表示
        cv2.imshow('frame', frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # リソースを解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
