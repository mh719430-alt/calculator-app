import tkinter as tk


expression = ""
current_language = "ar"
history_entries = []
history_list = None

ARABIC_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def format_for_language(value):
    text = str(value)
    if current_language == "ar":
        return text.translate(ARABIC_DIGITS)
    return text


def update_display(value):
    display.delete(0, tk.END)
    display.insert(0, format_for_language(value))


def show_welcome():
    message = (
        "مرحبًا بك في الآلة الحاسبة"
        if current_language == "ar"
        else "Welcome to the Calculator"
    )
    welcome_window = tk.Toplevel(window)
    welcome_window.title(
        "مرحبا" if current_language == "ar" else "Welcome"
    )
    welcome_window.resizable(False, False)
    welcome_window.configure(
        bg="#202020" if current_theme == "dark" else "#f2f2f2"
    )
    welcome_window.transient(window)
    welcome_window.grab_set()
    welcome_window.update_idletasks()

    welcome_label = tk.Label(
        welcome_window,
        text=message,
        font=("Arial", 16, "bold"),
        fg="#ffffff" if current_theme == "dark" else "#111111",
        bg="#202020" if current_theme == "dark" else "#f2f2f2",
        padx=30,
        pady=25,
    )
    welcome_label.pack()

    window.update_idletasks()
    x = window.winfo_rootx() + (window.winfo_width() - 300) // 2
    y = window.winfo_rooty() + (window.winfo_height() - 100) // 2
    welcome_window.geometry(f"+{x}+{y}")

    welcome_window.after(1800, welcome_window.destroy)


def close_application():
    farewell_window = tk.Toplevel(window)
    farewell_window.title(
        "وداعًا" if current_language == "ar" else "Goodbye"
    )
    farewell_window.resizable(False, False)
    farewell_window.configure(
        bg="#202020" if current_theme == "dark" else "#f2f2f2"
    )
    farewell_window.transient(window)
    farewell_window.grab_set()
    farewell_window.update_idletasks()

    farewell_label = tk.Label(
        farewell_window,
        text="وداعًا!" if current_language == "ar" else "Goodbye!",
        font=("Arial", 16, "bold"),
        fg="#ffffff" if current_theme == "dark" else "#111111",
        bg="#202020" if current_theme == "dark" else "#f2f2f2",
        padx=35,
        pady=20,
    )
    farewell_label.pack()

    window.update_idletasks()
    x = window.winfo_rootx() + (window.winfo_width() - 240) // 2
    y = window.winfo_rooty() + (window.winfo_height() - 100) // 2
    farewell_window.geometry(f"+{x}+{y}")

    def finish_close():
        farewell_window.destroy()
        window.destroy()

    farewell_window.after(1200, finish_close)

history_list = None


def clear_history():
    history_entries.clear()
    refresh_history()


def refresh_history():
    if history_list is None:
        return
    history_list.delete("1.0", tk.END)
    if not history_entries:
        empty_text = "لا توجد عمليات" if current_language == "ar" else "No history"
        history_list.insert("1.0", empty_text)
        return

    lines = []
    for original_expression, result in history_entries:
        if current_language == "ar":
            original_expression = format_for_language(original_expression)
            result = format_for_language(result)
        lines.append(f"{original_expression} = {result}")
    history_list.insert("1.0", "\n".join(lines))


def append_value(value):
    global expression
    if value in "+-*/" and (not expression or expression[-1] in "+-*/"):
        if value == "-" and (not expression or expression[-1] in "+-*/"):
            expression += value
        return

    expression += value
    update_display(expression)


def clear():
    global expression
    expression = ""
    update_display("0")


def delete_last():
    global expression
    expression = expression[:-1]
    update_display(expression or "0")


