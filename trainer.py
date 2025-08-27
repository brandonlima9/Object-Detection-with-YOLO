from ultralytics import YOLO

# For new Training
model = YOLO("yolov8x.pt")

if __name__ == '__main__':
    results = model.train(data='ENTER DIRECTORY HERE', epochs=100)

# For resumed training
#model = YOLO("ENTER DIRECTORY HERE")

#if __name__ == '__main__':
#	results = model.train(resume=True)