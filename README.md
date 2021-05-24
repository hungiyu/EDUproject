# EDUproject
Dr.Farm
作品集在資策會AIOT班結業時所完成的期末專題，是由團體合作的方式完成，上傳的code只有本人負責的部分，完整專案的呈現可以參考影片。  
  
我們在終端部署了兩個樹莓派，一個為自走車另一個為物件偵測，我們做到可以從本機終端來下指令控制樹莓派。  
本人負責的code部分皆部署在終端樹莓派上：  
  
1.pi_Donkeycar為部署在Donkeycar樹莓派上的程式(port設定為9000)  
2.pi_Mango為部署在物件偵測樹莓派的程式(port設定為5000)  
  
作業程序：  
1.開啟樹莓派時，同時開啟Donkeycar樹莓派上的comment.js以及物件偵測樹莓派上的server.js  
2.本機端的server連接到樹莓派port:5000/activate送出pi_Mango的active.html以及下指令開啟yolo_object_detection.py(開始物件偵測)  
3.五秒鐘後跳轉到port:9000/start送出pi_Donkeycar的index.html及下指令開啟自走車(Donkeycar啟動的python檔為官網提供)  
4.三秒鐘後跳轉到port:8887切為自走車模式(這為Donkeycar官網所提供的，要切成自動駕駛需進入此網站)  
5.以上將終端樹莓派的程式都開啟，開始作業  
6.yolo_object_detection.py會將偵測到的芒果儲存為照片及資訊儲存為Json檔  
7.當本機端連接port:5000/送出pi_Mango的page.html  
8.page.html會抓取最即時的芒果圖片以及Json檔資料呈現到網頁上  
  
  
程式：  
物件偵測:  
1.yolo_object_detection.py  
  
遠端遙控下指令以及回傳網址的部分:  
1.comment.js   
2.server.js  
  
即時呈現Json檔以及圖片的網頁:  
1.page.html  
2.farmJson.js  
  
參考資料：  
https://github.com/raghavrajmittal/yolo-object-detection 
https://github.com/eslynunez/yolo-object-detection/blob/master/yolo.py
  
  
訓練模型：  
物件偵測：使用yoloV4_tiny演算法以及darknet框架來完成芒果物件偵測的moudle，以及labelimg來匡出訓練資料  
1.環境參數：yolov4-tiny-mango.cfg  
2.訓練好的權重：yolov4-tiny-mango_last.weights  
3.classes的名稱：mango.names  
  
donkey car:使用donkey car官網所提供的套件以及步驟來完成   
1.訓練好的模型：mypilot0308_base.h5  
  
參考資料:  
https://github.com/AlexeyAB/darknet  
https://docs.donkeycar.com/  
https://wings890109.pixnet.net/blog/post/68926387-yolov4%E5%BB%BA%E7%BD%AE%E6%B5%81%E7%A8%8B  
https://wings890109.pixnet.net/blog/post/68939643-yolo-v4-%e8%be%a8%e8%ad%98%e8%87%aa%e5%ae%9a%e7%be%a9%e7%89%a9%e4%bb%b6  
