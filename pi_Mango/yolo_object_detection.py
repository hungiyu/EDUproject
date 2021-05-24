from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import json

# argparse為命令列指令套件
# add_argument可以指名讓我們的程式接受哪些命令列參數。
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-y", "--yolo", required=True,
                help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
                help="threshold when applying non-maxima suppression")
# vars()為讀取物件屬性以及屬性質
args = vars(ap.parse_args())

# Label
# .sep在相容作業系統上更改路徑符號
# os.path.join(path1[,path2[,.........]]) 將多個路徑組合
labelsPath = os.path.sep.join([args["yolo"], "mango.names"])
# .strip()去掉空白 .split()回傳list
LABELS = open(labelsPath).read().strip().split("\n")
# np.random.uniform()需要一起 0到255之間的亂數 回傳ndarray
# size輸出樣本數目為len(LABELS)＊3
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# load paths to the YOLO weights and configuration
weightsPath = os.path.sep.join(
    [args["yolo"], "yolov4-tiny-mango_last.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov4-tiny-mango.cfg"])

# load our YOLO object detector
print("[Dr. Farm] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# determine only the *output* layer names
# getLayerNames(): Get the name of all layers of the network.
ln = net.getLayerNames()
# getUnconnectedOutLayers()：Returns indexes of layers with unconnected outputs.
# 補充：getUnconnectedOutLayersNames()用於提取輸出圖層的名稱，yolo含有很多的圖層
# getLayerNames()可以將所有圖層的名稱提取出来。
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# warm camera
# vs = VideoStream(usePiCamera=True).start()
cap = VideoStream(src=0).start()
# time.sleep(2.0)停止兩秒後再繼續進行程式

time.sleep(2.0)
pic = [0, 0]  # for taking picture [pic_get, pic_type]
position = "unknow"  # zone
picTime = [time.time(), 0]  # [last taking picture time, the number of picture]

# with...as的用法可替代需要使用try...catch...finally的用法
with open("//home//pi//Farm_info//public//farmData.json", 'w') as obj:
    obj.write("[")

while True:
    # grab the frame from the threaded video stream and resize it
    # cap.read()會讀取一張畫面，其第一個傳回值代表成功與否，而第二個傳回值frame就是攝影機的單張畫面。
    frame = cap.read()
    # imutils.resize(img,height,width)可對圖片做等比例縮放，長寬兩者取一即可
    frame = cv2.resize(frame, (320, 240))
    # grab the frame dimensions and convert it to a blob
    # 圖片陣列中前五個為,框框的center_x,center_y,width,height,object confidence，接下來為自定義類別數
    # 因此有3個label就會為8個數值的陣列
    (H, W) = frame.shape[:2]

    # pass the blob through the network and forward network
    # cv2.dnn.blobFromImage(image[, scalefactor[, size[, mean[, swapRB[, crop[, ddepth]]]]]])
    # 對圖像進行預處理，比例縮放，裁剪，減均值，交換通道等，返回一個4通道的blob(blob可以簡單理解一個N維的數組，用於神經網路的輸入)
    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (192, 192), swapRB=True, crop=False)
    # pass the blob through the network
    net.setInput(blob)
    # forward()能取得跑完模型的結果, 方法為透過向前傳遞法，回傳資料型態為blob。
    # DNN就是把input透過超過一層的hidden layer產生計算結果能對應出output各個的機率值,即所謂feedforwarding。
    # 有兩個label,輸出為7維度
    layerOutputs = net.forward(ln)

    # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # 提取每個輸出層
    for output in layerOutputs:
        # 提取每個匡
        for detection in output:
            # extract the class ID and confidence of the current object detection
            scores = detection[5:]
            # np.argmax() Returns index_arrayndarray of ints
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected probability is greater than the minimum probability
            if confidence > args["confidence"]:
                if pic[0] == 0:
                    pic[:] = [1, 0] if classID == 0 else [
                        1, 1]  # check mango type 多於兩個label需要用switch...case...

                # 邊界框座標相對於圖像的大小進行縮放
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # 轉換出左上角座標
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences, and class IDs
                # 以下會加入所有置信度有超過的，會形成[ [],[],[].....[] ]
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    # 非最大值抑制，确定唯一边框
    # NMSBoxes(bboxes, scores, score_threshold, nms_threshold, eta=None, top_k=None)
    # bboxes:預測框尺寸，參數為[left, top, width, height]
    # scores:預測中的置信度得分
    # score_threshold：置信度閥值
    # nms_threshold：nms閥值
    idxs = cv2.dnn.NMSBoxes(
        boxes, confidences, args["confidence"], args["threshold"])

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        # flatten()返回該函數折疊為一維
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the frame
            color = [int(c) for c in COLORS[classIDs[i]]]
            # cv2.rectangle(image, start_point, end_point, color, thickness)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                       confidences[i])
            # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
            cv2.putText(frame, text, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # pic[0]=1才會儲存照片以及json檔
    if pic[0] == 1:
        # cv2.imwrite(filename, image)
        cv2.imwrite('//home//pi//Farm_info//public//images//' +
                    str(picTime[1]) + '.jpg', frame)
        print("[Dr. Farm] take a mango picture!")
        # time.time() 可以傳回從 1970/1/1 00:00:00 算起至今的秒數
        picTime[0] = time.time()
        if picTime[1] % 4 == 0:
            zone = "A"
        elif picTime[1] % 4 == 1:
            zone = "B"
        elif picTime[1] % 4 == 2:
            zone = "C"
        else:
            zone = "D"

        # time.localtime() 可以將 time.time() 所產生的秒數，轉換為 struct_time 格式的本地時間。
        # time.asctime() 函數可將 struct_time 格式的時間轉為文字
        jasonData = {"zone": zone, "picNumber": picTime[1], "type": pic[1], "time": time.asctime(
            time.localtime(picTime[0]))}
        picTime[1] += 1
        with open("//home//pi//Farm_info//public//farmData.json", 'a') as obj:
            # json.dump()將資料寫成json檔案
            json.dump(jasonData, obj)
            obj.write(",")

    if picTime[1] != 0:
        # pic[0]==0前面檢視cofidence的地方才會進去將數值改成1
        pic[0] = 0 if time.time() - picTime[0] > 10 else 2

    cv2.imshow("Output", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("okok json")
        with open("//home//pi//Farm_info//public//farmData.json", 'a') as obj:
            obj.write(" {} ] ")

        break

print("[Dr. Farm] cleanup up...")
cap.release()
cv2.destroyAllWindows()
