import time
from tkinter import ttk
import cv2
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import requests
from tkVideoPlayer import TkinterVideo
from tkinter import filedialog
import os  # them thu vien os de check file ton tai
import random #random quiz
from model import HandGesturePredictor
from learning_model import HandGestureCorrection
# Thêm imports cần thiết ở đầu file

# Khởi tạo predictor
model_filename = 'LargerDataset.joblib'
predictor = HandGesturePredictor(model_filename)
correction = HandGestureCorrection()
predictions_array = []  # Mảng lưu các dự đoán
last_update_time = time.time()  # Thời điểm cập nhật cuối
last_hand_positions = None  # Vị trí tay ở frame trước
PREDICTION_THRESHOLD = 0.6  # Ngưỡng tin cậy (60%)
MOVEMENT_THRESHOLD = 0.1  # Ngưỡng thay đổi vị trí tay (10%)
last_prediction_time = time.time()  # Thời điểm dự đoán cuối



# Create the main window
root = tk.Tk()
root.title("Sign Language Translator & Learning")
root.geometry("900x750+290+10")

# Set the application icon
image_icon = PhotoImage(file="../assets/images/logo.png")
root.iconphoto(False, image_icon)

# Define functions to switch between frames
def show_home_frame():
    home_frame.tkraise()

def show_video_frame():
    video_frame.tkraise()

def show_vocab_frame():
    vocab_frame.tkraise()

def show_quiz_frame():
    quiz_frame.tkraise()
    
    # Chọn từ đúng
    global random_word
    random_word = random.choice(words)
    
    # Tạo danh sách các từ sai (không bao gồm từ đúng)
    wrong_words = [word for word in words if word != random_word]
    # Chọn ngẫu nhiên 3 từ sai
    incorrect_words = random.sample(wrong_words, 3)
    
    # Tạo list chứa cả 4 từ (1 đúng + 3 sai)
    all_options = [random_word] + incorrect_words
    # Xáo trộn vị trí các từ
    random.shuffle(all_options)
    
    # Cập nhật text và value cho 4 radio buttons
    quiz_option_1.config(text=all_options[0], value=all_options[0])
    quiz_option_2.config(text=all_options[1], value=all_options[1])
    quiz_option_3.config(text=all_options[2], value=all_options[2])
    quiz_option_4.config(text=all_options[3], value=all_options[3])
    
    # Reset instruction text và radio button selection
    quiz_instruction_label.config(text="Select the correct word for the video shown:")
    quiz_option_var.set(None)
    
    # Load và play video
    quiz_vid_player.load(f"../assets/videos/{random_word}.mp4")
    quiz_vid_player.play()


# Main frame
main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill="both", expand=True)

# Home Frame
home_frame = tk.Frame(main_frame, bg="#FFFFFF")
home_frame.place(relwidth=1, relheight=1)

# Header Section
header_frame = tk.Frame(home_frame, bg="#4CAF50")
header_frame.pack(fill="x")

# Add App Image in Header
app_image = Image.open("../assets/images/logo.png")  # Load your app logo
app_image = app_image.resize((100, 100), Image.LANCZOS)  # Resize the image if necessary
app_logo = ImageTk.PhotoImage(app_image)

logo_label = tk.Label(header_frame, image=app_logo, bg="#4CAF50")
logo_label.pack(side=tk.LEFT, padx=10)

title_label = tk.Label(header_frame, text="Sign Language Translation & Learning", font=("Arial", 24, "bold"), bg="#4CAF50", fg="#fff")
title_label.pack(pady=20)
# Button Section
button_frame = tk.Frame(home_frame, bg="#FFFFFF")
button_frame.pack(pady=30)

# Create Buttons with Icons (Optional)
btn1 = tk.Button(button_frame, text="Translate Sign Language", font=("Arial", 16, "bold"), bg="#4CAF50", fg="#fff", command=show_video_frame)
btn1.pack(pady=10, padx=20, fill="x")

btn2 = tk.Button(button_frame, text="Learn Sign Language", font=("Arial", 16, "bold"), bg="#2196F3", fg="#fff", command=show_vocab_frame)
btn2.pack(pady=10, padx=20, fill="x")

btn_quiz = tk.Button(button_frame, text="Vocabulary Quiz", font=("Arial", 16, "bold"), bg="#FF5722", fg="#fff", command=show_quiz_frame)
btn_quiz.pack(pady=10, padx=20, fill="x")

