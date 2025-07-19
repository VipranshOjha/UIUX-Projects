import tkinter as tk
from tkinter import ttk
from Calculator import Calculator
from Converter import Converter

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator & Converter")
        self.root.geometry("400x600")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='#1a1a1a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header with navigation buttons
        self.create_header()
        
        # Create content frame
        self.content_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize calculator and converter
        self.calculator = Calculator(self.content_frame)
        self.converter = Converter(self.content_frame)
        
        # Show calculator by default
        self.show_calculator()
        
    def create_header(self):
        """Create the header with navigation buttons"""
        header_frame = tk.Frame(self.main_frame, bg='#1a1a1a', height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Create a container frame for centering the buttons
        button_container = tk.Frame(header_frame, bg='#1a1a1a')
        button_container.pack(expand=True)
        
        # Calculator button
        self.calc_button = tk.Button(
            button_container,
            text="Calculator",
            font=('Arial', 14, 'bold'),
            bg='#1a1a1a',
            fg='white',
            activebackground='#333333',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.show_calculator
        )
        self.calc_button.pack(side=tk.LEFT, padx=20)
        
        # Converter button
        self.conv_button = tk.Button(
            button_container,
            text="Converter",
            font=('Arial', 14),
            bg='#1a1a1a',
            fg='#666666',
            activebackground='#333333',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.show_converter
        )
        self.conv_button.pack(side=tk.LEFT, padx=20)

    def show_calculator(self):
        """Show calculator interface"""
        self.calculator.show()
        self.converter.hide()
        
        # Update button styles
        self.calc_button.config(font=('Arial', 14, 'bold'), fg='white')
        self.conv_button.config(font=('Arial', 14), fg='#666666')
    
    def show_converter(self):
        """Show converter interface"""
        self.converter.show()
        self.calculator.hide()
        
        # Update button styles
        self.calc_button.config(font=('Arial', 14), fg='#666666')
        self.conv_button.config(font=('Arial', 14, 'bold'), fg='white')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()