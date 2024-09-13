from tkinter import *
import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import requests  # Thư viện để gửi request HTTP

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

def update_duration(event):
    """ Cập nhật thời gian kết thúc và giá trị thanh trượt """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration

def update_scale(event):
    """ Cập nhật giá trị thanh trượt theo thời gian hiện tại của video """
    progress_value.set(vid_player.current_duration())

def load_video():
    """ Tải video và gửi chuỗi văn bản lên server để xử lý """
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)
        # Ví dụ gửi chuỗi văn bản lên server
        text_to_send = "iloveyou"  # Thay đổi chuỗi văn bản theo yêu cầu tùy chọn
        process_text(text_to_send)

def process_text(text):
    """ Gửi chuỗi văn bản lên server và xử lý phản hồi """
    url = "http://localhost:8080/home/create-text-voice"  # Url cho api xử lý chuỗi văn bản
    payload = {'text_voice': text}  # Thay đổi 'text_voice' là trường cần gửi trong body
    response = requests.post(url, json=payload)  # Gửi payload dưới dạng JSON
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            formatted_text = result.get("message", "No message returned")
            text_box.delete("1.0", "end")
            text_box.insert("1.0", formatted_text)
        else:
            text_box.delete("1.0", "end")
            text_box.insert("1.0", "Error in server response")
    else:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "Error processing text")


def seek(value):
    """ Di chuyển đến thời điểm cụ thể trong video """
    vid_player.seek(int(value))

def skip(value: int):
    """ Lùi hoặc tiến một số giây trong video """
    vid_player.seek(int(progress_slider.get()) + value)
    progress_value.set(progress_slider.get() + value)

def play_pause():
    """ Phát hoặc tạm dừng video """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"
    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"

def video_ended(event):
    """ Xử lý khi video kết thúc """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

load_btn = tk.Button(top_frame, text="Browse", bg="#FFFFFF", font=("calibri", 12, "bold"), command=load_video)
load_btn.pack(side=tk.LEFT, padx=5)

start_time = tk.Label(top_frame, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side=tk.LEFT)

progress_value = tk.IntVar(root)
progress_slider = tk.Scale(top_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

end_time = tk.Label(top_frame, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side=tk.LEFT)

vid_player = TkinterVideo(root, scaled=True)
vid_player.pack(expand=True, fill="both")

Buttonbackward = PhotoImage(file="backward.png")
back = tk.Button(lower_frame, image=Buttonbackward, bd=0, height=50, width=50, command=lambda: skip(-5)).pack(side=LEFT)

play_pause_btn = tk.Button(lower_frame, text="Play", width=40, height=2, command=play_pause)
play_pause_btn.pack(expand=True, fill="both", side=LEFT)

ButtonPlay = PhotoImage(file="forward.png")
Playbutton = tk.Button(lower_frame, image=ButtonPlay, bd=0, height=50, width=50, command=lambda: skip(5)).pack(side=LEFT)

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)

text_box = tk.Text(root, height=5, width=80)
text_box.pack(pady=10, fill="x")

text_box.insert("1.0", "This is a text box to display text below the video.")

root.mainloop()
