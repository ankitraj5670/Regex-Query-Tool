import re
import tkinter as tk
from tkinter import filedialog, messagebox

def text_highlighting(text_widget, pattern, case_sensitive=True, color='yellow'):
    txt = text_widget.get("1.0", tk.END)
    flags = 0 if not case_sensitive else re.IGNORECASE
    pattern = re.compile(pattern, flags)

    matches = pattern.finditer(txt)
    highlighted_text = ""
    last_end = 0
    for match in matches:
        start, end = match.span()
        highlighted_text += txt[last_end:start] + txt[start:end]
        last_end = end

        # Apply background color to the matched text
        text_widget.tag_add("highlight", f"1.{start}", f"1.{end}")
        text_widget.tag_config("highlight", background=color)

    highlighted_text += txt[last_end:]
    return highlighted_text

def capture_text(txt, pattern, case_sensitive=True):
    flags = 0 if not case_sensitive else re.IGNORECASE
    pattern = re.compile(pattern, flags)

    match = pattern.findall(txt)
    return match

def replace_text(txt, pattern, rep, case_sensitive=True):
    flags = 0 if not case_sensitive else re.IGNORECASE
    pattern = re.compile(pattern, flags)
    replaced_text = pattern.sub(rep, txt)
    return replaced_text

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, mode='r', encoding='utf-8') as f:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, f.read())

def process_highlight():
    pattern = pattern_entry.get()
    case_sensitive = case_sensitive_var.get()
    color = color_var.get()
    
    highlighted = text_highlighting(text_area, pattern, case_sensitive, color)
    
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, highlighted)

def process_capture():
    txt = text_area.get("1.0", tk.END)
    pattern = pattern_entry.get()
    case_sensitive = case_sensitive_var.get()
    
    captured = capture_text(txt, pattern, case_sensitive)
    
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, '\n'.join(captured))

def process_replace():
    txt = text_area.get("1.0", tk.END)
    pattern = pattern_entry.get()
    case_sensitive = case_sensitive_var.get()
    rep = replace_entry.get()
    
    replaced = replace_text(txt, pattern, rep, case_sensitive)
    
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, replaced)

def display_regex_help():
    regex_help_text = """Regular Expressions Help:
- Regular expressions (regex) are patterns used to match character combinations in strings.
- They are a powerful tool for searching, extracting, and manipulating text.
- Common regex symbols and their meanings:
    * .     - Matches any single character.
    * ^     - Matches the start of a string.
    * $     - Matches the end of a string.
    * [...] - Matches any single character in the specified set.
    * [^...] - Matches any single character not in the specified set.
    * *     - Matches zero or more occurrences of the preceding element.
    * +     - Matches one or more occurrences of the preceding element.
    * ?     - Matches zero or one occurrence of the preceding element.
    * |     - Alternation, matches either the pattern before or after the |.
    * ()    - Groups patterns together.
- Example patterns:
    * \d    - Matches any digit character.
    * \w    - Matches any alphanumeric character or underscore.
    * \s    - Matches any whitespace character.
    * \b    - Matches a word boundary.
- Use online regex testers for practice and debugging.
"""
    messagebox.showinfo("Regular Expressions Help", regex_help_text)

# GUI setup
root = tk.Tk()
root.title("Text Processing Application")
root.geometry("800x600")

# Initialize text_area
text_area = tk.Text(root, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12))
text_area.pack(fill=tk.BOTH, expand=True)

# Styles
root.configure(background="#f0f0f0")
button_bg = "#007bff"
button_fg = "white"
text_bg = "white"
text_fg = "black"

# File Frame
file_frame = tk.Frame(root, bg="#f0f0f0")
file_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

open_button = tk.Button(file_frame, text="Open File", command=open_file, bg=button_bg, fg=button_fg)
open_button.pack(side=tk.LEFT)

# Options Frame
options_frame = tk.Frame(root, bg="#f0f0f0")
options_frame.pack(fill=tk.X, padx=20, pady=10)

pattern_label = tk.Label(options_frame, text="Enter pattern:", bg="#f0f0f0")
pattern_label.grid(row=0, column=0, padx=(0, 5))

pattern_entry = tk.Entry(options_frame, width=30)
pattern_entry.grid(row=0, column=1, padx=(0, 10))

case_sensitive_var = tk.BooleanVar()
case_sensitive_check = tk.Checkbutton(options_frame, text="Case sensitive", variable=case_sensitive_var, bg="#f0f0f0")
case_sensitive_check.grid(row=0, column=2, padx=(0, 10))

color_var = tk.StringVar(value='yellow')
color_label = tk.Label(options_frame, text="Choose color:", bg="#f0f0f0")
color_label.grid(row=0, column=3, padx=(0, 5))

color_options = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
color_dropdown = tk.OptionMenu(options_frame, color_var, *color_options)
color_dropdown.grid(row=0, column=4)

# Regex Help Button
help_button = tk.Button(options_frame, text="Regex Help", command=display_regex_help, bg="#007bff", fg="white")
help_button.grid(row=0, column=5)

# Process Frame
process_frame = tk.Frame(root, bg="#f0f0f0")
process_frame.pack(fill=tk.X, padx=20, pady=10)

highlight_button = tk.Button(process_frame, text="Highlight Text", command=process_highlight, bg="#28a745", fg="white")
highlight_button.pack(side=tk.LEFT, padx=5)

capture_button = tk.Button(process_frame, text="Capture Text", command=process_capture, bg="#007bff", fg="white")
capture_button.pack(side=tk.LEFT, padx=5)

replace_button = tk.Button(process_frame, text="Replace Text", command=process_replace, bg="#dc3545", fg="white")
replace_button.pack(side=tk.LEFT, padx=5)

# Replacement Frame
replace_frame = tk.Frame(root, bg="#f0f0f0")
replace_frame.pack(fill=tk.X, padx=20, pady=10)

replace_label = tk.Label(replace_frame, text="Replace with:", bg="#f0f0f0")
replace_label.grid(row=0, column=0, padx=(0, 5))

replace_entry = tk.Entry(replace_frame, width=30)
replace_entry.grid(row=0, column=1, padx=(0, 10))

# Output Frame
output_frame = tk.Frame(root, bg="#f0f0f0")
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

output_text = tk.Text(output_frame, wrap=tk.WORD, bg=text_bg, fg=text_fg, font=("Arial", 14))
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()

