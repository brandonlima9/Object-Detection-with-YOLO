import cv2

def draw_detect(img, text, x1, y1, x2, y2, color=(0, 255, 0), thickness=10):
    cv2.putText(img, text, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX, 0.9, color, 2)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    return img