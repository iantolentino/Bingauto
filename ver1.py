import random
import time
import threading
import tkinter as tk

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

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
search_delay = 8  # seconds between searches

# ------------------ Globals ------------------ #
used_queries = set()
searching = False
driver = None
search_count = 0

# ------------------ Generate Unique Query ------------------ #
def next_query():
    while True:
        q = f"{random.choice(topics)} {random.choice(modifiers)}"
        if q not in used_queries:
            used_queries.add(q)
            return q

# ------------------ Typing Simulation ------------------ #
def simulate_typing_direct(query):
    # type each character over ~8 seconds then ENTER
    actions = ActionChains(driver)
    interval = 8.0 / len(query)
    for ch in query:
        actions.send_keys(ch).perform()
        time.sleep(interval)
    actions.send_keys(Keys.RETURN).perform()

# ------------------ Main Automation ------------------ #
def start_searching():
    global driver, searching, search_count
    searching = True
    search_count = 0

    def run():
        global driver, search_count
        try:
            # Initialize Edge via webdriver-manager
            options = Options()
            options.add_argument("--start-maximized")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)

            while searching and search_count < max_searches:
                q = next_query()
                status_var.set(f"Searching ({search_count+1}/{max_searches}): {q}")

                # Open a new tab at Bing
                driver.execute_script("window.open('https://www.bing.com', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)  # allow page to load and autofocus

                try:
                    simulate_typing_direct(q)
                except Exception:
                    # Fallback: direct URL search
                    url = "https://www.bing.com/search?q=" + q.replace(" ", "+")
                    driver.get(url)

                search_count += 1
                time.sleep(search_delay)

            status_var.set(f"Completed {search_count} searches.")
        except Exception as e:
            status_var.set(f"Error: {e}")
        finally:
            if driver:
                driver.quit()

    threading.Thread(target=run, daemon=True).start()

# ------------------ Stop Automation ------------------ #
def stop_searching():
    global searching
    searching = False
    status_var.set("Stopped.")

# ------------------ GUI Setup ------------------ #
app = tk.Tk()
app.title("Bing Search Automator")
app.geometry("500x200")
app.resizable(False, False)

# Correct StringVar initialization
status_var = tk.StringVar(value="Ready to start.")

tk.Label(app, text="Bing Search Automator", font=("Helvetica", 16)).pack(pady=10)
tk.Label(app, textvariable=status_var, font=("Arial", 10), wraplength=480).pack(pady=5)

tk.Button(app, text="Start", command=start_searching,
          bg="green", fg="white", width=20).pack(pady=5)
tk.Button(app, text="Stop", command=stop_searching,
          bg="red", fg="white", width=20).pack(pady=5)

app.mainloop()
