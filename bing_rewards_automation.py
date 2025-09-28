import random
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pygame
from datetime import timedelta 
  
# ------------------ Configuration ------------------ #
topics = [
    "AI apps", "neural nets", "deep learning", "large models", "AI ethics",
    "AI tools", "AI startups", "AI agents", "cloud AI", "vision AI",
    "NLP models", "AI robotics", "AI research", "data mining", "AI coding"
]
 
modifiers = [
    "quick guide", "deep dive", "easy intro", "step walk", "real use",
    "best picks", "case study", "AI hacks", "top tools", "fast tips",
    "full guide", "new trends", "smart plan", "code tricks", "core facts",
    "common bugs", "mini tool", "fast track", "logic flow", "tech news"
]


# ------------------ Globals ------------------ #
used_queries = set()
searching = False
search_count = 0
max_searches = 30
avg_time_per_search = 6.5  # seconds (rough estimate)
remaining_time = 0

# ------------------ Play Notification ------------------ #
def play_notification():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("bingnotif.mp3")
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
    interval = 0.75 / len(query)
    for ch in query:
        pyautogui.write(ch)
        time.sleep(interval)
    pyautogui.press('enter')

# ------------------ Countdown Updater ------------------ #
def update_timer():
    global remaining_time
    if searching and remaining_time > 0:
        remaining_time -= 1
        eta_var.set(f"⏳ Time left: {str(timedelta(seconds=remaining_time))}")
        app.after(1000, update_timer)
    elif not searching:
        eta_var.set("⏹ Stopped")
    else:
        eta_var.set("✅ Finished!")

# ------------------ Main Automation ------------------ #
def start_searching():
    global searching, search_count, max_searches, remaining_time
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
    remaining_time = max_searches * avg_time_per_search
    eta_var.set(f"⏳ Time left: {str(timedelta(seconds=remaining_time))}")
    update_timer()

    def run():
        global search_count, searching
        try:
            time.sleep(3)
            status_var.set("Started searching...")

            while searching and search_count < max_searches:
                q = next_query()
                status_var.set(f"Search {search_count+1}/{max_searches}: {q}")

                pyautogui.hotkey('ctrl', 't')
                time.sleep(1)
                type_query_fast(q)
                time.sleep(2)
                pyautogui.hotkey('ctrl', 'w')

                search_count += 1

            status_var.set(f"✅ Done {search_count} searches")
            play_notification()
        except Exception as e:
            status_var.set(f"Error: {e}")
        finally:
            searching = False

    threading.Thread(target=run, daemon=True).start()

# ------------------ Stop Automation ------------------ #
def stop_searching():
    global searching
    searching = False
    status_var.set("Stopped ❌")

# ------------------ GUI Setup ------------------ #
app = tk.Tk()
app.title("AI Search Automator")
app.configure(bg="#f0f0f0")
app.wm_attributes("-topmost", 1)

# Center window
window_width, window_height = 460, 280
screen_w, screen_h = app.winfo_screenwidth(), app.winfo_screenheight()
pos_x = (screen_w // 2) - (window_width // 2)
pos_y = (screen_h // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
app.resizable(False, False)

# Style
style = ttk.Style(app)
style.theme_use("clam")
style.configure("TLabel", background="#f0f0f0", foreground="#000000", font=("Inter", 11))
style.configure("TButton", background="#1a1a1a", foreground="#ffffff", padding=6, font=("Inter", 10))
style.map("TButton", background=[("active", "#333333")], foreground=[("active", "#ffffff")])
style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

status_var = tk.StringVar(value="Ready. Enter search count and click Start.")
eta_var = tk.StringVar(value="⏳ Time left: 00:00:00")

ttk.Label(app, text="🔍 AI Search Automator", font=("Inter", 16, "bold")).pack(pady=8)
ttk.Label(app, textvariable=status_var, wraplength=420).pack(pady=5)
ttk.Label(app, textvariable=eta_var, font=("Inter", 11, "bold"), foreground="blue").pack(pady=5)

frame = ttk.Frame(app)
frame.pack(pady=8)

ttk.Label(frame, text="Number of searches: ").grid(row=0, column=0, padx=5)
search_input = ttk.Entry(frame, width=8)
search_input.grid(row=0, column=1, padx=5)
search_input.insert(0, str(max_searches))

btn_frame = ttk.Frame(app)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="▶ Start", command=start_searching).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="⏹ Stop", command=stop_searching).grid(row=0, column=1, padx=8)

app.mainloop()




