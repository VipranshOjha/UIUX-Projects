import customtkinter as ctk
from Alarm import Alarm
from WorldClock import WorldClock
from Stopwatch import Stopwatch
from Timer import Timer

class ClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clock")
        self.geometry("400x700")
        self.resizable(False, False)
        self.configure(fg_color="#000000")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.content_frame.pack(fill="both", expand=True)

        # Bottom navigation bar
        self.nav_frame = ctk.CTkFrame(self, fg_color="#000000", height=60)
        self.nav_frame.pack(side="bottom", fill="x")

        self.buttons = {}
        self.active = None

        # Navigation buttons
        self.buttons['WorldClock'] = ctk.CTkButton(
            self.nav_frame, text="World clock", command=lambda: self.show_frame('WorldClock'), width=90, height=50, fg_color="#222831", hover_color="#393e46")
        self.buttons['Alarm'] = ctk.CTkButton(
            self.nav_frame, text="Alarm", command=lambda: self.show_frame('Alarm'), width=90, height=50, fg_color="#222831", hover_color="#393e46")
        self.buttons['Stopwatch'] = ctk.CTkButton(
            self.nav_frame, text="Stopwatch", command=lambda: self.show_frame('Stopwatch'), width=90, height=50, fg_color="#222831", hover_color="#393e46")
        self.buttons['Timer'] = ctk.CTkButton(
            self.nav_frame, text="Timer", command=lambda: self.show_frame('Timer'), width=90, height=50, fg_color="#222831", hover_color="#393e46")

        for i, key in enumerate(['WorldClock', 'Alarm', 'Stopwatch', 'Timer']):
            self.buttons[key].grid(row=0, column=i, padx=5, pady=5)
        self.nav_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Show WorldClock by default
        self.current_frame = None
        self.show_frame('WorldClock')

    def show_frame(self, name):
        # Destroy current frame if exists
        if self.current_frame is not None:
            self.current_frame.destroy()
        # Create new frame
        if name == 'Alarm':
            self.current_frame = Alarm(self.content_frame)
        elif name == 'WorldClock':
            self.current_frame = WorldClock(self.content_frame)
        elif name == 'Stopwatch':
            self.current_frame = Stopwatch(self.content_frame)
        elif name == 'Timer':
            self.current_frame = Timer(self.content_frame)
        self.current_frame.pack(fill="both", expand=True)
        # Highlight active button
        for key, btn in self.buttons.items():
            if key == name:
                btn.configure(fg_color="#4444aa")
            else:
                btn.configure(fg_color="#222831")

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop() 
