from tkinter import *
import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo

root = tk.Tk()
root.title("Simpli Video Player")
root.geometry("800x700+290+10")

frame = tk.Frame(root)
frame.pack()

image_icon = PhotoImage(file="logo png.png")
root.iconphoto(False, image_icon)

# Tạo khung mới chứa nút "Browse", thanh progress_slider và thời gian video
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill="x", padx=10, pady=10)

lower_frame = tk.Frame(root, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)

def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration

def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())

def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)

def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))

def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get()) + value)
    progress_value.set(progress_slider.get() + value)

def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"
    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"

def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

# Đặt nút "Browse" vào khung top_frame
load_btn = tk.Button(top_frame, text="Browse", bg="#FFFFFF", font=("calibri", 12, "bold"), command=load_video)
load_btn.pack(side=tk.LEFT, padx=5)

# Đặt thời gian bắt đầu vào khung top_frame (bên trái thanh slider)
start_time = tk.Label(top_frame, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side=tk.LEFT)

# Đặt thanh progress_slider vào khung top_frame cạnh nút "Browse"
progress_value = tk.IntVar(root)
progress_slider = tk.Scale(top_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

# Đặt thời gian kết thúc vào khung top_frame (bên phải thanh slider)
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

# Tạo một ô text box ngay dưới video player
text_box = tk.Text(root, height=5, width=80)
text_box.pack(pady=10, fill="x")

# Cài đặt nội dung ban đầu cho text box (nếu cần)
text_box.insert("1.0", "This is a text box to display text below the video.")

root.mainloop()
