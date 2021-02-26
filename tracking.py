import cv2
import math
tracker = cv2.TrackerCSRT_create()
tracker1 = cv2.TrackerCSRT_create()
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

success, frame = cap.read()
bbox3 = cv2.selectROI("Tracking",frame, False)
tracker.init(frame, bbox3)

bbox13 = cv2.selectROI("Tracking",frame, False)
tracker1.init(frame, bbox13)


def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    # cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
 
while True:
    timer = cv2.getTickCount()
    success, img = cap.read()
    cv2.line(img, (int(bbox3[0] + bbox3[2]/2), int(bbox3[1] + bbox3[3]/2)), (int(bbox13[0] + bbox13[2]/2), int(bbox13[1] + bbox13[3]/2)), (0, 255, 0), thickness=2)
    success, bbox = tracker.update(img)
    success1, bbox1 = tracker1.update(img)
    # print(bbox)
 
    if success1:
        drawBox(img,bbox1)
    # else:
        # cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
    if success:
        drawBox(img,bbox)
    # else:
        # cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if success and success1:
        try:
            cv2.line(img, (int(bbox[0] + bbox[2]/2), int(bbox[1] + bbox[3]/2)), (int(bbox1[0] + bbox1[2]/2), int(bbox1[1] + bbox1[3]/2)), (0, 255, 0), thickness=2)
            cv2.putText(img, str(int(math.degrees(math.atan((bbox[1]-bbox1[1]+bbox[3]/2-bbox1[3]/2)/(bbox[0]-bbox1[0]+bbox[2]/2-bbox1[2]/2))))), (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        except:
            if (bbox[1]-bbox1[1]+bbox[3]/2-bbox1[3]/2)<0:
                cv2.putText(img, str(-90), (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(img, str(90), (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
    cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)
    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2)
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
 
 
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if fps>60: myColor = (20,230,20)
    elif fps>20: myColor = (230,20,20)
    else: myColor = (20,20,230)
    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)
 
    cv2.imshow("Tracking", img)
    key = cv2.waitKey(1)
    if key==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