def calculate():
    global expression
    if not expression:
        return

    try:
        original_expression = expression
        allowed_characters = set("0123456789+-*/(). ")
        if not set(expression).issubset(allowed_characters):
            raise ValueError

        result = eval(expression, {"__builtins__": {}}, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        expression = str(result)
        update_display(expression)
        history_entries.insert(0, (original_expression, expression))
        if len(history_entries) > 20:
            history_entries.pop()
        refresh_history()
    except ZeroDivisionError:
        expression = ""
        update_display(
            "لا يمكن القسمة على صفر"
            if current_language == "ar"
            else "Cannot divide by zero"
        )
    except (SyntaxError, NameError, ValueError):
        expression = ""
        update_display(
            "ادخال غير صحيح"
            if current_language == "ar"
            else "Invalid input"
        )


window = tk.Tk()
window.title("آلة حاسبة")
window.resizable(False, False)
window.configure(bg="#202020")

history_list = tk.Text(
    window,
    font=("Arial", 12),
    width=22,
    height=16,
    state="normal",
    wrap="word",
    bg="#111111",
    fg="#ffffff",
    borderwidth=0,
    padx=10,
    pady=10,
)
history_list.grid(row=1, column=4, rowspan=6, padx=(8, 12), pady=(12, 12), sticky="ns")

display = tk.Entry(
    window,
    font=("Arial", 28),
    justify="right",
    bg="#111111",
    fg="#ffffff",
    borderwidth=0,
)
display.grid(row=1, column=0, columnspan=4, padx=12, pady=12, ipady=12)
update_display("0")

current_theme = "dark"
button_widgets = []
theme_switch = None
dark_dot = None
light_dot = None
dark_dot_animation = None
light_dot_animation = None

def set_language(language):
    global current_language
    current_language = language
    update_display(expression or "0")
    refresh_history()
    clear_history_button.configure(
        text="مسح السجل" if language == "ar" else "Clear history"
    )
    window.title("آلة حاسبة" if language == "ar" else "Calculator")
    arabic_numbers = {"0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
                      "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"}
    for button, original_text in button_widgets:
        if original_text.isdigit():
            button.configure(
                text=arabic_numbers[original_text]
                if language == "ar"
                else original_text
            )
    language_button.configure(
        text="English" if language == "ar" else "العربية",
        bg="#28a745",
        fg="#ffffff",
        activebackground="#218838",
    )
    set_theme(current_theme)

def toggle_language():
    set_language("en" if current_language == "ar" else "ar")

def set_theme(theme):
    global current_theme
    current_theme = theme

    if theme == "dark":
        window.configure(bg="#202020")
        display.configure(bg="#111111", fg="#ffffff")
        theme_switch.configure(bg="#202020")
        history_list.configure(bg="#111111", fg="#ffffff")
        normal_bg = "#303030"
        operator_bg = "#505050"
    else:
        window.configure(bg="#f2f2f2")
        display.configure(bg="#ffffff", fg="#111111")
        theme_switch.configure(bg="#f2f2f2")
        history_list.configure(bg="#ffffff", fg="#111111")
        normal_bg = "#e6e6e6"
        operator_bg = "#d0d0d0"

    for button, text in button_widgets:
        if text == "=":
            button.configure(bg="#28a745", fg="#ffffff", activebackground="#218838")
        elif text in ["⌫", "%", "÷", "×", "-", "+", "±"]:
            button.configure(
                bg=operator_bg,
                fg="#111111" if theme == "light" else "#ffffff",
                activebackground="#b0b0b0" if theme == "light" else "#707070",
            )
        else:
            button.configure(
                bg=normal_bg,
                fg="#111111" if theme == "light" else "#ffffff",
                activebackground="#c8c8c8" if theme == "light" else "#707070",
            )

    clear_history_button.configure(
        bg="#505050" if theme == "dark" else "#d0d0d0",
        fg="#ffffff" if theme == "dark" else "#111111",
        activebackground="#707070" if theme == "dark" else "#b0b0b0",
    )

    animate_theme_dots()

def toggle_theme():
    set_theme("light" if current_theme == "dark" else "dark")


def animate_theme_dots():
    global dark_dot_animation, light_dot_animation
    if theme_switch is None:
        return
    if dark_dot_animation is not None:
        theme_switch.after_cancel(dark_dot_animation)
    if light_dot_animation is not None:
        theme_switch.after_cancel(light_dot_animation)

    dark_active = current_theme == "dark"
    light_active = current_theme == "light"
    dark_target = (9, 6, 27, 24) if dark_active else (11, 8, 25, 22)
    light_target = (41, 6, 59, 24) if light_active else (43, 8, 57, 22)

    def animate_dot(dot, target, job_name, step=0):
        global dark_dot_animation, light_dot_animation
        current = theme_switch.coords(dot)
        if len(current) != 4:
            return

        if step >= 5:
            theme_switch.coords(dot, *target)
            if job_name == "dark":
                dark_dot_animation = None
            else:
                light_dot_animation = None
            return

        next_coords = []
        for index in range(4):
            next_coords.append(current[index] + (target[index] - current[index]) * 0.35)
        theme_switch.coords(
            dot,
            next_coords[0],
            next_coords[1],
            next_coords[2],
            next_coords[3],
        )

        job = theme_switch.after(
            18,
            lambda: animate_dot(dot, target, job_name, step + 1),
        )
        if job_name == "dark":
            dark_dot_animation = job
        else:
            light_dot_animation = job

    theme_switch.itemconfigure(
        dark_dot,
        fill="#7e8da8" if dark_active else "#a8a8a8",
        outline="",
        width=0,
    )
    theme_switch.itemconfigure(
        light_dot,
        fill="#f4c542" if light_active else "#a8a8a8",
        outline="",
        width=0,
    )
    animate_dot(dark_dot, dark_target, "dark")
    animate_dot(light_dot, light_target, "light")

buttons = [
    ("C", 2, 0, clear),
    ("⌫", 2, 1, delete_last),
    ("%", 2, 2, lambda: append_value("/")),
    ("÷", 2, 3, lambda: append_value("/")),
    ("7", 3, 0, lambda: append_value("7")),
    ("8", 3, 1, lambda: append_value("8")),
    ("9", 3, 2, lambda: append_value("9")),
    ("×", 3, 3, lambda: append_value("*")),
    ("4", 4, 0, lambda: append_value("4")),
    ("5", 4, 1, lambda: append_value("5")),
    ("6", 4, 2, lambda: append_value("6")),
    ("-", 4, 3, lambda: append_value("-")),
    ("1", 5, 0, lambda: append_value("1")),
    ("2", 5, 1, lambda: append_value("2")),
    ("3", 5, 2, lambda: append_value("3")),
    ("+", 5, 3, lambda: append_value("+")),
    ("±", 6, 0, lambda: append_value("-")),
    ("0", 6, 1, lambda: append_value("0")),
    (".", 6, 2, lambda: append_value(".")),
    ("=", 6, 3, calculate),
]

for text, row, column, command in buttons:
    is_operator = text in ["⌫", "%", "÷", "×", "-", "+", "=", "±"]
    button = tk.Button(
        window,
        text=text,
        command=command,
        font=("Arial", 16),
        width=5,
        height=2,
        bg="#28a745" if text == "=" else ("#505050" if is_operator else "#303030"),
        fg="#ffffff",
        activebackground="#707070",
        borderwidth=0,
    )
    button.grid(row=row, column=column, padx=4, pady=4)
    button_widgets.append((button, text))

theme_switch = tk.Canvas(
    window,
    width=66,
    height=30,
    highlightthickness=0,
    bd=0,
    relief="flat",
    cursor="hand2",
)
theme_switch.grid(row=0, column=3, sticky="e", padx=(0, 10), pady=(8, 0))
dark_dot = theme_switch.create_oval(
    11,
    8,
    25,
    22,
    outline="",
    width=0,
    fill="#7e8da8",
)
light_dot = theme_switch.create_oval(
    43,
    8,
    57,
    22,
    outline="",
    fill="#a8a8a8",
)
theme_switch.tag_bind(dark_dot, "<Button-1>", lambda _event: set_theme("dark"))
theme_switch.tag_bind(light_dot, "<Button-1>", lambda _event: set_theme("light"))

clear_history_button = tk.Button(
    window,
    text="",
    command=clear_history,
    font=("Arial", 12),
    borderwidth=0,
)
clear_history_button.grid(row=7, column=4, sticky="ew", padx=(8, 12), pady=(0, 8))

language_button = tk.Button(
    window,
    text="",
    command=toggle_language,
    font=("Arial", 12),
    borderwidth=0,
)
language_button.grid(row=7, column=0, columnspan=4, sticky="ew", padx=4, pady=(0, 8))
set_language("ar")
set_theme("dark")

window.bind("<Return>", lambda _event: calculate())
window.bind("<Escape>", lambda _event: clear())
window.bind("<BackSpace>", lambda _event: delete_last())

window.protocol("WM_DELETE_WINDOW", close_application)
window.after(300, show_welcome)

window.mainloop()
 