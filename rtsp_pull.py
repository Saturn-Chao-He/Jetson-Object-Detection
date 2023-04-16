import cv2

cap = cv2.VideoCapture("rtsp://192.168.8.115:8554/live")
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ret, frame = cap.read()
while (ret):
    ret, frame = cap.read()
    cv2.imshow("cam0", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()