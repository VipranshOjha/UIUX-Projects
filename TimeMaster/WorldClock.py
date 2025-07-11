import customtkinter as ctk
import datetime

class WorldClock(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#000000")
        self.main_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.main_frame.pack(fill="both", expand=True)
        # Title at top left
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="World clock",
            font=("Helvetica", 32),
            text_color="#ffffff",
            anchor="w",
            justify="left"
        )
        self.title_label.pack(pady=(30, 10), anchor="w", padx=30)
        # Center content frame
        self.center_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000")
        self.center_frame.pack(expand=True)
        # Time label
        self.time_label = ctk.CTkLabel(
            self.center_frame,
            text="00:00:00",
            font=("Helvetica", 48, "bold"),
            text_color="#ffffff"
        )
        self.time_label.pack(pady=(10, 10))
        # Date label
        self.date_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            font=("Helvetica", 20),
            text_color="#888888"
        )
        self.date_label.pack(pady=(0, 40))
        # Local time label (optional, for style)
        self.local_label = ctk.CTkLabel(
            self.center_frame,
            text="",
            font=("Helvetica", 16),
            text_color="#888888"
        )
        self.local_label.pack(pady=(0, 40))
        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now()
        self.time_label.configure(text=now.strftime("%H:%M:%S"))
        self.date_label.configure(text=now.strftime("Local time %m/%d %p"))
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    app = WorldClock(None)
    app.mainloop() 
