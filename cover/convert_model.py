from ultralytics import YOLO

# Load your custom trained model
<<<<<<< HEAD
model = YOLO('model\ken_final.pt')

# Export to TensorRT .engine format
# model.export(format='onnx',imgsz = 320, half=True,simplify = True)
model.predict(source="Screenshot 2024-10-10 155739.png", save = True, imgsz = 640)
=======
model = YOLO('model/ken.pt')

# Export to TensorRT .engine format
model.export(format='onnx',imgsz = 640, half=True,simplify = True)
>>>>>>> a4f7f890a220c2bf2ed4fdffcf31685bfd3930d2
