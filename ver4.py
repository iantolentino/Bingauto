import random
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pygame   # ✅ for MP3 notification sound

# ------------------ Configuration ------------------ #
topics = [
    "AI apps", "neural networks", "transformers",
    "LLMs", "generative AI", "AI startups",
    "AI ethics", "AI tools", "prompt engineering",
    "vision AI", "NLP models", "AI in cloud",
    "AI research", "AI in robotics", "autonomous agents"
]

modifiers = [
    "quick guide", "step by step", "from scratch", "easy intro", "deep dive",
    "real world use", "2025 trends", "complete tutorial", "case study", "best practices",
    "hands-on", "no code tools", "AI hacks", "top frameworks", "comparison",
    "core concepts", "common mistakes", "tips and tricks", "full workflow", "practical guide"
]

# ------------------ Globals ------------------ #
used_queries = set()
searching = False
search_count = 0
max_searches = 30  # default, user can override

# ------------------ Play Notification ------------------ #
def play_notification():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("bingnotif.mp3")  # ✅ make sure file is in same folder
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)

# ------------------ Generate Unique Query ------------------ #
def next_query():
    while True:
        q = f"{random.choice(topics)} {random.choice(modifiers)}"
        if q not in used_queries:
            used_queries.add(q)
            return q

# ------------------ Typing Simulation ------------------ #
def type_query_fast(query):
    interval = 1 / len(query)
    for ch in query:
        pyautogui.write(ch)
        time.sleep(interval)
    pyautogui.press('enter')

# ------------------ Main Automation ------------------ #
def start_searching():
    global searching, search_count, max_searches
    try:
        max_searches = int(search_input.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of searches.")
        return

    if max_searches <= 0:
        messagebox.showerror("Error", "Search count must be greater than 0.")
        return

    searching = True
    search_count = 0

    def run():
        global search_count
        try:
            status_var.set("Click your browser in 3s...")
            time.sleep(3)

            while searching and search_count < max_searches:
                q = next_query()
                status_var.set(f"Search {search_count+1}/{max_searches}: {q}")

                pyautogui.hotkey('ctrl', 't')  # new tab
                time.sleep(1)
                type_query_fast(q)
                time.sleep(2)  # stay on page
                pyautogui.hotkey('ctrl', 'w')  # close tab

                search_count += 1

            status_var.set(f"Done {search_count} searches ✅")
            play_notification()  # 🔔 Play custom MP3
        except Exception as e:
            status_var.set(f"Error: {e}")

    threading.Thread(target=run, daemon=True).start()

# ------------------ Stop Automation ------------------ #
def stop_searching():
    global searching
    searching = False
    status_var.set("Stopped ❌")

# ------------------ GUI Setup ------------------ #
app = tk.Tk()
app.title("AI Search Automator")

# Light gray background
app.configure(bg="#f0f0f0")

# Center the window
window_width = 440
window_height = 240
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
pos_x = (screen_width // 2) - (window_width // 2)
pos_y = (screen_height // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
app.resizable(False, False)

# Style
style = ttk.Style(app)
style.theme_use("clam")
style.configure("TLabel", background="#f0f0f0", foreground="#000000", font=("Inter", 11))
style.configure("TButton", background="#1a1a1a", foreground="#ffffff", padding=6, font=("Inter", 10))
style.map("TButton",
    background=[("active", "#333333")],
    foreground=[("active", "#ffffff")]
)
style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

status_var = tk.StringVar(value="Ready. Enter search count and click Start.")

ttk.Label(app, text="🔍 AI Search Automator", font=("Inter", 16, "bold")).pack(pady=10)
ttk.Label(app, textvariable=status_var, wraplength=400).pack(pady=5)

frame = ttk.Frame(app)
frame.pack(pady=10)

ttk.Label(frame, text="Number of searches: ").grid(row=0, column=0, padx=5)
search_input = ttk.Entry(frame, width=8)
search_input.grid(row=0, column=1, padx=5)
search_input.insert(0, str(max_searches))

btn_frame = ttk.Frame(app)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="▶ Start", command=start_searching).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="⏹ Stop", command=stop_searching).grid(row=0, column=1, padx=8)

app.mainloop()
