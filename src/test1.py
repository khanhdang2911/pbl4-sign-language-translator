import datetime
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
from tkintertest import HoverButton
# Thêm imports cần thiết ở đầu file

# Khởi tạo predictor
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

# Initialize frames
main_frame = tk.Frame(root)
login_frame = tk.Frame(root, bg="#f5f5f5")

# Login / Logout functionality
def logout():
    # Reset any necessary variables or states here
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')
    error_label.config(text="")
    
    # Hide main frame and show login frame
    main_frame.pack_forget()
    login_frame.pack(fill='both', expand=True)
    login_frame.tkraise()

def show_home_frame():
    home_frame.pack(fill='both', expand=True)
    video_frame.pack_forget()
    vocab_frame.pack_forget()
    quiz_frame.pack_forget()

def show_video_frame():
    home_frame.pack_forget()
    video_frame.pack(fill='both', expand=True)
    vocab_frame.pack_forget()
    quiz_frame.pack_forget()

def show_vocab_frame():
    home_frame.pack_forget()
    video_frame.pack_forget()
    vocab_frame.pack(fill='both', expand=True)
    quiz_frame.pack_forget()

def show_quiz_frame():
    home_frame.pack_forget()
    video_frame.pack_forget()
    vocab_frame.pack_forget()
    quiz_frame.pack(fill='both', expand=True)
    
    # Chọn từ đúng
    global random_word
    random_word = random.choice(words)
    
    # Tạo danh sách các từ sai
    wrong_words = [word for word in words if word != random_word]
    incorrect_words = random.sample(wrong_words, 3)
    
    # Tạo list chứa cả 4 từ và xáo trộn
    all_options = [random_word] + incorrect_words
    random.shuffle(all_options)
    
    # Cập nhật radio buttons
    quiz_option_1.config(text=all_options[0], value=all_options[0])
    quiz_option_2.config(text=all_options[1], value=all_options[1])
    quiz_option_3.config(text=all_options[2], value=all_options[2])
    quiz_option_4.config(text=all_options[3], value=all_options[3])
    
    quiz_instruction_label.config(text="Select the correct word for the video shown:")
    quiz_option_var.set(None)
    
    quiz_vid_player.load(f"../assets/videos/{random_word}.mp4")
    quiz_vid_player.play()

# Login Frame
login_frame.pack(fill='both', expand=True)

login_label = tk.Label(login_frame, text="Login", font=("Arial", 24, "bold"), bg="#f5f5f5")
login_label.pack(pady=20)

username_label = tk.Label(login_frame, text="Username:", bg="#f5f5f5")
username_label.pack(pady=5)

username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Password:", bg="#f5f5f5")
password_label.pack(pady=5)

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "admin" and password == "password":
        login_frame.pack_forget()  # Hide login frame
        main_frame.pack(fill='both', expand=True)  # Show main frame
        show_home_frame()  # Show home frame with features
        fetch_history()  # Fetch and display recording history
    else:
        error_label.config(text="Invalid username or password", fg="red")

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack(pady=20)

error_label = tk.Label(login_frame, text="", bg="#f5f5f5")
error_label.pack(pady=5)

# Create all other frames
# Home Frame
home_frame = tk.Frame(main_frame, bg="#FFFFFF")

# Header Section
header_frame = tk.Frame(home_frame, bg="#4CAF50")
header_frame.pack(fill="x")

# Add App Image in Header
app_image = Image.open("../assets/images/logo.png")
app_image = app_image.resize((100, 100), Image.LANCZOS)
app_logo = ImageTk.PhotoImage(app_image)

logo_label = tk.Label(header_frame, image=app_logo, bg="#4CAF50")
logo_label.pack(side=tk.LEFT, padx=10)

title_label = tk.Label(header_frame, text="Sign Language Translation & Learning", font=("Arial", 24, "bold"), bg="#4CAF50", fg="#fff")
title_label.pack(side=tk.LEFT, pady=20, expand=True)

# Add Logout Button in Header
logout_button = tk.Button(
    header_frame, 
    text="Logout", 
    font=("Arial", 12, "bold"),
    bg="#FF5722",
    fg="#fff",
    command=logout,
    padx=20
)
logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Button Section
button_frame = tk.Frame(home_frame, bg="#FFFFFF")
button_frame.pack(pady=30)

