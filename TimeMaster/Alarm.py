import customtkinter as ctk
import datetime
import time
import winsound
from threading import Thread

class AlarmData:
    def __init__(self, hour, minute, enabled=True):
        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.thread = None

    def time(self):
        return datetime.time(self.hour, self.minute)

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}"

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.grid_columnconfigure(0, weight=1)

class Alarm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#000000")
        # Initialize alarms list
        self.alarms = []
        # Create main frame with gradient effect
        self.main_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.main_frame.pack(pady=15, padx=15, fill="both", expand=False)
        # Time display with glowing effect
        self.time_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000", corner_radius=15)
        self.time_frame.pack(pady=10, padx=15, fill="x")
        self.time_label = ctk.CTkLabel(
            self.time_frame,
            text="No alarms set",
            font=("Helvetica", 48, "bold"),
            text_color="#ffffff"
        )
        self.time_label.pack(pady=15)
        # Date display
        self.date_label = ctk.CTkLabel(
            self.time_frame,
            text="",
            font=("Helvetica", 16),
            text_color="#888888"
        )
        self.date_label.pack(pady=(0, 15))
        # Alarm time entry with modern design
        self.alarm_frame = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b", corner_radius=15)
        self.alarm_frame.pack(pady=5, padx=30, fill="x")
        # Alarm title
        ctk.CTkLabel(
            self.alarm_frame,
            text="Add New Alarm",
            font=("Helvetica", 18, "bold"),
            text_color="#ffffff"
        ).pack(pady=(10, 5))
        # Time input frame
        self.input_frame = ctk.CTkFrame(self.alarm_frame, fg_color="transparent")
        self.input_frame.pack(pady=5)
        self.hour_var = ctk.StringVar(value="00")
        self.minute_var = ctk.StringVar(value="00")
        # Hour entry with modern styling
        self.hour_entry = ctk.CTkEntry(
            self.input_frame,
            textvariable=self.hour_var,
            width=80,
            height=40,
            font=("Helvetica", 24, "bold"),
            corner_radius=10,
            fg_color="#3b3b3b",
            border_color="#4CAF50",
            text_color="#ffffff"
        )
        self.hour_entry.pack(side="left", padx=5)
        # Colon label
        ctk.CTkLabel(
            self.input_frame,
            text=":",
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff"
        ).pack(side="left", padx=5)
        # Minute entry with modern styling
        self.minute_entry = ctk.CTkEntry(
            self.input_frame,
            textvariable=self.minute_var,
            width=80,
            height=40,
            font=("Helvetica", 24, "bold"),
            corner_radius=10,
            fg_color="#3b3b3b",
            border_color="#4CAF50",
            text_color="#ffffff"
        )
        self.minute_entry.pack(side="left", padx=5)
        # Add alarm button with modern styling
        self.add_alarm_button = ctk.CTkButton(
            self.alarm_frame,
            text="Add Alarm",
            command=self.add_alarm,
            font=("Helvetica", 16, "bold"),
            height=40,
            corner_radius=10,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.add_alarm_button.pack(pady=10)
        # Alarms list frame
        self.alarms_frame = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b", corner_radius=15)
        self.alarms_frame.pack(pady=5, padx=30, fill="both", expand=False)
        # Alarms list title
        ctk.CTkLabel(
            self.alarms_frame,
            text="Active Alarms",
            font=("Helvetica", 18, "bold"),
            text_color="#ffffff"
        ).pack(pady=(10, 5))
        # Scrollable alarms list
        self.alarms_list_frame = ScrollableFrame(
            self.alarms_frame,
            fg_color="transparent",
            height=120
        )
        self.alarms_list_frame.pack(pady=5, padx=15, fill="both", expand=False)
        # Start clock update
        self.update_clock()

    def update_clock(self):
        current_time = datetime.datetime.now()
        self.date_label.configure(text=current_time.strftime("%A, %B %d, %Y"))
        
        # Find next alarm
        next_alarm = None
        min_delta = None
        
        for alarm in self.alarms:
            if not alarm.enabled:
                continue
                
            alarm_time = current_time.replace(hour=alarm.hour, minute=alarm.minute, second=0, microsecond=0)
            if alarm_time < current_time:
                alarm_time += datetime.timedelta(days=1)
                
            delta = alarm_time - current_time
            if min_delta is None or delta < min_delta:
                min_delta = delta
                next_alarm = alarm
        
        if next_alarm and min_delta:
            hours, remainder = divmod(int(min_delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.time_label.configure(text="No alarms set")
            
        self.after(1000, self.update_clock)

    def add_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Invalid time")
            # Create new alarm
            new_alarm = AlarmData(hour, minute)
            self.alarms.append(new_alarm)
            # Sort alarms
            self.alarms.sort(key=lambda a: (a.hour, a.minute))
            # Refresh alarm list display
            self.refresh_alarm_list()
            # Start alarm thread
            new_alarm.thread = Thread(target=self.check_alarm, args=(new_alarm,))
            new_alarm.thread.daemon = True
            new_alarm.thread.start()
            # Clear input fields
            self.hour_var.set("00")
            self.minute_var.set("00")
        except ValueError:
            self.show_error("Invalid time format")

    def refresh_alarm_list(self):
        for widget in self.alarms_list_frame.winfo_children():
            widget.destroy()
        for alarm in self.alarms:
            self.create_alarm_row(alarm)

    def create_alarm_row(self, alarm):
        frame = ctk.CTkFrame(self.alarms_list_frame, fg_color="#3b3b3b", corner_radius=10)
        frame.pack(pady=8, padx=8, fill="x")

        # Time label
        time_str = f"{alarm.hour:02d}:{alarm.minute:02d}"
        ctk.CTkLabel(
            frame,
            text=time_str,
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff"
        ).pack(side="left", padx=15, pady=12)

        # Toggle switch
        switch = ctk.CTkSwitch(
            frame,
            text="",
            command=lambda: self.toggle_alarm(alarm),
            width=40
        )
        switch.pack(side="right", padx=15)
        if alarm.enabled:
            switch.select()
        else:
            switch.deselect()

        # Delete button
        delete_btn = ctk.CTkButton(
            frame,
            text="✕",
            width=30,
            height=30,
            font=("Helvetica", 16, "bold"),
            fg_color="#f44336",
            hover_color="#da190b",
            command=lambda: self.delete_alarm(alarm, frame)
        )
        delete_btn.pack(side="right", padx=5)

    def toggle_alarm(self, alarm):
        alarm.enabled = not alarm.enabled
        if alarm.enabled and (not alarm.thread or not alarm.thread.is_alive()):
            alarm.thread = Thread(target=self.check_alarm, args=(alarm,))
            alarm.thread.daemon = True
            alarm.thread.start()

    def delete_alarm(self, alarm, frame):
        alarm.enabled = False
        self.alarms.remove(alarm)
        frame.destroy()
        # Refresh alarm list display
        self.refresh_alarm_list()

    def check_alarm(self, alarm):
        while alarm.enabled:
            current_time = datetime.datetime.now().time()
            if (current_time.hour == alarm.hour and 
                current_time.minute == alarm.minute):
                self.trigger_alarm(alarm)
                break
            time.sleep(1)

    def trigger_alarm(self, alarm):
        for _ in range(3):  # 3 beeps
            if not alarm.enabled:
                break
            winsound.Beep(1000, 1000)
            time.sleep(1)
        alarm.enabled = False

    def show_error(self, message):
        # Create error popup
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x150")
        error_window.grab_set()  # Make window modal

        ctk.CTkLabel(
            error_window,
            text=message,
            font=("Helvetica", 16),
            text_color="#f44336"
        ).pack(pady=20)

        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=100
        ).pack(pady=10)

if __name__ == "__main__":
    app = Alarm()
    app.mainloop() 
