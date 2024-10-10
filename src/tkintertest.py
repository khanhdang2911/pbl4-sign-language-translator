import cv2
import requests
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk 
from tkVideoPlayer import TkinterVideo
from tkinter import filedialog

root = tk.Tk()
root.title("Simpli Video Player")
root.geometry("800x700+290+10")

image_icon = PhotoImage(file="../assets/images/logo.png")
root.iconphoto(False, image_icon)

def show_home_frame():
    home_frame.tkraise()

def show_video_frame():
    video_frame.tkraise()

def show_vocab_frame():
    vocab_frame.tkraise()

def show_quiz_frame():
    quiz_frame.tkraise()

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

home_frame = tk.Frame(main_frame)
home_frame.place(relwidth=1, relheight=1)

btn1 = tk.Button(home_frame, text="Dịch NNKH", font=("calibri", 14), command=show_video_frame)
btn1.pack(pady=20)

btn2 = tk.Button(home_frame, text="Học NNKH", font=("calibri", 14), command=show_vocab_frame)
btn2.pack(pady=20)

btn_quiz = tk.Button(home_frame, text="Kiểm tra từ vựng", font=("calibri", 14), command=show_quiz_frame)
btn_quiz.pack(pady=20)

video_frame = tk.Frame(main_frame)
video_frame.place(relwidth=1, relheight=1)

top_frame = tk.Frame(video_frame)
top_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

lower_frame = tk.Frame(video_frame, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)

vid_player = TkinterVideo(video_frame, scaled=True)
vid_player.pack(expand=True, fill="both")

text_box = tk.Text(video_frame, height=5, width=80)
text_box.pack(pady=10, fill="x")
text_box.insert("1.0", "This is a text box to display text below the video.")

video_label = tk.Label(vid_player)
video_label.pack()

recording = False

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

def record_video():
    global cap, recording
    cap = cv2.VideoCapture(1) 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    recording = True
    update_video_frame()  

def stop_recording():
    global recording, cap
    recording = False
    cap.release()  
    text_box.delete("1.0", "end")
    text_box.insert("1.0", "Recording stopped.")

def upload_video():
    file_path = filedialog.askopenfilename()

    if file_path:
        files = {'file': open(file_path, 'rb')}
        url = 'http://localhost:8080/upload-video'  
        response = requests.post(url, files=files)

        if response.status_code == 200:
            text_box.delete("1.0", "end")
            text_box.insert("1.0", "Video uploaded successfully")
        else:
            text_box.delete("1.0", "end")
            text_box.insert("1.0", "Failed to upload video")

# call api
def get_video_by_prompt(prompt):
    url = f'http://localhost:8081/learn-signature/get-video-by-prompt?prompt={prompt}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print(video_data)
            video_data = data["videos"][0]
            cloudinary_url = video_data.get("video_url")

            text_box.delete("1.0", "end")
            text_box.insert("1.0", f"Video found: {video_data['prompt']}")

            # load video
            vid_player.load(cloudinary_url)
            vid_player.play()
        else:
            text_box.delete("1.0", "end")
            text_box.insert("1.0", "No video found for the given prompt")
    else:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", f"Failed to fetch video. Error: {response.status_code}")

record_btn = tk.Button(top_frame, text="Record Video", bg="#FFFFFF", font=("calibri", 12, "bold"), command=record_video)
record_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(top_frame, text="Stop Recording", bg="#FF0000", font=("calibri", 12, "bold"), command=stop_recording)
stop_btn.pack(side=tk.LEFT, padx=5)

upload_btn = tk.Button(top_frame, text="Upload Video", bg="#FFFFFF", font=("calibri", 12, "bold"), command=upload_video)
upload_btn.pack(side=tk.LEFT, padx=5)

search_btn_video = tk.Button(top_frame, text="Search Video by Prompt", bg="#FFFFFF", font=("calibri", 12, "bold"), command=lambda: get_video_by_prompt("book"))
search_btn_video.pack(side=tk.LEFT, padx=5)

back_to_home_btn = tk.Button(video_frame, text="Trở về trang chủ", bg="#FFFFFF", font=("calibri", 12, "bold"), command=show_home_frame)
back_to_home_btn.pack(side=tk.BOTTOM, pady=10)

vocab_frame = tk.Frame(main_frame)
vocab_frame.place(relwidth=1, relheight=1)

search_frame = tk.Frame(vocab_frame, bg="#f0f0f0")
search_frame.pack(side=tk.TOP, fill="x")

search_label = tk.Label(search_frame, text="Tìm từ:", font=("calibri", 12))
search_label.pack(side=tk.LEFT, padx=10)

search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("calibri", 12))
search_entry.pack(side=tk.LEFT, padx=10, fill="x", expand=True)

def search_word():
    word_to_find = search_var.get().lower()
    for button in word_buttons:
        if word_to_find in button['text'].lower():
            button.pack(pady=5, anchor='w')
        else:
            button.pack_forget()

search_btn = tk.Button(search_frame, text="Tìm kiếm", font=("calibri", 12), command=search_word)
search_btn.pack(side=tk.LEFT, padx=10)

sub_frame = tk.Frame(vocab_frame, bg="#f0f0f0", width=150)
sub_frame.pack(side=tk.LEFT, fill="y")

words = ["hello", "goodbye", "thanks", "sorry"]
word_buttons = []

def play_vocab_video(word):
    video_path = f"../assets/videos/{word}.mp4"
    vid_player_vocab.load(video_path)
    vid_player_vocab.play()

for word in words:
    btn = tk.Button(sub_frame, text=word, font=("calibri", 12), command=lambda w=word: play_vocab_video(w))
    btn.pack(pady=5, anchor='w')
    word_buttons.append(btn)

vid_player_vocab = TkinterVideo(vocab_frame, scaled=True)
vid_player_vocab.pack(expand=True, fill="both")

back_to_home_btn_vocab = tk.Button(vocab_frame, text="Trở về trang chủ", bg="#FFFFFF", font=("calibri", 12), command=show_home_frame)
back_to_home_btn_vocab.pack(side=tk.BOTTOM, pady=10)

quiz_frame = tk.Frame(main_frame)
quiz_frame.place(relwidth=1, relheight=1)

quiz_label = tk.Label(quiz_frame, text="Kiểm tra từ vựng", font=("calibri", 20))
quiz_label.pack(pady=20)

vid_player_quiz = TkinterVideo(quiz_frame, scaled=True)
vid_player_quiz.pack(expand=True, fill="both")

back_to_home_btn_quiz = tk.Button(quiz_frame, text="Trở về trang chủ", bg="#FFFFFF", font=("calibri", 12), command=show_home_frame)
back_to_home_btn_quiz.pack(side=tk.BOTTOM, pady=10)

show_home_frame()

root.mainloop()