btn1 = tk.Button(button_frame, text="Translate Sign Language", font=("Arial", 16, "bold"), bg="#4CAF50", fg="#fff", command=show_video_frame)
btn1.pack(pady=10, padx=20, fill="x")

btn2 = tk.Button(button_frame, text="Learn Sign Language", font=("Arial", 16, "bold"), bg="#2196F3", fg="#fff", command=show_vocab_frame)
btn2.pack(pady=10, padx=20, fill="x")

btn_quiz = tk.Button(button_frame, text="Vocabulary Quiz", font=("Arial", 16, "bold"), bg="#FF5722", fg="#fff", command=show_quiz_frame)
btn_quiz.pack(pady=10, padx=20, fill="x")

# Footer
footer_frame = tk.Frame(home_frame, bg="#f5f5f5")
footer_frame.pack(side="bottom", fill="x")

footer_label = tk.Label(footer_frame, text="© 2024 Sign Language Learning App. All Rights Reserved.", font=("Arial", 10), bg="#f5f5f5", fg="#333")
footer_label.pack(pady=10)

# Video Frame
video_frame = tk.Frame(main_frame, bg="#f5f5f5")

# Create a container frame for video and history
video_container = tk.Frame(video_frame, bg="#f5f5f5")
video_container.pack(fill="both", expand=True)

# Left side - Video recording
left_frame = tk.Frame(video_container, bg="#f5f5f5")
left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

top_frame = tk.Frame(left_frame, bg="#f5f5f5")
top_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

vid_player = TkinterVideo(left_frame, scaled=True)
vid_player.pack(expand=True, fill="both", padx=10, pady=10)

video_label = tk.Label(left_frame)
video_label.pack(expand=True, fill="both", padx=10, pady=10)

text_box = tk.Text(left_frame, height=5, width=80, font=("Arial", 12), fg="#333")
text_box.pack(pady=10)

# Right side - History
history_frame = tk.Frame(video_container, bg="#f5f5f5", width=300)
history_frame.pack(side=tk.RIGHT, fill="y", padx=10, pady=10)
history_frame.pack_propagate(False)  # Prevent frame from shrinking

# History header
history_label = tk.Label(
    history_frame,
    text="Recording History",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5",
    fg="#333"
)
history_label.pack(pady=(0, 10))

# Create Treeview for history
history_tree = ttk.Treeview(
    history_frame,
    columns=("date", "text"),
    show="headings",
    height=15
)

# Configure columns
history_tree.heading("date", text="Date")
history_tree.heading("text", text="Translation")
history_tree.column("date", width=100)
history_tree.column("text", width=180)

# Add scrollbar
scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
scrollbar.pack(side="right", fill="y")
history_tree.configure(yscrollcommand=scrollbar.set)
history_tree.pack(fill="both", expand=True)

def fetch_history():
    try:
        response = requests.get('http://localhost:8080/history')
        if response.status_code == 200:
            history_data = response.json()
            
            # Clear existing items
            for item in history_tree.get_children():
                history_tree.delete(item)
            
            # Add new items
            for record in history_data:
                date = datetime.datetime.fromtimestamp(record.get('timestamp')).strftime('%Y-%m-%d %H:%M')
                text = record.get('translation', '')
                history_tree.insert('', 'end', values=(date, text))
                
    except requests.exceptions.RequestException as e:
        # Show error in a small popup
        error_window = tk.Toplevel()
        error_window.title("Error")
        error_window.geometry("300x100")
        tk.Label(
            error_window,
            text="Could not fetch history.\nPlease check if the server is running.",
            pady=20
        ).pack()
        tk.Button(
            error_window,
            text="OK",
            command=error_window.destroy
        ).pack()

# Add refresh button
refresh_btn = tk.Button(
    history_frame,
    text="Refresh History",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10),
    command=fetch_history
)
refresh_btn.pack(pady=10)

recording = False


API_URL = "http://127.0.0.1:3000/predict/"
frame_rate = 30  # 30 FPS

def update_video_frame():
    print("Demo test, not have logic yet")


def record_video():
    print("Demo test, not have logic yet")

def stop_recording():
    print("Demo test, not have logic yet")


class PracticeWindow:
    def __init__(self, word):
        print("Demo test, not have logic yet")

        
    def create_widgets(self):
        print("Demo test, not have logic yet")
        
    def start_practice(self):
        print("Demo test, not have logic yet")
        
    def stop_practice(self):
        print("Demo test, not have logic yet")
        
    def update_practice_frame(self):
        print("Demo test, not have logic yet")