# Footer Section (optional)
footer_frame = tk.Frame(home_frame, bg="#f5f5f5")
footer_frame.pack(side="bottom", fill="x")

footer_label = tk.Label(footer_frame, text="© 2024 Sign Language Learning App. All Rights Reserved.", font=("Arial", 10), bg="#f5f5f5", fg="#333")
footer_label.pack(pady=10)

# Keep a reference to the image to avoid garbage collection
logo_label.image = app_logo


# Add some padding around the main frame
home_frame.pack_propagate(False)  # Prevent frame from resizing to fit contents


# Video Frame
video_frame = tk.Frame(main_frame, bg="#f5f5f5")
video_frame.place(relwidth=1, relheight=1)

top_frame = tk.Frame(video_frame, bg="#f5f5f5")
top_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

lower_frame = tk.Frame(video_frame, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)

vid_player = TkinterVideo(video_frame, scaled=True)
vid_player.pack(expand=True, fill="both", padx=10, pady=10)

text_box = tk.Text(video_frame, height=5, width=80, font=("Arial", 16,"bold"), fg="#333", bg="#f5f5f5")
text_box.pack(pady=10, fill="x")
text_box.insert("1.0", "This is a text box to display text below the video.")

video_label = tk.Label(vid_player)
video_label.pack()


def calculate_hand_movement(current_results, last_positions):
    if last_positions is None:
        return 1.0  # Trả về giá trị lớn để chắc chắn xử lý frame đầu tiên
    
    # Lấy landmarks của tay hiện tại
    current_positions = []
    if current_results.left_hand_landmarks:
        for landmark in current_results.left_hand_landmarks.landmark:
            current_positions.extend([landmark.x, landmark.y, landmark.z])
    if current_results.right_hand_landmarks:
        for landmark in current_results.right_hand_landmarks.landmark:
            current_positions.extend([landmark.x, landmark.y, landmark.z])
            
    if not current_positions:
        return 1.0  # Không phát hiện tay trong frame hiện tại
        
    current_positions = np.array(current_positions)
    
    # Tính toán sự thay đổi vị trí trung bình
    movement = np.mean(np.abs(current_positions - last_positions))
    return movement
# Video recording control variable
recording = False

def calculate_hand_movement(current_results, last_positions):
    if last_positions is None:
        return 1.0  # Trả về giá trị lớn để chắc chắn xử lý frame đầu tiên
    
    # Lấy landmarks của tay hiện tại
    current_positions = []
    hand_count = 0
    
    if current_results.left_hand_landmarks:
        for landmark in current_results.left_hand_landmarks.landmark:
            current_positions.extend([landmark.x, landmark.y, landmark.z])
        hand_count += 1
            
    if current_results.right_hand_landmarks:
        for landmark in current_results.right_hand_landmarks.landmark:
            current_positions.extend([landmark.x, landmark.y, landmark.z])
        hand_count += 1
            
    if not current_positions:
        return 1.0  # Không phát hiện tay trong frame hiện tại
        
    current_positions = np.array(current_positions)
    
    # Nếu số lượng tay phát hiện được khác với frame trước
    if len(current_positions) != len(last_positions):
        return 1.0
    
    # Tính toán sự thay đổi vị trí trung bình
    try:
        movement = np.mean(np.abs(current_positions - last_positions))
        return movement
    except:
        return 1.0

def update_video_frame():
    global recording, cap, predictor, text_box, resultPredict
    
    # Khởi tạo mảng dự đoán cho mỗi giây
    if not hasattr(update_video_frame, 'predictions'):
        update_video_frame.predictions = []
        update_video_frame.last_time = time.time()
    
    if recording:
        ret, frame = cap.read()
        if ret:
            # Hiển thị frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            
            current_time = time.time()
            
            # Thực hiện dự đoán mỗi 100ms
            try:
                prediction = predictor.predict(frame)[0]  # Lấy kết quả dự đoán
                update_video_frame.predictions.append(prediction)
            except Exception as e:
                print(f"Prediction error: {e}")
            
            # Mỗi 1 giây, phân tích kết quả
            if current_time - update_video_frame.last_time >= 1.0:
                if update_video_frame.predictions:
                    # Đếm số lần xuất hiện của mỗi từ
                    word_counts = {}
                    total_predictions = len(update_video_frame.predictions)
                    
                    for word in update_video_frame.predictions:
                        word_counts[word] = word_counts.get(word, 0) + 1
                    
                    # Tìm từ có tỷ lệ xuất hiện cao nhất
                    max_word = None
                    max_confidence = 0
                    
                    for word, count in word_counts.items():
                        confidence = count / total_predictions
                        if confidence > max_confidence:
                            max_confidence = confidence
                            max_word = word
                    
                    # Nếu từ xuất hiện trên 60% trong 1s, lưu kết quả và hiển thị
                    if max_confidence >= 0.6:
                        # Lưu kết quả vào resultPredict
                        resultPredict.append({
                            'word': max_word,
                            'confidence': max_confidence
                        })
                        
                        # Hiển thị kết quả hiện tại
                        result_text = (
                            f"Predicted Word: {max_word}\n"
                            f"Confidence: {max_confidence*100:.2f}%\n"
                            f"Total predictions: {total_predictions}"
                        )
                        text_box.delete("1.0", "end")
                        text_box.insert("1.0", result_text)
                
                # Reset cho chu kỳ mới
                update_video_frame.predictions = []
                update_video_frame.last_time = current_time
            
            video_label.after(100, update_video_frame)  # Cập nhật mỗi 100ms
            
