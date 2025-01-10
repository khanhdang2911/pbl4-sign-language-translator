from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import joblib
import torch
import mediapipe as mp
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from torch import nn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class HandGesturePredictor:
    def __init__(self, model_filename, scaler_filename, label_encoder_filename):
        self.model = self.load_model(model_filename)
        self.model.eval()
        self.scaler = joblib.load(scaler_filename)
        self.label_encoder = joblib.load(label_encoder_filename)
        self.mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def load_model(self, model_filename):
        import torch.nn as nn

        class DeepNet(nn.Module):
            def __init__(self, input_size, num_classes):
                super(DeepNet, self).__init__()
                self.network = nn.Sequential(
                    nn.Linear(input_size, 512),      # Input -> 512
                    nn.BatchNorm1d(512),
                    nn.ReLU(),
                    nn.Dropout(0.3),

                    nn.Linear(512, 1024),            # 512 -> 1024
                    nn.BatchNorm1d(1024),
                    nn.ReLU(),
                    nn.Dropout(0.4),

                    nn.Linear(1024, 512),            # 1024 -> 512
                    nn.BatchNorm1d(512),
                    nn.ReLU(),
                    nn.Dropout(0.4),

                    nn.Linear(512, 256),             # 512 -> 256
                    nn.BatchNorm1d(256),
                    nn.ReLU(),
                    nn.Dropout(0.3),

                    nn.Linear(256, 128),             # 256 -> 128
                    nn.BatchNorm1d(128),
                    nn.ReLU(),
                    nn.Dropout(0.3),

                    nn.Linear(128, 64),              # 128 -> 64
                    nn.BatchNorm1d(64),
                    nn.ReLU(),
                    nn.Dropout(0.2),

                    nn.Linear(64, num_classes)       # 64 -> Output (num_classes)
                )

            def forward(self, x):
                return self.network(x)


        input_size = 21 * 3 * 2 + 2  # Feature size: 2 hands (21 landmarks * 3 coords) + distances
        num_classes = len(joblib.load("label_encoder.pkl").classes_)
        model = DeepNet(input_size, num_classes)
        model.load_state_dict(torch.load(model_filename, map_location=device))
        return model.to(device)

    def calculate_dist(self, pose):
        p1 = pose[0]
        p2 = pose[19]
        p3 = pose[20]
        dist_p1_p2 = 0 
        # dist_p2_p3 = 0
        dist_p1_p3 = 0

        if p1 and p2:
            dist_p1_p2 = np.linalg.norm(p1-p2)
        if p1 and p3: 
            dist_p1_p3 = np.linalg.norm(p1-p3)
        # if p2 and p3:
        #     dist_p2_p3 = np.linalg.norm(p2-p3)
        
        return dist_p1_p2, dist_p1_p3


    def hand_normalization(self, hand):
        origin = hand[0]
        hand -= origin
        min_val = hand.min(axis=0)
        max_val = hand.max(axis=0)
        range_val = max_val - min_val
        hand = (hand - min_val) / (range_val + 1e-6)
        return hand

    def extract_keypoints(self, results):
        if results.left_hand_landmarks:
            lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark])
            lh = self.hand_normalization(lh)
        else:
            lh = np.zeros(21*3).flatten()
        if results.right_hand_landmarks:
            rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark])
            rh = self.hand_normalization(rh)
        else:
            rh = np.zeros(21*3)
        
        if results.pose_landmarks:
            pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten()
        else:
            pose = np.zeros(33*3)
        dist_lh, dist_rh = self.calculate_dist(pose)
        lh = lh.flatten()
        rh = rh.flatten()
        dist = np.array([dist_lh, dist_rh]).flatten()
        return np.concatenate([ lh, rh, dist])

    def mediapipe_detection(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.mp_holistic.process(image_rgb)
        image_rgb.flags.writeable = True
        return results


    def preprocess_keypoints(self, keypoints):
        keypoints = self.scaler.transform([keypoints])
        return torch.tensor(keypoints, dtype=torch.float32).to(device)

    def predict(self, image):
        results = self.mediapipe_detection(image)
        keypoints = self.extract_keypoints(results)
        preprocessed_keypoints = self.preprocess_keypoints(keypoints)
        with torch.no_grad():
            outputs = self.model(preprocessed_keypoints)
            _, predicted = outputs.max(1)
            confidence = nn.functional.softmax(outputs, dim=1)[0][predicted].item()
            prediction = self.label_encoder.inverse_transform(predicted)[0]


        return prediction, confidence


model_filename = "model.pth"
scaler_filename = "scaler.pkl"
label_encoder_filename = "label_encoder.pkl"
predictor = HandGesturePredictor(model_filename, scaler_filename, label_encoder_filename)


@app.get("/")
async def read_root():
    return {"message": "Hand Gesture Recognition API is running."}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    prediction, confidence = predictor.predict(image)
    return JSONResponse(content={"prediction": prediction, "confidence": float(confidence)})
