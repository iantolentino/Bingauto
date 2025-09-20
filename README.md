# Bing Search Automator

The **Bing Search Automator** is a simple desktop tool built with Python and Tkinter that automatically performs multiple Bing searches using randomized queries.  
It’s useful for automating repetitive searches, simulating browsing, or quickly generating query ideas.  

## ✨ Features
- 🎯 **Automated searches** — runs up to 35 searches by default.  
- 🔀 **Randomized queries** — combines topics with modifiers for variety.  
- 🌐 **Browser integration** — works with your default browser (tested with Microsoft Edge).  
- 🖥️ **Simple GUI** — start/stop buttons with real-time status updates.  
- ⚡ **Lightweight EXE** — no need to install Python, just run the provided `.exe`.  

## 📦 Installation
1. Download the latest **`.exe` file** from the release or the provided package.  
2. Place it anywhere on your computer.  
3. Double-click to run — no setup required.  

## 🚀 Usage
1. Open the **Bing Search Automator**.  
2. Click **Start**.  
3. Within 3 seconds, switch focus to your browser (Microsoft Edge recommended).  
4. The program will:  
   - Open a new tab.  
   - Type a randomized query.  
   - Wait briefly, then close the tab.  
   - Repeat until it reaches the set maximum (default: 35).  
5. Click **Stop** anytime to end the automation early.  

## ⚙️ Configuration
- **Default maximum searches**: 35  
- You can change this in the script (`max_searches` variable) if running from source.  

## 🛠️ Tech Stack
- **Python** (threading, random, time)  
- **Tkinter** (GUI)  
- **PyAutoGUI** (keyboard automation)  

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
Use responsibly — automated searches may violate Bing or browser terms of service.  

## 📜 License
MIT License. Free to use and modify.  
