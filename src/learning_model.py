import cv2
import os
import numpy as np
import mediapipe as mp

eps = 1e-6

class HandGestureCorrection:
    def __init__(self, keypoints_path='Data/colectedkeypoints'):
        self.keypoints_path = keypoints_path
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def mediapipe_detection(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(image)
        return results

    def extract_keypoints_normalized(self, results):
        if results.left_hand_landmarks:
            left_wrist = np.array([results.left_hand_landmarks.landmark[0].x,
                                   results.left_hand_landmarks.landmark[0].y,
                                   results.left_hand_landmarks.landmark[0].z])
            left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]) - left_wrist
        else:
            left_hand = np.zeros((21, 3))

        if results.right_hand_landmarks:
            right_wrist = np.array([results.right_hand_landmarks.landmark[0].x,
                                    results.right_hand_landmarks.landmark[0].y,
                                    results.right_hand_landmarks.landmark[0].z])
            right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]) - right_wrist
        else:
            right_hand = np.zeros((21, 3))

        return np.concatenate([left_hand.flatten(), right_hand.flatten()])

    def calculate_shape_similarity(self, user_keypoints, reference_keypoints, threshold=0.05):
        errors = []
        shape_differences = []
        fingers_indices = {
            'Thumb': range(1, 5),
            'Index': range(5, 9),
            'Middle': range(9, 13),
            'Ring': range(13, 17),
            'Pinky': range(17, 21)
        }

        left_hand_user = user_keypoints[:63].reshape(21, 3)
        left_hand_ref = reference_keypoints[:63].reshape(21, 3)
        right_hand_user = user_keypoints[63:].reshape(21, 3)
        right_hand_ref = reference_keypoints[63:].reshape(21, 3)

        for hand, (user_hand, ref_hand) in zip(['Left', 'Right'], [(left_hand_user, left_hand_ref), (right_hand_user, right_hand_ref)]):
            for finger, indices in fingers_indices.items():
                user_finger_shape = np.linalg.norm(user_hand[indices] - user_hand[0], axis=1)
                ref_finger_shape = np.linalg.norm(ref_hand[indices] - ref_hand[0], axis=1)
                shape_difference = np.linalg.norm(user_finger_shape - ref_finger_shape) / max(np.linalg.norm(ref_finger_shape), eps)
                if shape_difference > threshold:
                    errors.append(f"{hand} {finger} Shape Error: {shape_difference:.2f}")
                    shape_differences.append(shape_difference)

        weights = [np.linalg.norm(ref_hand[indices] - ref_hand[0]) for finger, indices in fingers_indices.items()]
        score = 1 - np.average(shape_differences, weights=weights) if shape_differences else 1
        return score, errors

    def load_reference_keypoints(self, label):
        label_path = os.path.join(self.keypoints_path, label)
        if not os.path.exists(label_path):
            print(f"Path {label_path} does not exist.")
            return None
        for file in os.listdir(label_path):
            if file.endswith('.npy'):
                return np.load(os.path.join(label_path, file))
        print("No .npy file found in the specified folder.")
        return None

    def evaluate_image(self, image_path, label):
        reference_keypoints = self.load_reference_keypoints(label)
        if reference_keypoints is None:
            return

        image = cv2.imread(image_path)
        if image is None:
            print("Could not read the image. Please check the path.")
            return

        results = self.mediapipe_detection(image)
        user_keypoints = self.extract_keypoints_normalized(results)

        score, errors = self.calculate_shape_similarity(user_keypoints, reference_keypoints)
        
        print(f"Score: {score:.2f}")
        if errors:
            print("Errors found in the following positions:")
            for error in errors:
                print(error)
                return -1
        else:
            print("No significant errors found.")
            return score


def main():
    hand_gesture_correction = HandGestureCorrection()
    
    label = input("Enter keypoints folder label: ")
    image_path = 'image.jpg'
    
    hand_gesture_correction.evaluate_image(image_path, label)

if __name__ == "__main__":
    main()
