import random
import time
import threading
import tkinter as tk
import pyautogui

# ------------------ Configuration ------------------ #
topics = [
    "python tips", "ai hacks", "web build",
    "data tools", "selenium bot"
]

modifiers = [
    "free guide", "quick tips", "step guide", "easy way", "fast build", "code help",
    "full course", "real case", "pro tricks", "top tools", "ai guide", "best use",
    "zero hero", "job tips", "mini app", "no code", "code walk", "tool list",
    "from base", "deep look", "full app", "fast path", "2025 trend", "smart way",
    "code boost", "quick hack", "use case", "how work", "must know", "data set",
    "code flow", "it guide", "code start", "for dev", "no need", "easy steps",
    "short list", "real deal", "new tips", "good tricks", "key facts"
]

max_searches = 50

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
def type_query_fast(query):
    interval = 1 / len(query)
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
            status_var.set("Click your browser")
            time.sleep(3)

            while searching and search_count < max_searches:
                q = next_query()
                status_var.set(f"Search {search_count+1}/{max_searches}: {q}")

                pyautogui.hotkey('ctrl', 't')
                time.sleep(1)

                type_query_fast(q)

                time.sleep(2)  # view time

                pyautogui.hotkey('ctrl', 'w')  # close tab

                search_count += 1

            status_var.set(f"Done {search_count} searches.")
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

status_var = tk.StringVar(value="Ready. Click Start and focus Edge.")

tk.Label(app, text="Bing Search Automator", font=("Helvetica", 16)).pack(pady=10)
tk.Label(app, textvariable=status_var, font=("Arial", 10), wraplength=380).pack(pady=5)

tk.Button(app, text="Start", command=start_searching, bg="green", fg="white", width=15).pack(pady=5)
tk.Button(app, text="Stop",  command=stop_searching,  bg="red",   fg="white", width=15).pack(pady=5)

app.mainloop()
