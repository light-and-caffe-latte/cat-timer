import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from typing import Optional, Any # 型ヒントの為追加




class main:

    root: tk.Tk
    remaining_seconds: int
    is_running: bool
    after_id: Optional[int]
    alarm_window: Optional[tk.Toplevel]
    play_photo: Optional[ImageTk.PhotoImage]
    pause_photo: Optional[ImageTk.PhotoImage]
    reset_photo: Optional[ImageTk.PhotoImage]
    count_down_time: tk.StringVar
    label_time: tk.Label
    button_toggle: tk.Button
    button_reset: tk.Button
    initial_upmin: tk.Button
    initial_5min: tk.Button
    initial_downmin: tk.Button

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Timer")
        # self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.root.configure(bg="#8a9a5b")
        
        self.remaining_seconds = 0
        self.is_running = False
        self.after_id = None
        self.alarm_window = None
        
        # Load toggle icons
        try:
            play_img = Image.open("cat_start_icon.png").resize((48, 48), Image.Resampling.LANCZOS)
            pause_img = Image.open("cat_stop_icon.png").resize((48, 48), Image.Resampling.LANCZOS)
            reset_img = Image.open("cat_reset_icon.png").resize((48, 48), Image.Resampling.LANCZOS)
            self.play_photo = ImageTk.PhotoImage(play_img)
            self.pause_photo = ImageTk.PhotoImage(pause_img)
            self.reset_photo = ImageTk.PhotoImage(reset_img)
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.play_photo = None
            self.pause_photo = None
            self.reset_photo = None

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self) -> None:
        
        # display time
        label_area = tk.Frame(self.root, bg="#8a9a5b")
        label_area.pack(pady=10)

        self.count_down_time = tk.StringVar()
        self.count_down_time.set("00:00:00")
        self.label_time = tk.Label(label_area, textvariable=self.count_down_time, font=("Helvetica", 45), bg="#8a9a5b", fg="white")
        self.label_time.pack()

        # control buttons
        button_area = tk.Frame(self.root, bg="#8a9a5b")
        button_area.pack(padx=10)
        
        self.button_toggle = tk.Button(button_area, command=self.toggle_timer, borderwidth=0, bg="#8a9a5b", activebackground="#8a9a5b")
        if self.play_photo:
            self.button_toggle.config(image=self.play_photo)
        else:
            self.button_toggle.config(text="Start", font=("Helvetica", 24))
        self.button_toggle.pack(side="left", padx=5)

        self.button_reset = tk.Button(button_area, command=self.reset_timer, borderwidth=0, bg="#8a9a5b", activebackground="#8a9a5b")
        if self.reset_photo:
            self.button_reset.config(image=self.reset_photo)
        else:
            self.button_reset.config(text="Reset", font=("Helvetica", 24))
        self.button_reset.pack(side="left", padx=2)

        # initial time buttons
        initial_area = tk.Frame(self.root, bg="#8a9a5b")
        initial_area.pack(pady=10)

        self.initial_upmin = tk.Button(initial_area, text="-", font=("Helvetica", 24), command=lambda: self.adjust_time(-60))
        self.initial_upmin.pack(side="left")        
        self.initial_5min = tk.Button(initial_area, text="5min", font=("Helvetica", 24), command=lambda: self.set_time(300))
        self.initial_5min.pack(side="left")
        self.initial_downmin = tk.Button(initial_area, text="+", font=("Helvetica", 24), command=lambda: self.adjust_time(60))
        self.initial_downmin.pack(side="left")

    def update_display(self) -> None:
        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60
        self.count_down_time.set(f"{h:02d}:{m:02d}:{s:02d}")

    def adjust_time(self, delta: int) -> None:
        self.remaining_seconds = max(0, self.remaining_seconds + delta)
        self.update_display()

    def set_time(self, seconds: int) -> None:
        self.remaining_seconds = seconds
        self.update_display()

    def toggle_timer(self) -> None:
        if self.is_running:
            self.stop_timer()
        else:
            if self.remaining_seconds > 0:
                self.start_timer()

    def start_timer(self) -> None:
        if not self.is_running and self.remaining_seconds > 0:
            self.is_running = True
            if self.pause_photo:
                self.button_toggle.config(image=self.pause_photo)
            else:
                self.button_toggle.config(text="Stop")
            self.tick()

    def stop_timer(self) -> None:
        self.is_running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        if self.play_photo:
            self.button_toggle.config(image=self.play_photo)
        else:
            self.button_toggle.config(text="Start")

    def reset_timer(self) -> None:
        self.stop_timer()
        self.remaining_seconds = 0
        self.update_display()
        if self.alarm_window:
            self.alarm_window.destroy()
            self.alarm_window = None

    def tick(self) -> None:
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            if self.remaining_seconds == 0:
                self.is_running = False
                self.trigger_alarm()
            else:
                self.after_id = self.root.after(1000, self.tick)

    def trigger_alarm(self) -> None:
        if self.alarm_window:
            return
        
        self.alarm_window = tk.Toplevel(self.root)
        self.alarm_window.title("Time's Up!")
        
        try:
            img = Image.open("cat_alarm.png")
            # Resize if needed, keeping aspect ratio
            img.thumbnail((550, 826))
            self.photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.alarm_window, image=self.photo)
            label.pack()
        except Exception as e:
            label = tk.Label(self.alarm_window, text="Time's Up! (Image not found)", font=("Helvetica", 16))
            label.pack(pady=20)
            print(f"Error loading image: {e}")

        btn_close = tk.Button(self.alarm_window, text="OK", command=self.reset_timer)
        btn_close.pack(pady=10)



if __name__ == "__main__":
    
    root: tk.Tk = tk.Tk()

    window: main = main(root)

