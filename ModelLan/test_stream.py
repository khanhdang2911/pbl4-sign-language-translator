import cv2
import requests
API_URL = "http://127.0.0.1:3000/predict/"
cap = cv2.VideoCapture(0)  
frame_rate = 60  
if not cap.isOpened():
    print("Error: Cannot access the camera.")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    cv2.imshow("Video", frame)
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
    try:
        response = requests.post(API_URL, files=files)        
        if response.status_code == 200:
            prediction_data = response.json()
            print(f"Prediction: {prediction_data['prediction']}, Confidence: {prediction_data['confidence']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error occurred: {e}")

    if cv2.waitKey(33) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
