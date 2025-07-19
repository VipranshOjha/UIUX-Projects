import tkinter as tk
from tkinter import messagebox
import math
import re
from typing import List, Dict, Optional, Tuple


class Calculator:
    """
    Enhanced Scientific Calculator with improved error handling, 
    history tracking, and keyboard support.
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize the calculator.
        
        Args:
            parent: The parent widget to contain the calculator
        """
        self.parent = parent
        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.last_was_operator = False
        self.last_was_equals = False
        self.angle_mode = "deg"  # "deg" or "rad"
        self.history: List[str] = []
        self.max_history = 20
        self.second_mode = False  # Track if we're in second function mode
        
        # Error messages for better user experience
        self.error_messages = {
            "division_by_zero": "Cannot divide by zero",
            "invalid_input": "Invalid input",
            "math_error": "Mathematical error",
            "overflow": "Number too large",
            "domain_error": "Invalid domain for function"
        }
        
        self.create_widgets()
        self.setup_keyboard_bindings()
        self.frame.pack_forget()  # Hide initially
    
    def create_widgets(self) -> None:
        """Create the calculator interface with improved styling."""
        self.frame = tk.Frame(self.parent, bg='#1a1a1a')
        
        # Create angle mode indicator and history button
        self.create_top_bar()
        
        # Display frame with improved styling
        self.create_display()
        
        # Button grid
        self.create_button_grid()
    
    def create_top_bar(self) -> None:
        """Create top bar with angle mode toggle and history button."""
        top_frame = tk.Frame(self.frame, bg='#1a1a1a', height=40)
        top_frame.pack(fill=tk.X, pady=(0, 5))
        top_frame.pack_propagate(False)
        
        # History button
        history_btn = tk.Button(
            top_frame,
            text="📋",
            font=('Arial', 12),
            bg='#333333',
            fg='white',
            activebackground='#555555',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.show_history
        )
        history_btn.pack(side=tk.LEFT, padx=5)
        
        # Angle mode toggle
        self.angle_btn = tk.Button(
            top_frame,
            text="DEG",
            font=('Arial', 10, 'bold'),
            bg='#666666',
            fg='white',
            activebackground='#888888',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.toggle_angle_mode
        )
        self.angle_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_display(self) -> None:
        """Create the calculator display with improved styling."""
        display_frame = tk.Frame(self.frame, bg='#2a2a2a', relief='sunken', bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Expression display (smaller, shows current expression)
        self.expression_var = tk.StringVar()
        self.expression_display = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=('Arial', 12),
            bg='#2a2a2a',
            fg='#888888',
            anchor='e',
            justify=tk.RIGHT,
            height=1
        )
        self.expression_display.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Main result display
        self.display = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 36, 'bold'),
            bg='#2a2a2a',
            fg='white',
            anchor='e',
            justify=tk.RIGHT,
            height=2
        )
        self.display.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def create_button_grid(self) -> None:
        """Create the button grid with symmetric layout and uniform button sizes."""
        # Button configurations in a 7x5 grid layout
        buttons = [
            ['2nd', 'deg', 'sin', 'cos', 'tan'],
            ['x^y', 'lg', 'ln', '(', ')'],
            ['√x', 'AC', '⌫', '%', '÷'],
            ['x!', '7', '8', '9', '×'],
            ['1/x', '4', '5', '6', '-'],
            ['π', '1', '2', '3', '+'],
            ['e', '0', '.', '=', '=']  # Extended last row to maintain 5 columns
        ]
        
        # Create button grid container
        button_container = tk.Frame(self.frame, bg='#1a1a1a')
        button_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid weights for uniform sizing
        for i in range(7):  # 7 rows
            button_container.grid_rowconfigure(i, weight=1)
        for j in range(5):  # 5 columns
            button_container.grid_columnconfigure(j, weight=1)
        
        # Create buttons in grid layout
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # Skip duplicate equals button
                if i == 6 and j == 4:
                    continue
                
                btn = self.create_button(button_container, text)
                
                # Handle equals button spanning two columns in the last row
                if text == '=' and i == 6:
                    btn.grid(row=i, column=j, columnspan=2, sticky='nsew', padx=2, pady=2)
                else:
                    btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
    
    def create_button(self, parent: tk.Widget, text: str) -> tk.Button:
        """
        Create a calculator button with improved styling and uniform size.
        
        Args:
            parent: Parent widget for the button
            text: Button text
            
        Returns:
            tk.Button: The created button
        """
        # Determine button style based on type
        if text in ['AC', '⌫', '%', '÷', '×', '-', '+', '=']:
            if text == '=':
                bg_color = '#ff9500'
                hover_color = '#ffad33'
            else:
                bg_color = '#ff9500'
                hover_color = '#ffad33'
        elif text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            bg_color = '#333333'
            hover_color = '#555555'
        else:
            bg_color = '#666666'
            hover_color = '#888888'
        
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 12, 'bold'),  # Slightly smaller font for better fit
            bg=bg_color,
            fg='white',
            activebackground=hover_color,
            activeforeground='white',
            border=0,
            cursor='hand2',
            relief='flat',
            width=6,  # Fixed width for uniformity
            height=2,  # Fixed height for uniformity
            command=lambda t=text: self.button_click(t)
        )
        
        # Add hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=hover_color))
        btn.bind('<Leave>', lambda e: btn.config(bg=bg_color))
        
        return btn
    
    def setup_keyboard_bindings(self) -> None:
        """Setup keyboard bindings for calculator input."""
        # Bind to the parent window
        self.parent.bind('<Key>', self.on_key_press)
        self.parent.focus_set()
        
        # Make sure the parent can receive focus
        self.parent.bind('<Button-1>', lambda e: self.parent.focus_set())
    
    def on_key_press(self, event) -> None:
        """
        Handle keyboard input.
        
        Args:
            event: The key press event
        """
        key = event.keysym
        char = event.char
        
        # Number keys
        if char.isdigit():
            self.button_click(char)
        # Operator keys
        elif char == '+':
            self.button_click('+')
        elif char == '-':
            self.button_click('-')
        elif char == '*':
            self.button_click('×')
        elif char == '/':
            self.button_click('÷')
        elif char == '%':
            self.button_click('%')
        elif char == '.':
            self.button_click('.')
        elif char == '(':
            self.button_click('(')
        elif char == ')':
            self.button_click(')')
        elif key == 'Return' or key == 'KP_Enter':
            self.button_click('=')
        elif key == 'Escape':
            self.button_click('AC')
        elif key == 'BackSpace':
            self.button_click('⌫')
    
    def button_click(self, text: str) -> None:
        """
        Handle button clicks with improved logic.
        
        Args:
            text: The button text that was clicked
        """
        try:
            if text == 'AC':
                self.clear_all()
            elif text == '⌫':
                self.backspace()
            elif text == '=':
                self.calculate()
            elif text in ['+', '-', '×', '÷', '%']:
                self.add_operator(text)
            elif text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.add_number(text)
            elif text == '.':
                self.add_decimal()
            elif text == 'π':
                self.add_constant('π')
            elif text == 'e':
                self.add_constant('e')
            elif text in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹']:
                self.add_function(text)
            elif text == 'ln':
                self.add_function('ln')
            elif text == 'lg':
                self.add_function('lg')
            elif text == '√x':
                self.add_function('sqrt')
            elif text == 'x!':
                self.add_function('factorial')
            elif text == '1/x':
                self.add_function('reciprocal')
            elif text == 'x^y':
                self.add_operator('^')
            elif text == '(':
                self.add_bracket('(')
            elif text == ')':
                self.add_bracket(')')
            elif text == 'deg':
                self.toggle_angle_mode()
            elif text == '2nd':
                self.toggle_second_functions()
        except Exception as e:
            self.show_error("Invalid operation")
    
    def clear_all(self) -> None:
        """Clear all input and reset calculator state."""
        self.expression = ""
        self.result_var.set("0")
        self.expression_var.set("")
        self.last_was_operator = False
        self.last_was_equals = False
    
    def backspace(self) -> None:
        """Remove the last character from the expression."""
        if self.expression:
            self.expression = self.expression[:-1]
            self.update_display()
    
    def add_number(self, number: str) -> None:
        """
        Add a number to the expression.
        
        Args:
            number: The number to add
        """
        if self.last_was_equals:
            self.expression = ""
            self.last_was_equals = False
        
        self.expression += number
        self.update_display()
        self.last_was_operator = False
    
    def add_operator(self, operator: str) -> None:
        """
        Add an operator to the expression.
        
        Args:
            operator: The operator to add
        """
        if self.last_was_equals:
            self.last_was_equals = False
        
        if self.expression and not self.last_was_operator:
            # Convert display operators to calculation operators
            if operator == '×':
                self.expression += '*'
            elif operator == '÷':
                self.expression += '/'
            elif operator == '^':
                self.expression += '**'
            else:
                self.expression += operator
            
            self.update_display()
            self.last_was_operator = True
        elif self.expression and self.last_was_operator:
            # Replace the last operator
            self.expression = self.expression[:-1]
            if operator == '×':
                self.expression += '*'
            elif operator == '÷':
                self.expression += '/'
            elif operator == '^':
                self.expression += '**'
            else:
                self.expression += operator
            self.update_display()
    
    def add_decimal(self) -> None:
        """Add a decimal point to the current number."""
        if self.last_was_equals:
            self.expression = ""
            self.last_was_equals = False
        
        # Find the last number in the expression
        parts = re.split(r'[+\-*/()]', self.expression)
        if parts and '.' not in parts[-1]:
            if not parts[-1] or parts[-1][-1] in '+-*/%^(':
                self.expression += '0.'
            else:
                self.expression += '.'
            self.update_display()
            self.last_was_operator = False
    
    def add_constant(self, constant: str) -> None:
        """
        Add a mathematical constant to the expression.
        
        Args:
            constant: The constant to add ('π' or 'e')
        """
        if self.last_was_equals:
            self.expression = ""
            self.last_was_equals = False
        
        # Add multiplication if needed
        if self.expression and self.expression[-1] not in '+-*/%^(':
            self.expression += '*'
        
        if constant == 'π':
            self.expression += str(math.pi)
        elif constant == 'e':
            self.expression += str(math.e)
        
        self.update_display()
        self.last_was_operator = False
    
    def add_function(self, function: str) -> None:
        """
        Add a mathematical function to the expression.
        
        Args:
            function: The function to add
        """
        if self.last_was_equals:
            # If we just calculated, apply function to result
            if function == 'factorial':
                self.expression += "!"
            elif function == 'reciprocal':
                self.expression = f"1/({self.expression})"
            else:
                self.expression = f"{function}({self.expression})"
            self.last_was_equals = False
        else:
            if function in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'ln', 'lg', 'sqrt']:
                # Add multiplication if needed
                if self.expression and self.expression[-1] not in '+-*/%^(':
                    self.expression += '*'
                self.expression += f"{function}("
            elif function == 'factorial':
                if self.expression and self.expression[-1] not in '+-*/%^(':
                    self.expression += "!"
            elif function == 'reciprocal':
                if self.expression:
                    # Wrap current expression in reciprocal
                    self.expression = f"1/({self.expression})"
        
        self.update_display()
        self.last_was_operator = False
    
    def add_bracket(self, bracket: str) -> None:
        """
        Add a bracket to the expression.
        
        Args:
            bracket: The bracket to add ('(' or ')')
        """
        if self.last_was_equals:
            self.expression = ""
            self.last_was_equals = False
        
        if bracket == '(':
            # Add multiplication if needed
            if self.expression and self.expression[-1] not in '+-*/%^(':
                self.expression += '*'
        
        self.expression += bracket
        self.update_display()
        self.last_was_operator = False
    
    def toggle_angle_mode(self) -> None:
        """Toggle between degrees and radians for trigonometric functions."""
        if self.angle_mode == "deg":
            self.angle_mode = "rad"
            self.angle_btn.config(text="RAD")
        else:
            self.angle_mode = "deg"
            self.angle_btn.config(text="DEG")
    
    def toggle_second_functions(self) -> None:
        """Toggle second functions (inverse trig functions)."""
        self.second_mode = not self.second_mode
        self.update_button_labels()

    def update_button_labels(self) -> None:
        """Update button labels based on current mode."""
        # Find and update the trig function buttons
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        current_text = child.cget('text')
                        if self.second_mode:
                            if current_text == 'sin':
                                child.config(text='sin⁻¹')
                            elif current_text == 'cos':
                                child.config(text='cos⁻¹')
                            elif current_text == 'tan':
                                child.config(text='tan⁻¹')
                        else:
                            if current_text == 'sin⁻¹':
                                child.config(text='sin')
                            elif current_text == 'cos⁻¹':
                                child.config(text='cos')
                            elif current_text == 'tan⁻¹':
                                child.config(text='tan')
    
    def calculate(self) -> None:
        """Calculate the result of the expression with improved error handling."""
        try:
            if not self.expression:
                return
            
            # Prepare expression for calculation
            calc_expression = self.prepare_expression()
            
            # Evaluate the expression
            result = eval(calc_expression, {"__builtins__": {}}, {
                "math": math,
                "sin": self.safe_sin,
                "cos": self.safe_cos,
                "tan": self.safe_tan,
                "ln": self.safe_ln,
                "lg": self.safe_lg,
                "sqrt": self.safe_sqrt,
                "factorial": self.safe_factorial,
                "pi": math.pi,
                "e": math.e,
                "sin⁻¹": self.safe_asin,
                "cos⁻¹": self.safe_acos,
                "tan⁻¹": self.safe_atan
            })
            
            # Format result
            formatted_result = self.format_result(result)
            
            # Add to history
            self.add_to_history(f"{self.expression} = {formatted_result}")
            
            # Update display
            self.result_var.set(formatted_result)
            self.expression_var.set(self.expression)
            self.expression = str(result)
            self.last_was_equals = True
            self.last_was_operator = False
            
        except ZeroDivisionError:
            self.show_error(self.error_messages["division_by_zero"])
        except ValueError as e:
            if "math domain error" in str(e).lower():
                self.show_error(self.error_messages["domain_error"])
            else:
                self.show_error(self.error_messages["invalid_input"])
        except OverflowError:
            self.show_error(self.error_messages["overflow"])
        except Exception as e:
            self.show_error(self.error_messages["math_error"])
    
    def prepare_expression(self) -> str:
        """
        Prepare the expression for evaluation by replacing custom functions.
        
        Returns:
            str: The prepared expression
        """
        calc_expression = self.expression
        
        # Replace custom functions
        calc_expression = calc_expression.replace('sin(', 'sin(')
        calc_expression = calc_expression.replace('cos(', 'cos(')
        calc_expression = calc_expression.replace('tan(', 'tan(')
        calc_expression = calc_expression.replace('ln(', 'ln(')
        calc_expression = calc_expression.replace('lg(', 'lg(')
        calc_expression = calc_expression.replace('sqrt(', 'sqrt(')
        calc_expression = calc_expression.replace('sin⁻¹(', 'sin⁻¹(')
        calc_expression = calc_expression.replace('cos⁻¹(', 'cos⁻¹(')
        calc_expression = calc_expression.replace('tan⁻¹(', 'tan⁻¹(')
        
        # Handle factorial
        calc_expression = self.handle_factorial(calc_expression)
        
        return calc_expression
    
    def handle_factorial(self, expression: str) -> str:
        """
        Handle factorial operations in the expression.
        
        Args:
            expression: The expression containing factorial operations
            
        Returns:
            str: The expression with factorial operations converted
        """
        # Simple factorial handling - can be improved
        if '!' in expression:
            # This is a simplified approach
            parts = expression.split('!')
            if len(parts) == 2:
                number_part = parts[0]
                # Extract the last number
                import re
                match = re.search(r'(\d+)$', number_part)
                if match:
                    num = match.group(1)
                    expression = expression.replace(f'{num}!', f'factorial({num})')
        
        return expression
    
    def safe_sin(self, x: float) -> float:
        """Safe sine function with angle mode support."""
        if self.angle_mode == "deg":
            x = math.radians(x)
        return math.sin(x)
    
    def safe_cos(self, x: float) -> float:
        """Safe cosine function with angle mode support."""
        if self.angle_mode == "deg":
            x = math.radians(x)
        return math.cos(x)
    
    def safe_tan(self, x: float) -> float:
        """Safe tangent function with angle mode support."""
        if self.angle_mode == "deg":
            x = math.radians(x)
        return math.tan(x)
    
    def safe_ln(self, x: float) -> float:
        """Safe natural logarithm function."""
        if x <= 0:
            raise ValueError("Math domain error")
        return math.log(x)
    
    def safe_lg(self, x: float) -> float:
        """Safe base-10 logarithm function."""
        if x <= 0:
            raise ValueError("Math domain error")
        return math.log10(x)
    
    def safe_sqrt(self, x: float) -> float:
        """Safe square root function."""
        if x < 0:
            raise ValueError("Math domain error")
        return math.sqrt(x)
    
    def safe_factorial(self, x: float) -> float:
        """Safe factorial function."""
        if x < 0 or x != int(x):
            raise ValueError("Math domain error")
        return math.factorial(int(x))
    
    def safe_asin(self, x: float) -> float:
        """Safe arcsine function with angle mode support."""
        if x < -1 or x > 1:
            raise ValueError("Math domain error")
        result = math.asin(x)
        if self.angle_mode == "deg":
            result = math.degrees(result)
        return result

    def safe_acos(self, x: float) -> float:
        """Safe arccosine function with angle mode support."""
        if x < -1 or x > 1:
            raise ValueError("Math domain error")
        result = math.acos(x)
        if self.angle_mode == "deg":
            result = math.degrees(result)
        return result

    def safe_atan(self, x: float) -> float:
        """Safe arctangent function with angle mode support."""
        result = math.atan(x)
        if self.angle_mode == "deg":
            result = math.degrees(result)
        return result
    
    def format_result(self, result: float) -> str:
        """
        Format the result for display.
        
        Args:
            result: The calculation result
            
        Returns:
            str: The formatted result
        """
        if isinstance(result, (int, float)):
            if abs(result) > 1e15:
                return f"{result:.4e}"
            elif abs(result) < 1e-10 and result != 0:
                return f"{result:.4e}"
            elif result == int(result):
                return str(int(result))
            else:
                # Format with appropriate decimal places
                formatted = f"{result:.10f}".rstrip('0').rstrip('.')
                return formatted
        return str(result)
    
    def update_display(self) -> None:
        """Update the calculator display."""
        display_expr = self.expression
        # Replace operators for display
        display_expr = display_expr.replace('*', '×')
        display_expr = display_expr.replace('/', '÷')
        display_expr = display_expr.replace('**', '^')
        
        self.result_var.set(display_expr if display_expr else "0")
        self.expression_var.set("")
    
    def show_error(self, message: str) -> None:
        """
        Show an error message and reset the calculator.
        
        Args:
            message: The error message to display
        """
        self.result_var.set(message)
        self.expression_var.set("")
        self.expression = ""
        self.last_was_equals = False
        self.last_was_operator = False
    
    def add_to_history(self, calculation: str) -> None:
        """
        Add a calculation to the history.
        
        Args:
            calculation: The calculation to add to history
        """
        self.history.append(calculation)
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def show_history(self) -> None:
        """Show the calculation history in a popup window."""
        if not self.history:
            messagebox.showinfo("History", "No calculations in history")
            return
        
        history_window = tk.Toplevel(self.parent)
        history_window.title("Calculation History")
        history_window.geometry("400x300")
        history_window.configure(bg='#1a1a1a')
        
        # Create scrollable text widget
        frame = tk.Frame(history_window, bg='#1a1a1a')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            frame,
            bg='#2a2a2a',
            fg='white',
            font=('Arial', 10),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Add history items
        for i, calc in enumerate(reversed(self.history)):
            text_widget.insert(tk.END, f"{len(self.history) - i}. {calc}\n")
        
        text_widget.config(state=tk.DISABLED)
        
        # Clear history button
        clear_btn = tk.Button(
            history_window,
            text="Clear History",
            font=('Arial', 10),
            bg='#ff4444',
            fg='white',
            command=lambda: (self.clear_history(), history_window.destroy())
        )
        clear_btn.pack(pady=5)
    
    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.history.clear()
    
    def show(self) -> None:
        """Show the calculator interface."""
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.parent.focus_set()  # Ensure keyboard bindings work
    
    def hide(self) -> None:
        """Hide the calculator interface."""
        self.frame.pack_forget()