import customtkinter as ctk
import time

class Timer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#000000")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.timer_state = "picker"  # picker, running, paused
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.timer_id = None
        self.main_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.main_frame.pack(fill="both", expand=True)

        # Title at top left
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Timer",
            font=("Helvetica", 32),
            text_color="#ffffff",
            anchor="w",
            justify="left"
        )
        self.title_label.pack(pady=(30, 10), anchor="w", padx=30)

        # Center content frame for pickers, time, and button
        self.center_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000")
        self.center_frame.pack(expand=True, pady=(0, 80))

        # Barrel picker frame
        self.picker_frame = ctk.CTkFrame(self.center_frame, fg_color="#000000")
        self.picker_frame.pack(pady=(10, 10))

        self.hour_val = 0
        self.minute_val = 30
        self.second_val = 0

        def barrel_picker(parent, label_text, min_val, max_val, get_val, set_val):
            frame = ctk.CTkFrame(parent, fg_color="#000000")
            hold_job = {'up': None, 'down': None}
            repeat_job = {'up': None, 'down': None}
            def up():
                v = get_val()
                v = (v + 1) if v < max_val else min_val
                set_val(v)
                self.update_selected_time()
            def down():
                v = get_val()
                v = (v - 1) if v > min_val else max_val
                set_val(v)
                self.update_selected_time()
            def start_hold(direction):
                # Schedule repeat after 300ms
                def start_repeat():
                    repeat(direction)
                hold_job[direction] = frame.after(300, start_repeat)
            def repeat(direction):
                if direction == 'up':
                    up()
                    repeat_job['up'] = frame.after(100, lambda: repeat('up'))
                else:
                    down()
                    repeat_job['down'] = frame.after(100, lambda: repeat('down'))
            def stop_hold(direction):
                # If hold_job exists, cancel it (means it was a tap, not a hold)
                if hold_job[direction]:
                    frame.after_cancel(hold_job[direction])
                    hold_job[direction] = None
                # If repeat_job exists, cancel it (means it was a hold)
                if repeat_job[direction]:
                    frame.after_cancel(repeat_job[direction])
                    repeat_job[direction] = None
            up_btn = ctk.CTkButton(frame, text="▲", width=40, height=40, command=up, font=("Helvetica", 18), fg_color="#222831", hover_color="#393e46")
            up_btn.pack()
            up_btn.bind("<ButtonPress-1>", lambda e: start_hold('up'))
            up_btn.bind("<ButtonRelease-1>", lambda e: stop_hold('up'))
            val_label = ctk.CTkLabel(frame, text=f"{get_val():02d}", font=("Helvetica", 36, "bold"), text_color="#ffffff", width=60, height=60, fg_color="#222831", corner_radius=20)
            val_label.pack(pady=5)
            down_btn = ctk.CTkButton(frame, text="▼", width=40, height=40, command=down, font=("Helvetica", 18), fg_color="#222831", hover_color="#393e46")
            down_btn.pack()
            down_btn.bind("<ButtonPress-1>", lambda e: start_hold('down'))
            down_btn.bind("<ButtonRelease-1>", lambda e: stop_hold('down'))
            def update_label(*_):
                val_label.configure(text=f"{get_val():02d}")
            frame.update_label = update_label
            return frame

        self.barrel_frames = []
        def get_hour(): return self.hour_val
        def set_hour(v): self.hour_val = v; self.barrel_frames[0].update_label()
        def get_min(): return self.minute_val
        def set_min(v): self.minute_val = v; self.barrel_frames[1].update_label()
        def get_sec(): return self.second_val
        def set_sec(v): self.second_val = v; self.barrel_frames[2].update_label()

        hour_barrel = barrel_picker(self.picker_frame, "Hour", 0, 23, get_hour, set_hour)
        min_barrel = barrel_picker(self.picker_frame, "Min", 0, 59, get_min, set_min)
        sec_barrel = barrel_picker(self.picker_frame, "Sec", 0, 59, get_sec, set_sec)
        hour_barrel.grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(self.picker_frame, text=":", font=("Helvetica", 32), text_color="#ffffff").grid(row=0, column=1)
        min_barrel.grid(row=0, column=2, padx=(10, 10))
        ctk.CTkLabel(self.picker_frame, text=":", font=("Helvetica", 32), text_color="#ffffff").grid(row=0, column=3)
        sec_barrel.grid(row=0, column=4, padx=(10, 0))
        self.barrel_frames = [hour_barrel, min_barrel, sec_barrel]

        # Selected time display
        self.selected_time_label = ctk.CTkLabel(
            self.center_frame,
            text="00:30:00",
            font=("Helvetica", 20),
            text_color="#ffffff",
            fg_color="#222831",
            corner_radius=20,
            width=220,
            height=50
        )
        self.selected_time_label.pack(pady=(20, 40))

        # Start button
        self.start_button = ctk.CTkButton(
            self.center_frame,
            text="▶",
            command=self.start_timer,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.start_button.pack(pady=(0, 0))

        # Countdown frame (hidden initially)
        self.countdown_frame = ctk.CTkFrame(self.center_frame, fg_color="#000000")
        self.countdown_label = ctk.CTkLabel(
            self.countdown_frame,
            text="00:00:00",
            font=("Helvetica", 48, "bold"),
            text_color="#ffffff"
        )
        self.countdown_label.pack(pady=(10, 40))
        self.total_label = ctk.CTkLabel(
            self.countdown_frame,
            text="",
            font=("Helvetica", 18),
            text_color="#888888"
        )
        self.total_label.pack(pady=(0, 40))

        # Pause and Reset buttons
        self.timer_buttons_frame = ctk.CTkFrame(self.countdown_frame, fg_color="transparent")
        self.pause_button = ctk.CTkButton(
            self.timer_buttons_frame,
            text="⏸",
            command=self.pause_timer,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.reset_button = ctk.CTkButton(
            self.timer_buttons_frame,
            text="■",
            command=self.reset_timer,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.resume_button = ctk.CTkButton(
            self.timer_buttons_frame,
            text="▶",
            command=self.resume_timer,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.pause_button.pack(side="left", padx=30)
        self.reset_button.pack(side="right", padx=30)
        self.timer_buttons_frame.pack(pady=(0, 0))
        self.countdown_frame.pack_forget()

        # Update selected time when pickers change
        self.update_selected_time()

    def update_selected_time(self):
        h = self.hour_val
        m = self.minute_val
        s = self.second_val
        self.selected_time_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

    def show_pause_reset(self):
        self.clear_timer_buttons()
        self.pause_button.pack(side="left", padx=30)
        self.reset_button.pack(side="right", padx=30)

    def show_resume_reset(self):
        self.clear_timer_buttons()
        self.resume_button.pack(side="left", padx=30)
        self.reset_button.pack(side="right", padx=30)

    def clear_timer_buttons(self):
        for widget in self.timer_buttons_frame.winfo_children():
            widget.pack_forget()

    def start_timer(self):
        h = self.hour_val
        m = self.minute_val
        s = self.second_val
        self.total_seconds = h * 3600 + m * 60 + s
        if self.total_seconds == 0:
            return
        self.remaining_seconds = self.total_seconds
        self.show_countdown()
        self.show_pause_reset()
        self.update_countdown()

    def show_countdown(self):
        self.picker_frame.pack_forget()
        self.selected_time_label.pack_forget()
        self.start_button.pack_forget()
        self.countdown_frame.pack(pady=(40, 0), fill="both", expand=True)
        self.total_label.configure(text=f"Total {self.total_seconds//60} minutes" if self.total_seconds >= 60 else f"Total {self.total_seconds} seconds")

    def update_countdown(self):
        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60
        if self.remaining_seconds > 0:
            self.countdown_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
            self.remaining_seconds -= 1
            self.timer_id = self.after(1000, self.update_countdown)
        else:
            self.countdown_label.configure(text="Time's up")
            # Optionally: play sound or show alert

    def pause_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.show_resume_reset()

    def reset_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.countdown_frame.pack_forget()
        self.picker_frame.pack(pady=(40, 20))
        self.selected_time_label.pack(pady=(30, 60))
        self.start_button.pack()
        self.update_selected_time()

    def resume_timer(self):
        self.show_pause_reset()
        self.update_countdown()

if __name__ == "__main__":
    app = Timer()
    app.mainloop() 
