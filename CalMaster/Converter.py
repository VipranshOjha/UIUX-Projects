import tkinter as tk
from tkinter import ttk
import math

class Converter:
    def __init__(self, parent):
        self.parent = parent
        self.current_converter = None
        self.frame = tk.Frame(self.parent, bg='#1a1a1a')  # Only create ONCE
        self.create_widgets()
        self.frame.pack_forget()  # Hide initially

    def create_widgets(self):
        """Create converter interface"""
        # Only clear children, do NOT recreate self.frame!
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Converter categories
        categories = [
            ('Currency', '🪙'),
            ('Length', '📏'),
            ('Mass', '⚖️'),
            ('Area', '⬜'),
            ('Time', '🕐'),
            ('Finance', '💰'),
            ('Data', '💾'),
            ('Date', '📅'),
            ('Discount', '🏷️'),
            ('Volume', '📦'),
            ('Numeral system', '🔢'),
            ('Speed', '⚡'),
            ('Temperature', '🌡️'),
            ('BMI', '👤'),
            ('GST', '🧾')
        ]
        
        # Create grid of converter buttons
        for i, (name, icon) in enumerate(categories):
            row = i // 3
            col = i % 3
            
            button_frame = tk.Frame(self.frame, bg='#1a1a1a')
            button_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Configure grid weights
            self.frame.grid_rowconfigure(row, weight=1)
            self.frame.grid_columnconfigure(col, weight=1)
            
            btn = tk.Button(
                button_frame,
                text=f"{icon}\n{name}",
                font=('Arial', 12),
                bg='#333333',
                fg='white',
                activebackground='#555555',
                activeforeground='white',
                border=0,
                cursor='hand2',
                width=12,
                height=4,
                command=lambda n=name: self.open_converter(n)
            )
            btn.pack(fill=tk.BOTH, expand=True)
    
    def open_converter(self, converter_type):
        """Open specific converter"""
        self.current_converter = converter_type
        self.show_converter_interface(converter_type)
    
    def show_converter_interface(self, converter_type):
        """Show the conversion interface for specific type"""
        # Clear current frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create back button
        back_btn = tk.Button(
            self.frame,
            text="← Back",
            font=('Arial', 12),
            bg='#333333',
            fg='white',
            activebackground='#555555',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.go_back
        )
        back_btn.pack(anchor='w', padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            self.frame,
            text=f"{converter_type} Converter",
            font=('Arial', 18, 'bold'),
            bg='#1a1a1a',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Create converter based on type
        if converter_type == 'Temperature':
            self.create_temperature_converter()
        elif converter_type == 'Length':
            self.create_length_converter()
        elif converter_type == 'Mass':
            self.create_mass_converter()
        elif converter_type == 'Currency':
            self.create_currency_converter()
        elif converter_type == 'Time':
            self.create_time_converter()
        elif converter_type == 'Area':
            self.create_area_converter()
        elif converter_type == 'Volume':
            self.create_volume_converter()
        elif converter_type == 'Speed':
            self.create_speed_converter()
        elif converter_type == 'Data':
            self.create_data_converter()
        elif converter_type == 'BMI':
            self.create_bmi_calculator()
        elif converter_type == 'GST':
            self.create_gst_calculator()
        elif converter_type == 'Discount':
            self.create_discount_calculator()
        elif converter_type == 'Numeral system':
            self.create_numeral_converter()
        else:
            # Generic converter
            self.create_generic_converter(converter_type)
    
    def create_input_row(self, parent, label, var, values, entry_widget):
        """Helper to create a labeled row with a combobox and entry."""
        row = tk.Frame(parent, bg="#1a1a1a")
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text=label, font=("Arial", 12), bg="#1a1a1a", fg="white", width=7, anchor="w").pack(side=tk.LEFT, padx=(0, 8))
        combo = ttk.Combobox(row, textvariable=var, values=values, state="readonly", width=12)
        combo.pack(side=tk.LEFT, padx=(0, 8))
        entry_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        combo.bind("<<ComboboxSelected>>", self.convert_temperature)

    def create_temperature_converter(self):
        units = ["Celsius", "Fahrenheit", "Kelvin"]
        frame = tk.Frame(self.frame, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.temp_from = tk.StringVar(value="Celsius")
        self.temp_to = tk.StringVar(value="Fahrenheit")
        self.temp_entry = tk.Entry(frame, font=("Arial", 16), bg="#555555", fg="white", insertbackground="white")
        self.temp_result = tk.Entry(frame, font=("Arial", 16), bg="#2a2a2a", fg="white", insertbackground="white", state="readonly")

        self.create_input_row(frame, "From:", self.temp_from, units, self.temp_entry)
        self.create_input_row(frame, "To:", self.temp_to, units, self.temp_result)

        self.temp_entry.bind("<KeyRelease>", self.convert_temperature)

    def convert_temperature(self, event=None):
        try:
            val = float(self.temp_entry.get())
            f, t = self.temp_from.get(), self.temp_to.get()
            if f == t:
                result = val
            else:
                c = (val - 32) * 5/9 if f == "Fahrenheit" else val - 273.15 if f == "Kelvin" else val
                result = c * 9/5 + 32 if t == "Fahrenheit" else c + 273.15 if t == "Kelvin" else c
            self.temp_result.config(state="normal")
            self.temp_result.delete(0, tk.END)
            self.temp_result.insert(0, f"{result:.2f}")
            self.temp_result.config(state="readonly")
        except ValueError:
            self.temp_result.config(state="normal")
            self.temp_result.delete(0, tk.END)
            self.temp_result.insert(0, "Invalid")
            self.temp_result.config(state='readonly')
    
    def create_length_converter(self):
        self.create_unit_converter("Length", {
            "Millimeter": 0.001,
            "Centimeter": 0.01,
            "Meter": 1,
            "Kilometer": 1000,
            "Inch": 0.0254,
            "Foot": 0.3048,
            "Yard": 0.9144,
            "Mile": 1609.34
        })
    
    def create_mass_converter(self):
        self.create_unit_converter("Mass", {
            "Milligram": 0.001,
            "Gram": 1,
            "Kilogram": 1000,
            "Ounce": 28.3495,
            "Pound": 453.592,
            "Ton": 1000000
        })
    
    def create_currency_converter(self):
        """Create currency converter (simplified)"""
        self.create_unit_converter('Currency', {
            'USD': 1,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110,
            'INR': 74.5,
            'CAD': 1.25,
            'AUD': 1.35
        })
    
    def create_time_converter(self):
        """Create time converter"""
        self.create_unit_converter('Time', {
            'Second': 1,
            'Minute': 60,
            'Hour': 3600,
            'Day': 86400,
            'Week': 604800,
            'Month': 2592000,
            'Year': 31536000
        })
    
    def create_area_converter(self):
        """Create area converter"""
        self.create_unit_converter("Area", {
            "Square Millimeter": 1e-6,
            "Square Centimeter": 1e-4,
            "Square Meter": 1,
            "Square Kilometer": 1e6,
            "Square Inch": 0.00064516,
            "Square Foot": 0.092903,
            "Square Yard": 0.836127,
            "Acre": 4046.86,
            "Hectare": 10000
        })
    
    def create_volume_converter(self):
        """Create volume converter"""
        self.create_unit_converter("Volume", {
            "Milliliter": 0.001,
            "Liter": 1,
            "Cubic Meter": 1000,
            "Gallon (US)": 3.78541,
            "Gallon (UK)": 4.54609,
            "Fluid Ounce": 0.0295735,
            "Cup": 0.236588,
            "Pint": 0.473176,
            "Quart": 0.946353
        })
    
    def create_speed_converter(self):
        """Create speed converter"""
        self.create_unit_converter("Speed", {
            "Meter/sec": 1,
            "Km/hr": 0.277778,
            "Mile/hr": 0.44704,
            "Foot/sec": 0.3048,
            "Knot": 0.514444
        })
    
    def create_data_converter(self):
        """Create data converter"""
        self.create_unit_converter("Data", {
            "Bit": 1,
            "Byte": 8,
            "Kilobyte": 8192,
            "Megabyte": 8388608,
            "Gigabyte": 8589934592,
            "Terabyte": 8796093022208
        })
    
    def create_unit_converter(self, unit_type, conversions):
        """Create a generic unit converter"""
        converter_frame = tk.Frame(self.frame, bg='#1a1a1a')
        converter_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # From section
        from_frame = tk.Frame(converter_frame, bg='#333333')
        from_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(from_frame, text="From:", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        
        self.from_var = tk.StringVar(value=list(conversions.keys())[0])
        from_combo = ttk.Combobox(from_frame, textvariable=self.from_var, values=list(conversions.keys()), state='readonly')
        from_combo.pack(fill=tk.X, padx=10, pady=5)
        
        self.from_entry = tk.Entry(from_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.from_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # To section
        to_frame = tk.Frame(converter_frame, bg='#333333')
        to_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(to_frame, text="To:", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        
        self.to_var = tk.StringVar(value=list(conversions.keys())[1] if len(conversions) > 1 else list(conversions.keys())[0])
        to_combo = ttk.Combobox(to_frame, textvariable=self.to_var, values=list(conversions.keys()), state='readonly')
        to_combo.pack(fill=tk.X, padx=10, pady=5)
        
        self.to_entry = tk.Entry(
            to_frame,
            font=('Arial', 14),
            bg='#2a2a2a',  # Match calculator result display background
            fg='white',
            insertbackground='white',
            state='readonly',
            justify='right'
        )
        self.to_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Store conversions for later use
        self.conversions = conversions
        
        # Bind events
        self.from_entry.bind('<KeyRelease>', self.convert_units)
        from_combo.bind('<<ComboboxSelected>>', self.convert_units)
        to_combo.bind('<<ComboboxSelected>>', self.convert_units)
    
    def convert_units(self, event=None):
        """Convert between units"""
        try:
            value = float(self.from_entry.get())
            from_unit = self.from_var.get()
            to_unit = self.to_var.get()
            
            # Convert to base unit first, then to target unit
            base_value = value * self.conversions[from_unit]
            result = base_value / self.conversions[to_unit]
            
            self.to_entry.config(state='normal')
            self.to_entry.delete(0, tk.END)
            self.to_entry.insert(0, f"{result:.6f}".rstrip('0').rstrip('.'))
            self.to_entry.config(state='readonly')
            
        except (ValueError, KeyError):
            self.to_entry.config(state='normal')
            self.to_entry.delete(0, tk.END)
            self.to_entry.config(state='readonly')
    
    def create_bmi_calculator(self):
        """Create BMI calculator"""
        converter_frame = tk.Frame(self.frame, bg='#1a1a1a')
        converter_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Height input
        height_frame = tk.Frame(converter_frame, bg='#333333')
        height_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(height_frame, text="Height (cm):", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        self.height_entry = tk.Entry(height_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.height_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Weight input
        weight_frame = tk.Frame(converter_frame, bg='#333333')
        weight_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(weight_frame, text="Weight (kg):", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        self.weight_entry = tk.Entry(weight_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.weight_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Calculate button
        calc_btn = tk.Button(
            converter_frame,
            text="Calculate BMI",
            font=('Arial', 12),
            bg='#ff9500',
            fg='white',
            activebackground='#cc7700',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.calculate_bmi
        )
        calc_btn.pack(pady=20)
        
        # Result display
        self.bmi_result = tk.Label(
            converter_frame,
            text="BMI: --",
            font=('Arial', 16, 'bold'),
            bg='#1a1a1a',
            fg='white'
        )
        self.bmi_result.pack(pady=10)
        
        self.bmi_category = tk.Label(
            converter_frame,
            text="Category: --",
            font=('Arial', 12),
            bg='#1a1a1a',
            fg='white'
        )
        self.bmi_category.pack(pady=5)
    
    def calculate_bmi(self):
        """Calculate BMI"""
        try:
            height = float(self.height_entry.get()) / 100  # Convert cm to meters
            weight = float(self.weight_entry.get())
            
            bmi = weight / (height ** 2)
            
            # Determine category
            if bmi < 18.5:
                category = "Underweight"
                color = "#3498db"
            elif bmi < 25:
                category = "Normal weight"
                color = "#2ecc71"
            elif bmi < 30:
                category = "Overweight"
                color = "#f39c12"
            else:
                category = "Obese"
                color = "#e74c3c"
            
            self.bmi_result.config(text=f"BMI: {bmi:.1f}")
            self.bmi_category.config(text=f"Category: {category}", fg=color)
            
        except ValueError:
            self.bmi_result.config(text="BMI: Error")
            self.bmi_category.config(text="Category: Invalid input", fg="#e74c3c")
    
    def create_gst_calculator(self):
        """Create GST calculator"""
        converter_frame = tk.Frame(self.frame, bg='#1a1a1a')
        converter_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Amount input
        amount_frame = tk.Frame(converter_frame, bg='#333333')
        amount_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(amount_frame, text="Amount:", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        self.gst_amount_entry = tk.Entry(amount_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.gst_amount_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # GST rate input
        rate_frame = tk.Frame(converter_frame, bg='#333333')
        rate_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(rate_frame, text="GST Rate (%):", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        self.gst_rate_var = tk.StringVar(value="18")
        rate_combo = ttk.Combobox(rate_frame, textvariable=self.gst_rate_var, values=['5', '12', '18', '28'], state='readonly')
        rate_combo.pack(fill=tk.X, padx=10, pady=5)
        
        # Calculate button
        calc_btn = tk.Button(
            converter_frame,
            text="Calculate GST",
            font=('Arial', 12),
            bg='#ff9500',
            fg='white',
            activebackground='#cc7700',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.calculate_gst
        )
        calc_btn.pack(pady=20)
        
        # Results
        self.gst_amount_result = tk.Label(converter_frame, text="GST Amount: --", font=('Arial', 12), bg='#1a1a1a', fg='white')
        self.gst_amount_result.pack(pady=5)
        
        self.gst_total_result = tk.Label(converter_frame, text="Total Amount: --", font=('Arial', 12), bg='#1a1a1a', fg='white')
        self.gst_total_result.pack(pady=5)
    
    def calculate_gst(self):
        """Calculate GST"""
        try:
            amount = float(self.gst_amount_entry.get())
            rate = float(self.gst_rate_var.get())
            
            gst_amount = amount * (rate / 100)
            total_amount = amount + gst_amount
            
            self.gst_amount_result.config(text=f"GST Amount: ₹{gst_amount:.2f}")
            self.gst_total_result.config(text=f"Total Amount: ₹{total_amount:.2f}")
            
        except ValueError:
            self.gst_amount_result.config(text="GST Amount: Error")
            self.gst_total_result.config(text="Total Amount: Error")
    
    def create_discount_calculator(self):
        """Create discount calculator"""
        converter_frame = tk.Frame(self.frame, bg='#1a1a1a')
        converter_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Original price input
        price_frame = tk.Frame(converter_frame, bg='#333333')
        price_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(price_frame, text="Original Price:", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        self.original_price_entry = tk.Entry(price_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.original_price_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Discount rate input
        discount_frame = tk.Frame(converter_frame, bg='#333333')
        discount_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(discount_frame, text="Discount (%):", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        self.discount_rate_entry = tk.Entry(discount_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.discount_rate_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Calculate button
        calc_btn = tk.Button(
            converter_frame,
            text="Calculate Discount",
            font=('Arial', 12),
            bg='#ff9500',
            fg='white',
            activebackground='#cc7700',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.calculate_discount
        )
        calc_btn.pack(pady=20)
        
        # Results
        self.discount_amount_result = tk.Label(converter_frame, text="Discount Amount: --", font=('Arial', 12), bg='#1a1a1a', fg='white')
        self.discount_amount_result.pack(pady=5)
        
        self.final_price_result = tk.Label(converter_frame, text="Final Price: --", font=('Arial', 12), bg='#1a1a1a', fg='white')
        self.final_price_result.pack(pady=5)
    
    def calculate_discount(self):
        """Calculate discount"""
        try:
            original_price = float(self.original_price_entry.get())
            discount_rate = float(self.discount_rate_entry.get())
            
            discount_amount = original_price * (discount_rate / 100)
            final_price = original_price - discount_amount
            
            self.discount_amount_result.config(text=f"Discount Amount: ₹{discount_amount:.2f}")
            self.final_price_result.config(text=f"Final Price: ₹{final_price:.2f}")
            
        except ValueError:
            self.discount_amount_result.config(text="Discount Amount: Error")
            self.final_price_result.config(text="Final Price: Error")
    
    def create_numeral_converter(self):
        """Create numeral system converter"""
        converter_frame = tk.Frame(self.frame, bg='#1a1a1a')
        converter_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # From section
        from_frame = tk.Frame(converter_frame, bg='#333333')
        from_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(from_frame, text="From:", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        
        self.num_from_var = tk.StringVar(value="Decimal")
        from_combo = ttk.Combobox(from_frame, textvariable=self.num_from_var, values=['Binary', 'Decimal', 'Hexadecimal', 'Octal'], state='readonly')
        from_combo.pack(fill=tk.X, padx=10, pady=5)
        
        self.num_from_entry = tk.Entry(from_frame, font=('Arial', 14), bg='#555555', fg='white', insertbackground='white')
        self.num_from_entry.pack(fill=tk.X, padx=10, pady=5)
        self.num_from_entry.bind('<KeyRelease>', self.convert_numeral)
        
        # To section
        to_frame = tk.Frame(converter_frame, bg='#333333')
        to_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(to_frame, text="To:", font=('Arial', 12), bg='#333333', fg='white').pack(anchor='w', padx=10, pady=5)
        
        self.num_to_var = tk.StringVar(value="Binary")
        to_combo = ttk.Combobox(to_frame, textvariable=self.num_to_var, values=['Binary', 'Decimal', 'Hexadecimal', 'Octal'], state='readonly')
        to_combo.pack(fill=tk.X, padx=10, pady=5)
        to_combo.bind('<<ComboboxSelected>>', self.convert_numeral)
        from_combo.bind('<<ComboboxSelected>>', self.convert_numeral)
        
        self.num_to_entry = tk.Entry(
            to_frame,
            font=('Arial', 14),
            bg='#2a2a2a',  # Match calculator result display background
            fg='white',
            insertbackground='white',
            state='readonly',
            justify='right'
        )
        self.num_to_entry.pack(fill=tk.X, padx=10, pady=5)
    
    def convert_numeral(self, event=None):
        """Convert between numeral systems"""
        try:
            value = self.num_from_entry.get().strip()
            from_base = self.num_from_var.get()
            to_base = self.num_to_var.get()
            
            if not value:
                self.num_to_entry.config(state='normal')
                self.num_to_entry.delete(0, tk.END)
                self.num_to_entry.config(state='readonly')
                return
            
            # Convert to decimal first
            if from_base == 'Binary':
                decimal_value = int(value, 2)
            elif from_base == 'Decimal':
                decimal_value = int(value)
            elif from_base == 'Hexadecimal':
                decimal_value = int(value, 16)
            elif from_base == 'Octal':
                decimal_value = int(value, 8)
            
            # Convert from decimal to target base
            if to_base == 'Binary':
                result = bin(decimal_value)[2:]
            elif to_base == 'Decimal':
                result = str(decimal_value)
            elif to_base == 'Hexadecimal':
                result = hex(decimal_value)[2:].upper()
            elif to_base == 'Octal':
                result = oct(decimal_value)[2:]
            
            self.num_to_entry.config(state='normal')
            self.num_to_entry.delete(0, tk.END)
            self.num_to_entry.insert(0, result)
            self.num_to_entry.config(state='readonly')
            
        except ValueError:
            self.num_to_entry.config(state='normal')
            self.num_to_entry.delete(0, tk.END)
            self.num_to_entry.insert(0, "Invalid input")
            self.num_to_entry.config(state='readonly')
    
    def create_generic_converter(self, converter_type):
        """Create a generic converter interface"""
        converter_frame = tk.Frame(self.frame, bg='#1a1a1a')
        converter_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_label = tk.Label(
            converter_frame,
            text=f"{converter_type} converter\nComing soon!",
            font=('Arial', 14),
            bg='#1a1a1a',
            fg='white',
            justify=tk.CENTER
        )
        info_label.pack(expand=True)
    
    def go_back(self):
        """Go back to main converter menu"""
        # Clear current frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Recreate main converter interface
        self.create_widgets()
        self.frame.pack(fill=tk.BOTH, expand=True)  
    
    def show(self):
        """Show the converter"""
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Hide the converter"""
        self.frame.pack_forget()

