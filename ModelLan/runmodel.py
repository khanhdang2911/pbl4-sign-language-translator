import numpy as np
import cv2
import joblib
import mediapipe as mp

class HandGesturePredictor:
    def __init__(self, model_filename):
        self.model_filename = model_filename
        self.model = joblib.load(model_filename)
        self.mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def calculate_dist(self, pose):
        p1 = pose[0]
        p2 = pose[19]
        p3 = pose[20]
        dist_p1_p2 = 0 
        dist_p2_p3 = 0
        dist_p1_p3 = 0

        if p1 is not None and p2 is not None:
            dist_p1_p2 = np.linalg.norm(p1 - p2)
        if p1 is not None and p3 is not None:
            dist_p1_p3 = np.linalg.norm(p1 - p3)
        if p2 is not None and p3 is not None:
            dist_p2_p3 = np.linalg.norm(p2 - p3)
        
        return dist_p1_p2, dist_p1_p3, dist_p2_p3

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
            lh = np.zeros(21 * 3).flatten()
        
        if results.right_hand_landmarks:
            rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark])
            rh = self.hand_normalization(rh)
        else:
            rh = np.zeros(21 * 3).flatten()
        
        if results.pose_landmarks:
            pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark])
        else:
            pose = np.zeros(33 * 3)
        
        dist_lh, dist_rh, dist_p = self.calculate_dist(pose)
        lh = lh.flatten()
        rh = rh.flatten()
        dist = np.array([dist_lh, dist_rh, dist_p]).flatten()
        return np.concatenate([lh, rh, dist])

    def mediapipe_detection(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.mp_holistic.process(image_rgb)
        image_rgb.flags.writeable = True
        return results

    def predict(self, image):
        results = self.mediapipe_detection(image)
        keypoints = self.extract_keypoints(results)
        prediction = self.model.predict([keypoints])
        return prediction

if __name__ == "__main__":
    model_filename = 'model.joblib'
    predictor = HandGesturePredictor(model_filename)

    image_path = 'example_image.jpg'
    image = cv2.imread(image_path)
    prediction = predictor.predict(image)
    print(prediction)
