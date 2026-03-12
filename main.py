from ultralytics import YOLO

def main():

    model = YOLO("yolov8n.pt")

    model.train(
        data="dataset.yaml",
        epochs=50,
        imgsz=640,
        workers=0
    )

if __name__ == "__main__":
    main()