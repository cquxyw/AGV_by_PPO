import cv2

cap = cv2.VideoCapture(0)
cap.set(3,400)
cap.set(4,400)
while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('cap',frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()