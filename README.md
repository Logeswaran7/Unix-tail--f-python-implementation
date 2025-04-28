# Real-time Log Monitoring using Flask and Socket.IO

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [License](#license)

## Introduction

This project implements a real-time log file monitoring system using **Flask** and **Flask-SocketIO**.

It allows users to visualize live updates from a server-side log file directly in a web browser.

The application behaves like the Unix `tail -f` command — watching a log file for new lines and sending them to the client immediately — but implemented completely in **Python** and streamed to a **web interface**.

---

## Features

- **Real-Time Log Monitoring**: Continuously monitors a log file and streams new lines to clients in real-time.
- **Socket.IO Integration**: Uses WebSockets (through Socket.IO) for efficient two-way communication between the server and connected clients.
- **Tail -f Functionality in Python**: Replicates the behavior of `tail -f` natively in Python.
- **Web Interface**: Lightweight and responsive frontend to view logs without command-line access.
- **Initial Log Fetching**: On connection, the last `N` lines (configurable) of the log file are sent to the client.
- **Error Handling**: Gracefully handles cases where the log file does not exist or cannot be read.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Logeswaran7/Unix-tail--f-python-implementation.git
    cd Unix Tail --f Python Implementation
    ```

2. Install required dependencies:

    ```bash
    pip install flask flask-socketio
    ```

---

## Usage

1. Ensure you have a `log.txt` file in the same directory (or adjust the path in the code).

2. Start the server:

    ```bash
    python log_monitor.py
    ```

3. Open your web browser and navigate to:

    ```text
    'http://localhost:5000'
    
    ```

4. Append or write new lines into `log.txt` — they will instantly appear on the web client!

5. Example to manually append a new log entry:

    ```bash
    for i in {1..100}; do echo "$(date '+%Y-%m-%d %H:%M:%S') Simulated log file entry #$i" >> log.txt; sleep 1; done
    ```

    After running the above command, you will immediately see "New log entry at (current date and time)" appear in the web page without needing to refresh.

---

## Results

Example:  
When new log entries are written to `log.txt`, they instantly appear in the browser. You can watch a video demonstration of this functionality below:

![Live Log Monitoring Video](output.mp4)

---

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to use, modify, and share it!