def record_video():
    global cap, recording, predictor, last_update_time, last_hand_positions, last_prediction_time, predictions_array, resultPredict, last_hand_count
    cap = cv2.VideoCapture(0)
    recording = True
    
    predictions_array = []
    resultPredict = []  # Reset mảng resultPredict khi bắt đầu record mới
    last_update_time = time.time()
    last_hand_positions = None
    last_hand_count = 0
    last_prediction_time = time.time()
    
    model_filename = 'LargerDataset.joblib'
    predictor = HandGesturePredictor(model_filename)
    
    update_video_frame()

def stop_recording():
    global recording, cap, last_hand_positions, last_hand_count
    recording = False
    last_hand_positions = None
    last_hand_count = 0
    if cap is not None:
        cap.release()
    
    if resultPredict:
        filtered_results = []
        last_word = None
        predicted_words = []  # Mảng chứa các từ để gửi lên API
        
        # Lọc các kết quả, chỉ giữ lại khi có sự thay đổi từ
        for result in resultPredict:
            current_word = result['word']
            if last_word is None or current_word != last_word:
                filtered_results.append(result)
                predicted_words.append(current_word)  # Thêm từ vào mảng để gửi lên API
                last_word = current_word
        
        # Gọi API để sửa ngữ nghĩa
        try:
            # Chuẩn bị data để gửi lên API
            api_data = {
                "text_voice": predicted_words
            }
            
            # Gọi API
            response = requests.post('http://localhost:8081/home/create-text-voice', json=api_data)
            
            if response.status_code == 200:
                # Parse JSON response
                api_response = response.json()
                
                if api_response.get('success'):
                    # Hiển thị cả kết quả dự đoán và câu đã sửa
                    text_output = "Recording stopped.\nPredicted words with high confidence:\n\n"
                    for result in filtered_results:
                        text_output += f"Word: {result['word']}, Confidence: {result['confidence']*100:.2f}%\n"
                    
                    text_output += f"\nCorrected sentence:\n{api_response['message']}"
                    
                    text_box.delete("1.0", "end")
                    text_box.insert("1.0", text_output)
                else:
                    text_box.delete("1.0", "end")
                    text_box.insert("1.0", "Error in sentence correction.")
                    
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi khi gọi API
            text_output = "Recording stopped.\nPredicted words with high confidence:\n\n"
            for result in filtered_results:
                text_output += f"Word: {result['word']}, Confidence: {result['confidence']*100:.2f}%\n"
            
            text_output += f"\nError connecting to correction service: {str(e)}"
            text_box.delete("1.0", "end")
            text_box.insert("1.0", text_output)
            
    else:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "Recording stopped. No reliable predictions were made.")


