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

    def extract_keypoints(self, results):
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([lh, rh])

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
    model_filename = 'LargerDataset.joblib'
    predictor = HandGesturePredictor(model_filename)

    image_path = 'b.jpg'
    image = cv2.imread(image_path)

    prediction = predictor.predict(image)
    print(prediction)
    
#Cứ 100ms sẽ gửi lên 1 tấm ảnh, nhưng tôi muốn gửi ảnh khi không có sự thay đổi lớn về tay(tức là sự thay đổi của từ trong 1s thì sẽ gửi lên, chẳng hạn trên 60% thì sẽ lấy từ đó, nên cho vào 1 mảng để so sánh), có cách nào không?