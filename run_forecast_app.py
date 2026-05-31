import os
import subprocess
import sys
import time
import re

# Path to Google Chrome executable – adjust if needed
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Launch Streamlit as a subprocess, capture its stdout
proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=os.path.dirname(os.path.abspath(__file__)),
)

url = None
# Read output lines until we find the local URL
for line in proc.stdout:
    sys.stdout.write(line)  # Echo Streamlit logs to console
    match = re.search(r"Local URL: (http[^"]+)", line)
    if match:
        url = match.group(1)
        break

if url:
    # Give Streamlit a moment to finish startup
    time.sleep(2)
    # Open the URL in Chrome
    subprocess.Popen([chrome_path, url])
else:
    sys.stderr.write("[Error] Unable to detect Streamlit URL. Chrome not launched.\n")

# Wait for the Streamlit process to finish (Ctrl+C will terminate both)
proc.wait()
