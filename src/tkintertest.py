import cv2
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo
from tkinter import filedialog
import os  # Thêm thư viện os để kiểm tra tệp tin

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

# Main frame
main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill="both", expand=True)

# Home Frame
home_frame = tk.Frame(main_frame, bg="#FFFFFF")
home_frame.place(relwidth=1, relheight=1)

title_label = tk.Label(home_frame, text="Sign Language Translation & Learning", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333")
title_label.pack(pady=20)

btn1 = tk.Button(home_frame, text="Translate Sign Language", font=("Arial", 16, "bold"), bg="#4CAF50", fg="#fff", command=show_video_frame)
btn1.pack(pady=20)

btn2 = tk.Button(home_frame, text="Learn Sign Language", font=("Arial", 16, "bold"), bg="#2196F3", fg="#fff", command=show_vocab_frame)
btn2.pack(pady=20)

btn_quiz = tk.Button(home_frame, text="Vocabulary Quiz", font=("Arial", 16, "bold"), bg="#FF5722", fg="#fff", command=show_quiz_frame)
btn_quiz.pack(pady=20)

# Video Frame
video_frame = tk.Frame(main_frame, bg="#f5f5f5")
video_frame.place(relwidth=1, relheight=1)

top_frame = tk.Frame(video_frame, bg="#f5f5f5")
top_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

lower_frame = tk.Frame(video_frame, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)

vid_player = TkinterVideo(video_frame, scaled=True)
vid_player.pack(expand=True, fill="both", padx=10, pady=10)

text_box = tk.Text(video_frame, height=5, width=80, font=("Arial", 12), fg="#333")
text_box.pack(pady=10, fill="x")
text_box.insert("1.0", "This is a text box to display text below the video.")

video_label = tk.Label(vid_player)
video_label.pack()

# Video recording control variable
recording = False

# Function to update video frames
def update_video_frame():
    global recording, cap
    if recording:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        video_label.after(10, update_video_frame)

# Function to start recording video
def record_video():
    global cap, recording
    cap = cv2.VideoCapture(1)
    recording = True
    update_video_frame()

# Function to stop recording video
def stop_recording():
    global recording, cap
    recording = False
    cap.release()
    text_box.delete("1.0", "end")
    text_box.insert("1.0", "Recording stopped.")
def update_word_list(category):
    # Xóa hết các nút từ hiện tại trước khi hiển thị danh sách mới
    for button in word_buttons:
        button.pack_forget()

    # Tạo danh sách từ dựa trên category được chọn
    if category == "alphabet":
        words_to_display = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    elif category == "verbs":
        words_to_display = ["eat", "drink", "go", "have", "read", "write", "love", "open", "play", "take", "learn", "use"]
    elif category == "nouns":
        words_to_display = ["book", "water", "phone", "house", "school", "money", "car", "bed", "table", "chair", "friend", "family"]

    # Hiển thị danh sách từ mới
    for word in words_to_display:
        btn = tk.Button(sub_frame, text=word, font=("Arial", 14), bg="#FFFFFF", fg="#333", command=lambda w=word: play_vocab_video(w))
        btn.pack(pady=5, anchor='w')
        word_buttons.append(btn)

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

for word in words:
    btn = tk.Button(sub_frame, text=word, font=("Arial", 14), bg="#FFFFFF", fg="#333", command=lambda w=word: play_vocab_video(w))
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

def start_quiz():
    quiz_vid_player.load("../assets/videos/goodbye.mp4")
    quiz_vid_player.play()

start_quiz_btn = tk.Button(quiz_frame, text="Start Quiz", bg="#4CAF50", font=("Arial", 12, "bold"), fg="#fff", command=start_quiz)
start_quiz_btn.pack(pady=10)

quiz_option_var = tk.StringVar()

def check_answer():
    selected_word = quiz_option_var.get()
    if selected_word == "goodbye":
        quiz_instruction_label.config(text="Correct!")
    else:
        quiz_instruction_label.config(text="Try again.")

quiz_option_1 = tk.Radiobutton(quiz_frame, text="goodbye", variable=quiz_option_var, value="goodbye", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_1.pack(anchor='w', padx=20)

quiz_option_2 = tk.Radiobutton(quiz_frame, text="hello", variable=quiz_option_var, value="hello", font=("Arial", 14), bg="#f5f5f5", fg="#333")
quiz_option_2.pack(anchor='w', padx=20)

quiz_submit_btn = tk.Button(quiz_frame, text="Submit Answer", bg="#03A9F4", font=("Arial", 12, "bold"), fg="#fff", command=check_answer)
quiz_submit_btn.pack(pady=20)

back_to_home_btn = tk.Button(quiz_frame, text="Back to Home", bg="#FFFFFF", font=("Arial", 12, "bold"), fg="#333", command=show_home_frame)
back_to_home_btn.pack(side=tk.BOTTOM, pady=10)

# Start with home_frame raised
home_frame.tkraise()

# Run the Tkinter main loop
root.mainloop()
