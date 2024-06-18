from ultralytics import YOLO
from ultralytics import YOLOWorld
import cv2
from collections import defaultdict
import numpy as np

cap = cv2.VideoCapture(0)

model = YOLO("../yolov8n.pt") #modelo base yolo
#model = YOLO("C:/Users/loren/Desktop/processamento de imagens/runs/detect/train10/weights/best.pt") #modelo treinado pro mim

track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = True

while True:
    success, img = cap.read()

    if success:
        if seguir:
            results = model.track(img, persist=True)
        else:
            results = model(img)

        # Process results list
        for result in results:
            # Visualize the results on the frame
            img = result.plot()

            if seguir and deixar_rastro:
                try:
                    # Get the boxes and track IDs
                    boxes = result.boxes.xywh.cpu()
                    track_ids = result.boxes.id.int().cpu().tolist()

                    # Plot the tracks
                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = track_history[track_id]
                        track.append((float(x), float(y)))  # x, y center point
                        if len(track) > 30:  # retain 90 tracks for 90 frames
                            track.pop(0)

                        # Draw the tracking lines
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(img, [points], isClosed=False, color=(230, 0, 0), thickness=5)
                except:
                    pass

        cv2.imshow("Tela", img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("desligando")