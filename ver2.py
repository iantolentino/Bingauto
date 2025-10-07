import random
import time
import threading
import tkinter as tk

import pyautogui

# ------------------ Configuration ------------------ #
topics = [
    "python tutorial", "AI tools", "web development",
    "data science", "selenium automation"
]
modifiers = [
    "2025", "step-by-step", "free guide",
    "explained", "easy method", "for beginners"
]

max_searches = 50
batch_size = 5
search_delay = 8  # seconds between batches

# ------------------ Globals ------------------ #
used_queries = set()
searching = False
search_count = 0

# ------------------ Generate Unique Query ------------------ #
def next_query():
    while True:
        q = f"{random.choice(topics)} {random.choice(modifiers)}"
        if q not in used_queries:
            used_queries.add(q)
            return q

# ------------------ Typing Simulation ------------------ #
def type_query(query):
    interval = 8.0 / len(query)
    for ch in query:
        pyautogui.write(ch)
        time.sleep(interval)
    pyautogui.press('enter')

# ------------------ Main Automation ------------------ #
def start_searching():
    global searching, search_count
    searching = True
    search_count = 0

    def run():
        global search_count
        try:
            # Give user 5 seconds to focus Edge
            status_var.set("Focus Edge window in 5s...")
            time.sleep(5)

            while searching and search_count < max_searches:
                # build batch
                batch = [
                    next_query()
                    for _ in range(min(batch_size, max_searches - search_count))
                ]
                status_var.set(f"Batch {search_count+1}–{search_count+len(batch)}")

                # process each in batch
                for q in batch:
                    # Open new tab (Ctrl+T)
                    pyautogui.hotkey('ctrl', 't')
                    time.sleep(1)  # let tab open

                    # Type query over ~8s and Enter
                    type_query(q)

                    search_count += 1
                    time.sleep(1)  # small pause between tab opens

                # wait before next batch
                time.sleep(search_delay)

            status_var.set(f"Completed {search_count} searches.")
        except Exception as e:
            status_var.set(f"Error: {e}")

    threading.Thread(target=run, daemon=True).start()

# ------------------ Stop Automation ------------------ #
def stop_searching():
    global searching
    searching = False
    status_var.set("Stopped.")

# ------------------ GUI Setup ------------------ #
app = tk.Tk()
app.title("Bing Search Automator")
app.geometry("400x180")
app.resizable(False, False)

status_var = tk.StringVar(value="Ready. Click Start when Edge is focused.")

tk.Label(app, text="Bing Search Automator", font=("Helvetica", 16)).pack(pady=10)
tk.Label(app, textvariable=status_var, font=("Arial", 10), wraplength=380).pack(pady=5)

tk.Button(app, text="Start", command=start_searching,
          bg="green", fg="white", width=15).pack(pady=5)
tk.Button(app, text="Stop", command=stop_searching,
          bg="red", fg="white", width=15).pack(pady=5)

app.mainloop()