# Thêm function để tạo nút Practice trong word buttons
def create_word_button_with_practice(parent, word, command):
    print("Demo test, not have logic yet")

# Cập nhật hàm update_word_list để sử dụng button mới
def update_word_list(category):
    print("Demo test, not have logic yet")

# Video control buttons in Video Frame
record_btn = HoverButton(
    top_frame,
    text="Record Video",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="#fff",
    relief="flat",
    command=record_video,
    padx=10,
    pady=5,
    width=15,
    cursor="hand2"
)
record_btn.pack(side=tk.LEFT, padx=5)

stop_btn = HoverButton(
    top_frame,
    text="Stop Recording",
    font=("Arial", 12, "bold"),
    bg="#FF0000",
    fg="#fff",
    relief="flat",
    command=stop_recording,
    padx=10,
    pady=5,
    width=15,
    cursor="hand2"
)
stop_btn.pack(side=tk.LEFT, padx=5)

back_to_home_btn = HoverButton(
    video_frame,
    text="Back to Home",
    font=("Helvetica", 14, "bold"),
    bg="#FFFFFF",
    fg="#333",
    relief="flat",
    command=show_home_frame,
    padx=10,
    pady=5,
    width=15,
    cursor="hand2"
)
back_to_home_btn.pack(side=tk.BOTTOM, pady=10)

# Vocabulary Frame
vocab_frame = tk.Frame(main_frame, bg="#f5f5f5")
vocab_frame.place(relwidth=1, relheight=1)

# Vocabulary Learning Section (under "Learn Sign Language")
vocab_title = tk.Label(vocab_frame, text="Learn Sign Language - Vocabulary", font=("Arial", 24, "bold"), bg="#f5f5f5", fg="#333")
vocab_title.pack(pady=20)

category_frame = tk.Frame(vocab_frame, bg="#f0f0f0")
category_frame.pack(fill="x", pady=10)

alphabet_btn = HoverButton(
    category_frame,
    text="Alphabet",
    font=("Arial", 12, "bold"),
    bg="#03A9F4",
    fg="#fff",
    relief="flat",
    command=lambda: update_word_list("alphabet"),
    padx=8,
    pady=4,
    width=8,
    cursor="hand2"
)
alphabet_btn.pack(side=tk.LEFT, padx=10)

verbs_btn = HoverButton(
    category_frame,
    text="Verbs",
    font=("Arial", 12, "bold"),
    bg="#03A9F4",
    fg="#fff",
    relief="flat",
    command=lambda: update_word_list("verbs"),
    padx=8,
    pady=4,
    width=8,
    cursor="hand2"
)
verbs_btn.pack(side=tk.LEFT, padx=10)

nouns_btn = HoverButton(
    category_frame,
    text="Nouns",
    font=("Arial", 12, "bold"),
    bg="#03A9F4",
    fg="#fff",
    relief="flat",
    command=lambda: update_word_list("nouns"),
    padx=8,
    pady=4,
    width=8,
    cursor="hand2"
)
nouns_btn.pack(side=tk.LEFT, padx=10)

search_frame = tk.Frame(vocab_frame, bg="#f0f0f0")
search_frame.pack(side=tk.TOP, fill="x")