class PracticeWindow:
    def __init__(self, word):
        self.word = word
        self.root = tk.Toplevel()
        self.root.title(f"Practice '{word.capitalize()}'")
        self.root.geometry("900x700")
        
        # Khởi tạo HandGestureCorrection
        self.hand_gesture_correction = correction
        
        # Khởi tạo biến
        self.recording = False
        self.cap = None
        self.practice_attempts = []
        self.last_update_time = time.time()
        self.last_evaluation_time = time.time()
        
        # Tạo giao diện
        self.create_widgets()

        
    def create_widgets(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tiêu đề
        title = ttk.Label(main_frame, 
                         text=f"Practice '{self.word.capitalize()}'", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Frame video tham khảo
        ref_frame = ttk.LabelFrame(main_frame, text="Reference Video", padding="5")
        ref_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.vid_player = TkinterVideo(ref_frame, scaled=True)
        self.vid_player.grid(row=0, column=0, sticky="nsew")
        self.vid_player.load(f"../assets/videos/{self.word}.mp4")
        self.vid_player.play()
        
        # Frame camera practice
        practice_frame = ttk.LabelFrame(main_frame, text="Your Practice", padding="5")
        practice_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        self.video_label = ttk.Label(practice_frame)
        self.video_label.grid(row=0, column=0, sticky="nsew")
        
        # Frame điều khiển
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(control_frame, 
                                  text="Start Practice",
                                  command=self.start_practice)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, 
                                 text="Stop Practice",
                                 command=self.stop_practice)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Frame kết quả
        self.result_label = ttk.Label(main_frame, 
                                    text="Start practicing to get feedback",
                                    font=("Arial", 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Cấu hình grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def start_practice(self):
        self.cap = cv2.VideoCapture(0)
        self.recording = True
        self.predictions_array = []
        self.last_update_time = time.time()
        self.last_hand_positions = None
        self.last_prediction_time = time.time()
        self.update_practice_frame()
        
    def stop_practice(self):
        self.recording = False
        if self.cap is not None:
            self.cap.release()
        self.result_label.config(text="Practice stopped")
        
    def update_practice_frame(self):
        if self.recording:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((600, 450))  # Resize để phù hợp với giao diện
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                
                # Xử lý đánh giá cử chỉ tay
                current_time = time.time()
                if current_time - self.last_evaluation_time >= 1.0:  # Đánh giá mỗi giây
                    try:
                        # Kiểm tra kết quả MediaPipe
                        results = self.hand_gesture_correction.mediapipe_detection(frame)
                        
                        # Kiểm tra xem có hand landmarks không
                        if results.left_hand_landmarks or results.right_hand_landmarks:
                            print("Hand landmarks detected!")
                            
                            # Trích xuất keypoints
                            user_keypoints = self.hand_gesture_correction.extract_keypoints_normalized(results)
                            
                            # Tải keypoints tham chiếu
                            reference_keypoints = self.hand_gesture_correction.load_reference_keypoints(self.word)
                            
                            if reference_keypoints is not None:
                                # Đánh giá độ tương đồng
                                score, errors = self.hand_gesture_correction.calculate_shape_similarity(
                                    user_keypoints, 
                                    reference_keypoints
                                )
                                
                                print(f"Score: {score}")
                                
                                if errors:
                                    # Có lỗi trong cử chỉ tay
                                    print("Errors detected:", errors)
                                    self.result_label.config(
                                        text="Incorrect hand gesture. Try again!",
                                        foreground="red"
                                    )
                                else:
                                    # Cử chỉ tay chính xác
                                    print("Correct hand gesture!")
                                    self.result_label.config(
                                        text=f"Good job! Accuracy: {score*100:.2f}%",
                                        foreground="green"
                                    )
                            else:
                                print(f"No reference keypoints found for word: {self.word}")
                        else:
                            print("No hand landmarks detected")
                            self.result_label.config(
                                text="No hand landmarks detected",
                                foreground="red"
                            )
                        
                        self.last_evaluation_time = current_time
                    
                    except Exception as e:
                        print(f"Evaluation error: {e}")
                
            self.video_label.after(10, self.update_practice_frame)
# Thêm function để tạo nút Practice trong word buttons
def create_word_button_with_practice(parent, word, command):
    frame = ttk.Frame(parent)
    frame.pack(pady=5, anchor='w')
    
    word_btn = ttk.Button(frame, text=word, command=command, width=12)
    word_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    practice_btn = ttk.Button(
        frame,
        text="Practice",
        command=lambda: PracticeWindow(word),
        width=8
    )
    practice_btn.pack(side=tk.LEFT)
    
    return frame

# Cập nhật hàm update_word_list để sử dụng button mới
def update_word_list(category):
    for button in word_buttons:
        button.pack_forget()
    
    if category == "alphabet":
        words_to_display = ["a", "b", "c", "d", "o","u","v","y"]
    elif category == "verbs":
        words_to_display = ["eat", "drink", "go", "have", "read", "write", "love", "open", 
                           "play", "learn", "please","thank you", "use"]
    elif category == "nouns":
        words_to_display = ["book", "water", "phone", "house", "school", "money", "me"]

    for word in words_to_display:
        button_frame = create_word_button_with_practice(
            sub_frame,
            word,
            lambda w=word: play_vocab_video(w)
        )
        word_buttons.append(button_frame)

# Video control buttons in Video Frame
record_btn = tk.Button(top_frame, text="Record Video", bg="#4CAF50", font=("Arial", 12, "bold"), fg="#fff", command=record_video)
record_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(top_frame, text="Stop Recording", bg="#FF0000", font=("Arial", 12, "bold"), fg="#fff", command=stop_recording)
stop_btn.pack(side=tk.LEFT, padx=5)

back_to_home_btn = tk.Button(video_frame, text="Back to Home", bg="#FFFFFF", font=("Arial", 12, "bold"), fg="#333", command=show_home_frame)
back_to_home_btn.pack(side=tk.BOTTOM, pady=10)

# Vocabulary Frame
vocab_frame = tk.Frame(main_frame, bg="#f5f5f5")
vocab_frame.place(relwidth=1, relheight=1)

# Vocabulary Learning Section (under "Learn Sign Language")
vocab_title = tk.Label(vocab_frame, text="Learn Sign Language - Vocabulary", font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333")
vocab_title.pack(pady=20)

category_frame = tk.Frame(vocab_frame, bg="#f0f0f0")
category_frame.pack(fill="x", pady=10)

alphabet_btn = tk.Button(category_frame, text="Alphabet", font=("Arial", 14), bg="#03A9F4", fg="#fff", command=lambda: update_word_list("alphabet"))
alphabet_btn.pack(side=tk.LEFT, padx=10)

verbs_btn = tk.Button(category_frame, text="Verbs", font=("Arial", 14), bg="#03A9F4", fg="#fff", command=lambda: update_word_list("verbs"))
verbs_btn.pack(side=tk.LEFT, padx=10)

nouns_btn = tk.Button(category_frame, text="Nouns", font=("Arial", 14), bg="#03A9F4", fg="#fff", command=lambda: update_word_list("nouns"))
nouns_btn.pack(side=tk.LEFT, padx=10)

search_frame = tk.Frame(vocab_frame, bg="#f0f0f0")
search_frame.pack(side=tk.TOP, fill="x")

search_label = tk.Label(search_frame, text="Search word:", font=("Arial", 14), bg="#f0f0f0")
search_label.pack(side=tk.LEFT, padx=10)

search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14), bg="#fff", fg="#333")
search_entry.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

def search_word():
    word_to_find = search_var.get().lower()
    for button in word_buttons:
        if word_to_find in button['text'].lower():
            button.pack(pady=5, anchor='w')
        else:
            button.pack_forget()

search_btn = tk.Button(search_frame, text="Search", font=("Arial", 14), bg="#03A9F4", fg="#fff", command=search_word)
search_btn.pack(side=tk.LEFT, padx=10)

sub_frame = tk.Frame(vocab_frame, bg="#f0f0f0", width=150)
sub_frame.pack(side=tk.LEFT, fill="y")

words = ["goodbye", "thanks", "sorry", "a", "b", "c", "d", "eat", "drink", "hello", "go", "have", "read", "write", "love", "open", "play", "take",
         "learn", "please", "thanks", "use", "book", "water", "phone", "house", "school", "money", "car", "bed", "table", "chair", "friend", 
         "family", "you", "english", "apple", "baby", "camera", "me", "game", "hat"]
word_buttons = []

def play_vocab_video(word):
    video_path = f"../assets/videos/{word}.mp4"
    # Kiểm tra xem tệp video có tồn tại không
    if os.path.exists(video_path):
        vid_player_vocab.load(video_path)
        vid_player_vocab.play()
    else:
        # Nếu không tìm thấy tệp video, hiển thị thông báo lỗi
        text_box.delete("1.0", "end")
        text_box.insert("1.0", f"Video for '{word}' not found.")
button_width = 12
for word in words:
    btn = tk.Button(sub_frame, text=word, font=("Arial", 14), bg="#FFFFFF", fg="#333", 
                        command=lambda w=word: play_vocab_video(w), width=button_width)
    btn.pack(pady=5, anchor='w')
    word_buttons.append(btn)

vid_player_vocab = TkinterVideo(vocab_frame, scaled=True)
vid_player_vocab.pack(expand=True, fill="both", padx=10, pady=10)

back_to_home_btn = tk.Button(vocab_frame, text="Back to Home", bg="#FFFFFF", font=("Arial", 12, "bold"), fg="#333", command=show_home_frame)
back_to_home_btn.pack(side=tk.BOTTOM, pady=10)

# Quiz Frame (for the Vocabulary Quiz section)
quiz_frame = tk.Frame(main_frame, bg="#f5f5f5")
quiz_frame.place(relwidth=1, relheight=1)

quiz_title_label = tk.Label(quiz_frame, text="Vocabulary Quiz", font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333")
quiz_title_label.pack(pady=20)

quiz_instruction_label = tk.Label(quiz_frame, text="Select the correct word for the video shown:", font=("Arial", 16), bg="#f5f5f5", fg="#333")
quiz_instruction_label.pack(pady=10)

quiz_vid_player = TkinterVideo(quiz_frame, scaled=True)
quiz_vid_player.pack(expand=True, fill="both", padx=10, pady=10)

random_word = "goodbye"
random_word_incorrect = "hello"

def quiz_random_word():
    global random_word
    
    # Chọn từ đúng
    random_word = random.choice(words)
    
    # Tạo danh sách các từ sai (không bao gồm từ đúng)
    wrong_words = [word for word in words if word != random_word]
    # Chọn ngẫu nhiên 3 từ sai
    incorrect_words = random.sample(wrong_words, 3)
    
    # Tạo list chứa cả 4 từ (1 đúng + 3 sai)
    all_options = [random_word] + incorrect_words
    # Xáo trộn vị trí các từ
    random.shuffle(all_options)
    
    # Cập nhật text và value cho 4 radio buttons
    quiz_option_1.config(text=all_options[0], value=all_options[0])
    quiz_option_2.config(text=all_options[1], value=all_options[1])
    quiz_option_3.config(text=all_options[2], value=all_options[2])
    quiz_option_4.config(text=all_options[3], value=all_options[3])
    
    # Reset các trạng thái
    quiz_option_var.set(None)
    quiz_instruction_label.config(text="Select the correct word for the video shown:", fg="#333", font=("Arial", 16))
    
    # Bắt đầu quiz với từ đã chọn
    start_quiz(random_word)

def start_quiz(random_word):
    quiz_vid_player.load(f"../assets/videos/{random_word}.mp4")
    quiz_vid_player.play()

# Sử dụng lambda để không gọi hàm ngay lập tức
start_quiz_btn = tk.Button(quiz_frame, text="Start Quiz", bg="#4CAF50", font=("Arial", 12, "bold"), fg="#fff", command=lambda: start_quiz(random_word))
start_quiz_btn.pack(pady=10)
quiz_option_var = tk.StringVar()

def check_answer():
    selected_word = quiz_option_var.get()
    if selected_word == random_word:
        quiz_instruction_label.config(text="Correct!", fg="#4CAF50", font=("Arial", 16, "bold"))
    else:
        quiz_instruction_label.config(text="Wrong answer. Try again!", fg="#FF0000", font=("Arial", 16, "bold"))

quiz_option_1 = tk.Radiobutton(quiz_frame, text="goodbye", variable=quiz_option_var, value="goodbye", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_1.pack(anchor='w', padx=20)

quiz_option_2 = tk.Radiobutton(quiz_frame, text="hello", variable=quiz_option_var, value="hello", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_2.pack(anchor='w', padx=20)
# Thêm 2 radio buttons mới vào phần giao diện (đặt ngay sau quiz_option_2):
quiz_option_3 = tk.Radiobutton(quiz_frame, text="hello", variable=quiz_option_var, value="hello", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_3.pack(anchor='w', padx=20)

quiz_option_4 = tk.Radiobutton(quiz_frame, text="hello", variable=quiz_option_var, value="hello", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_4.pack(anchor='w', padx=20)

quiz_submit_btn = tk.Button(quiz_frame, text="Submit Answer", bg="#03A9F4", font=("Arial", 12, "bold"), fg="#fff", command=check_answer)
quiz_submit_btn.pack(pady=20)

quiz_random_btn = tk.Button(quiz_frame, text="Random Quiz", bg="#03A9F4", font=("Arial", 12, "bold"), fg="#fff", command=quiz_random_word)
quiz_random_btn.pack(pady=20)

back_to_home_btn = tk.Button(quiz_frame, text="Back to Home", bg="#FFFFFF", font=("Arial", 12, "bold"), fg="#333", command=show_home_frame)
back_to_home_btn.pack(side=tk.BOTTOM, pady=10)

# Start with home_frame raised
home_frame.tkraise()

# Run the Tkinter main loop
root.mainloop()
