import random
import time
import threading
import tkinter as tk
import pyautogui

# ------------------ Configuration ------------------ #
topics = [
    "app ideas", "data viz", "cloud tools",
    "linux hacks", "ui design", "backend dev",
    "dev ops", "tech news", "code tricks",
    "api guide", "bug fixes", "system build",
    "html tips", "css hacks", "logic flow"
]


modifiers = [
    "free tips", "quick hack", "step walk", "easy path", "fast track", "bug help",
    "full guide", "real test", "pro guide", "top picks", "ml start", "best ways",
    "zero start", "hire tips", "mini tool", "low code", "logic show", "gear list",
    "from zero", "deep dive", "full tool", "fast lane", "2025 picks", "smart plan",
    "boost mode", "speed hack", "real use", "how done", "must have", "data pack",
    "logic flow", "tech tips", "start code", "dev side", "no tools", "easy steps",
    "quick list", "solid pick", "fresh tips", "cool hacks", "core facts"
]

max_searches = 35

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