search_label = tk.Label(search_frame, text="Search word:", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")

search_label.pack(side=tk.LEFT, padx=10)

search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
search_entry.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

def search_word():
    print("Demo test, not have logic yet")

search_btn = HoverButton(
    search_frame,
    text="Search",
    font=("Arial", 12, "bold"),
    bg="#03A9F4",
    fg="#fff",
    relief="flat",
    command=search_word,
    padx=8,
    pady=4,
    width=8,
    cursor="hand2"
)
search_btn.pack(side=tk.LEFT, padx=10)

sub_frame = tk.Frame(vocab_frame, bg="#f0f0f0", width=150)
sub_frame.pack(side=tk.LEFT, fill="y")

words = ["goodbye", "thanks", "sorry", "a", "b", "c", "d", "eat", "drink", "hello", "go", "have", "read", "write", "love", "open", "play", "take",
         "learn", "please", "thanks", "use", "book", "water", "phone", "house", "school", "money", "car", "bed", "table", "chair", "friend", 
         "family", "you", "english", "apple", "baby", "camera", "me", "game", "hat"]
word_buttons = []

def play_vocab_video(word):
    print("Demo test, not have logic yet")
button_width = 12
for word in words:
    btn = HoverButton(
        sub_frame,
        text=word,
        font=("Arial", 14, "bold"),
        bg="#ff7675",
        fg="#fff",
        relief="flat",
        command=lambda w=word: play_vocab_video(w),
        width=button_width,
        cursor="hand2"
    )
    btn.pack(pady=5, anchor='w')
    word_buttons.append(btn)

vid_player_vocab = TkinterVideo(vocab_frame, scaled=True)
vid_player_vocab.pack(expand=True, fill="both", padx=10, pady=10)

# tro ve
back_to_home_btn = HoverButton(
    vocab_frame,
    text="Back to Home",
    font=("Helvetica", 12, "bold"),  # Giảm kích thước font
    bg="#FFFFFF",
    fg="#333",
    relief="flat",
    command=show_home_frame,
    padx=8,  # Giảm padding
    pady=4,  # Giảm padding
    width=12,  # Giảm chiều rộng
    cursor="hand2"
)
back_to_home_btn.pack(side=tk.BOTTOM, pady=8)  # Giảm khoảng cách padding

# Quiz Frame (for the Vocabulary Quiz section)
quiz_frame = tk.Frame(main_frame, bg="#f5f5f5")
quiz_frame.place(relwidth=1, relheight=1)

quiz_title_label = tk.Label(quiz_frame, text="Vocabulary Quiz", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#333")
quiz_title_label.pack(pady=5)

quiz_instruction_label = tk.Label(quiz_frame, text="Select the correct word for the video shown:", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_instruction_label.pack(pady=7)

quiz_vid_player = TkinterVideo(quiz_frame, scaled=True)
quiz_vid_player.pack(expand=True, fill="both", padx=10, pady=10)


random_word = "goodbye"
random_word_incorrect = "hello"

def quiz_random_word():
    print("Demo test, not have logic yet")

def start_quiz(random_word):
    print("Demo test, not have logic yet")


# Sử dụng lambda để không gọi hàm ngay lập tức
start_quiz_btn = HoverButton(
    quiz_frame,
    text="Start Quiz",
    font=("Helvetica", 12, "bold"),
    bg="#4CAF50",
    fg="#fff",
    relief="flat",
    command=lambda: start_quiz(random_word),
    padx=10,
    pady=5,
    width=15,
    cursor="hand2"
)
start_quiz_btn.pack(pady=10)
quiz_option_var = tk.StringVar()

def check_answer():
    print("Demo test, not have logic yet")

quiz_option_1 = tk.Radiobutton(quiz_frame, text="Goodbye", variable=quiz_option_var, value="goodbye", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_1.pack(anchor='w', padx=2, pady=1)

quiz_option_2 = tk.Radiobutton(quiz_frame, text="Hello", variable=quiz_option_var, value="hello", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_2.pack(anchor='w', padx=2, pady=1)

quiz_option_3 = tk.Radiobutton(quiz_frame, text="Yes", variable=quiz_option_var, value="yes", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_3.pack(anchor='w', padx=2, pady=1)

quiz_option_4 = tk.Radiobutton(quiz_frame, text="No", variable=quiz_option_var, value="no", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_4.pack(anchor='w', padx=2, pady=1)

quiz_submit_btn = HoverButton(
    quiz_frame,
    text="Submit Answer",
    font=("Helvetica", 10, "bold"),
    bg="#03A9F4",
    fg="#fff",
    relief="flat",
    command=check_answer,
    padx=7,
    pady=3,
    width=10,
    cursor="hand2"
)
quiz_submit_btn.pack(pady=5)

quiz_random_btn = HoverButton(
    quiz_frame,
    text="Random Quiz",
    font=("Helvetica", 10, "bold"),
    bg="#03A9F4",
    fg="#fff",
    relief="flat",
    command=quiz_random_word,
    padx=7,
    pady=3,
    width=10,
    cursor="hand2"
)
quiz_random_btn.pack(pady=5)

back_to_home_btn = HoverButton()
back_to_home_btn.pack(side=tk.BOTTOM, pady=7)
# Start with home_frame raised
login_frame.tkraise()

# Run the Tkinter main loop
root.mainloop()
