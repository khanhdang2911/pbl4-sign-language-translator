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

frame = tk.Frame(root)
frame.pack()

image_icon = PhotoImage(file="logo png.png")
root.iconphoto(False, image_icon)

top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

lower_frame = tk.Frame(root, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)

vid_player = TkinterVideo(root, scaled=True)
vid_player.pack(expand=True, fill="both")

text_box = tk.Text(root, height=5, width=80)
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

record_btn = tk.Button(top_frame, text="Record Video", bg="#FFFFFF", font=("calibri", 12, "bold"), command=record_video)
record_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(top_frame, text="Stop Recording", bg="#FF0000", font=("calibri", 12, "bold"), command=stop_recording)
stop_btn.pack(side=tk.LEFT, padx=5)

upload_btn = tk.Button(top_frame, text="Upload Video", bg="#FFFFFF", font=("calibri", 12, "bold"), command=upload_video)
upload_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
