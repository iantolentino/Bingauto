import random
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pygame
from datetime import timedelta

# ------------------ CONFIGURATION (EDIT POSITIONS HERE) ------------------ #
# Main position that is clicked before every search batch
main_click_pos = (1890, 270)  # <-- EDIT THIS IF NEEDED

# Positions to click between batches (pos1, pos2, pos3, pos4)
# Use position_finder.py (terminal) to get coordinates and paste here.
click_positions = [
    (1050, 1055),  # pos1  <-- EDIT IF NEEDED
    (1090, 1055),  # pos2  <-- EDIT IF NEEDED
    (1130, 1055),  # pos3  <-- EDIT IF NEEDED
    (1170, 1055)   # pos4  <-- EDIT IF NEEDED
]

# ------------------ SEARCH CONFIG ------------------ #
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

# ------------------ GLOBALS ------------------ #
pyautogui.FAILSAFE = True
used_queries = set()
searching = False
search_count = 0
max_searches = 30
avg_time_per_search = 6  # estimated seconds per search (for ETA)
remaining_time = 0

# ------------------ SOUND NOTIFICATION ------------------ #
def play_notification():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("bingnotif.mp3")
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)

# ------------------ QUERY GENERATION ------------------ #
def next_query():
    while True:
        q = f"{random.choice(topics)} {random.choice(modifiers)}"
        if q not in used_queries:
            used_queries.add(q)
            return q

# ------------------ TYPING SIMULATION ------------------ #
def type_query_fast(query):
    interval = 0.75 / max(len(query), 1)
    for ch in query:
        pyautogui.write(ch)
        time.sleep(interval)
    pyautogui.press('enter')

# ------------------ TIMER ------------------ #
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

# ------------------ PERFORM A SEARCH BATCH (click main then do searches) ------------------ #
def perform_search_batch(batch_name):
    global search_count, searching

    if not searching:
        return

    status_var.set(f"{batch_name}: Clicking main position...")
    pyautogui.click(main_click_pos[0], main_click_pos[1])
    time.sleep(2)

    for i in range(max_searches):
        if not searching:
            return

        q = next_query()
        status_var.set(f"{batch_name} | Search {i+1}/{max_searches}: {q}")

        # open new tab, type, wait, close tab
        pyautogui.hotkey('ctrl', 't')
        time.sleep(1)
        type_query_fast(q)
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'w')

        search_count += 1

# ------------------ MAIN AUTOMATION FLOW ------------------ #
def start_searching():
    global searching, search_count, max_searches, remaining_time

    try:
        max_searches = int(search_input.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of searches.")
        return

    if max_searches <= 0:
        messagebox.showerror("Error", "Search count must be greater than 0.")
        return

    if not click_positions or len(click_positions) < 4:
        # Optional: allow fewer than 4, but user expects 4 positions — warn if missing
        if messagebox.askyesno("Positions missing", "Less than 4 positions defined. Continue?"):
            pass
        else:
            return

    searching = True
    search_count = 0
    # total batches: 1 main + len(click_positions)
    total_batches = 1 + len(click_positions)
    remaining_time = max_searches * total_batches * avg_time_per_search
    eta_var.set(f"⏳ Estimated time: {str(timedelta(seconds=remaining_time))}")
    update_timer()

    def run():
        global searching
        try:
            time.sleep(3)
            status_var.set("🟢 Starting automation...")

            # 1) Start batch: MAIN (click main -> searches)
            perform_search_batch("Main Batch")

            # 2) For each position: click position -> click main -> searches
            for idx, pos in enumerate(click_positions, start=1):
                if not searching:
                    break

                status_var.set(f"Clicking position {idx} at {pos}...")
                pyautogui.click(pos[0], pos[1])
                time.sleep(1.5)

                # After clicking position, click main position again then run searches
                perform_search_batch(f"Batch {idx}")

            # 3) After finishing the 4th position batch, wait 3s then close 4 tabs
            if searching:
                status_var.set("Finished pos4 batch. Waiting 3s before closing 4 tabs...")
                time.sleep(3)
                for _ in range(4):
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.5)

            status_var.set("✅ All batches completed!")
            play_notification()

        except Exception as e:
            status_var.set(f"⚠️ Error: {e}")
        finally:
            searching = False

    threading.Thread(target=run, daemon=True).start()

# ------------------ STOP ------------------ #
def stop_searching():
    global searching
    searching = False
    status_var.set("⏹ Stopped manually.")

# ------------------ GUI ------------------ #
app = tk.Tk()
app.title("AI Search Automator")
app.configure(bg="#f0f0f0")
app.wm_attributes("-topmost", 1)

window_width, window_height = 480, 320
screen_w, screen_h = app.winfo_screenwidth(), app.winfo_screenheight()
pos_x = (screen_w // 2) - (window_width // 2)
pos_y = (screen_h // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
app.resizable(False, False)

style = ttk.Style(app)
style.theme_use("clam")
style.configure("TLabel", background="#f0f0f0", foreground="#000000", font=("Inter", 11))
style.configure("TButton", background="#1a1a1a", foreground="#ffffff", padding=6, font=("Inter", 10))
style.map("TButton", background=[("active", "#333333")], foreground=[("active", "#ffffff")])
style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

status_var = tk.StringVar(value="Ready. Enter search count and click Start.")
eta_var = tk.StringVar(value="⏳ Waiting...")

ttk.Label(app, text="🔍 AI Search Automator", font=("Inter", 16, "bold")).pack(pady=8)
ttk.Label(app, textvariable=status_var, wraplength=420).pack(pady=5)
ttk.Label(app, textvariable=eta_var, font=("Inter", 11, "bold"), foreground="blue").pack(pady=5)

frame = ttk.Frame(app)
frame.pack(pady=8)
ttk.Label(frame, text="Number of searches per batch: ").grid(row=0, column=0, padx=5)
search_input = ttk.Entry(frame, width=8)
search_input.grid(row=0, column=1, padx=5)
search_input.insert(0, str(max_searches))

btn_frame = ttk.Frame(app)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="▶ Start", command=start_searching).grid(row=0, column=0, padx=8)
ttk.Button(btn_frame, text="⏹ Stop", command=stop_searching).grid(row=0, column=1, padx=8)

app.mainloop()
