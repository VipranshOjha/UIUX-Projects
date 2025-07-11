import customtkinter as ctk
import time

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.grid_columnconfigure(0, weight=1)

class Stopwatch(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#000000")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_time = 0
        self.lap_times = []
        self.current_time = "00:00.00"

        self.main_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.main_frame.pack(pady=0, padx=0, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Stopwatch",
            font=("Helvetica", 32),
            text_color="#ffffff",
            anchor="w",
            justify="left"
        )
        self.title_label.pack(pady=(30, 10), anchor="w", padx=30)

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text=self.current_time,
            font=("Helvetica", 56, "bold"),
            text_color="#ffffff"
        )
        self.time_label.pack(pady=(60, 40))

        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=10)

        # Buttons (will be managed dynamically)
        self.start_button = ctk.CTkButton(
            self.buttons_frame,
            text="▶",
            command=self.start_stopwatch,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.lap_button = ctk.CTkButton(
            self.buttons_frame,
            text="Lap",
            command=self.lap_time,
            font=("Helvetica", 20, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#ffffff"
        )
        self.pause_button = ctk.CTkButton(
            self.buttons_frame,
            text="⏸",
            command=self.pause_stopwatch,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.resume_button = ctk.CTkButton(
            self.buttons_frame,
            text="▶",
            command=self.resume_stopwatch,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )
        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="■",
            command=self.reset_stopwatch,
            font=("Helvetica", 32, "bold"),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#222831",
            hover_color="#393e46",
            text_color="#00aaff"
        )

        # Lap times frame (hidden until first lap)
        self.lap_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000")
        self.lap_list_frame = ScrollableFrame(self.lap_frame, fg_color="transparent", height=120)
        self.lap_list_frame.pack(pady=10, padx=30, fill="both", expand=False)
        self.lap_frame.pack_forget()

        self.show_initial_buttons()

    def show_initial_buttons(self):
        self.clear_buttons()
        self.start_button.pack()

    def show_running_buttons(self):
        self.clear_buttons()
        self.pause_button.pack(side="left", padx=30)
        self.lap_button.pack(side="right", padx=30)

    def show_paused_buttons(self):
        self.clear_buttons()
        self.resume_button.pack(side="left", padx=30)
        self.reset_button.pack(side="right", padx=30)

    def clear_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.pack_forget()

    def start_stopwatch(self):
        self.running = True
        self.paused = False
        self.start_time = time.time() - self.pause_time
        self.update_time()
        self.show_running_buttons()

    def pause_stopwatch(self):
        self.running = False
        self.paused = True
        self.pause_time = time.time() - self.start_time
        self.show_paused_buttons()

    def resume_stopwatch(self):
        self.running = True
        self.paused = False
        self.start_time = time.time() - self.pause_time
        self.update_time()
        self.show_running_buttons()

    def reset_stopwatch(self):
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_time = 0
        self.current_time = "00:00.00"
        self.time_label.configure(text=self.current_time)
        self.lap_times = []
        self.lap_frame.pack_forget()
        self.clear_lap_list()
        self.show_initial_buttons()

    def lap_time(self):
        if not self.running:
            return
        now = time.time() - self.start_time
        lap_time = now if not self.lap_times else now - sum(self.lap_times)
        self.lap_times.append(lap_time)
        self.show_lap_list()
        self.add_lap_time(len(self.lap_times), lap_time, now)

    def update_time(self):
        if self.running:
            now = time.time() - self.start_time
            minutes = int(now // 60)
            seconds = int(now % 60)
            centiseconds = int((now % 1) * 100)
            self.current_time = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            self.time_label.configure(text=self.current_time)
            self.after(10, self.update_time)

    def show_lap_list(self):
        self.lap_frame.pack(pady=(10,0), padx=0, fill="both", expand=True)

    def add_lap_time(self, lap_number, lap_time, total_time):
        frame = ctk.CTkFrame(self.lap_list_frame, fg_color="#000000")
        frame.pack(pady=2, padx=2, fill="x")
        # Lap number
        ctk.CTkLabel(
            frame,
            text=f"{lap_number:02d}",
            font=("Helvetica", 16),
            text_color="#888888"
        ).pack(side="left", padx=10)
        # Lap time (difference)
        ctk.CTkLabel(
            frame,
            text=f"+ {lap_time:0.2f}",
            font=("Helvetica", 16),
            text_color="#888888"
        ).pack(side="left", padx=10)
        # Total time
        ctk.CTkLabel(
            frame,
            text=f"{total_time:0.2f}",
            font=("Helvetica", 16),
            text_color="#ffffff"
        ).pack(side="right", padx=10)

    def clear_lap_list(self):
        for widget in self.lap_list_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = Stopwatch()
    app.mainloop() 
