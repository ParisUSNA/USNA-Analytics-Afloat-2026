import os
import sys
import time
import socket
import signal
import threading

# --- AGGRESSIVE SIGNAL PATCH ---
# We must patch the signal module BEFORE Streamlit is even imported
def dummy_signal(sig, frame):
    pass
signal.signal = dummy_signal
# -------------------------------

from flaskwebgui import FlaskUI
import streamlit.web.cli as stcli

def resolve_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)

def wait_for_port(port, host='127.0.0.1', timeout=10.0):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                return False

def start_streamlit():
    """Actual streamlit logic"""
    app_path = resolve_path("app.py") 
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        f"--server.port={free_port}",
        "--server.address=127.0.0.1",
        "--global.developmentMode=false",
    ]
    stcli.main()

def dummy_server():
    """Does nothing, just satisfies flaskwebgui requirement"""
    pass

if __name__ == "__main__":
    # 1. Silence Output
    null_fds = [os.open(os.devnull, os.O_RDWR) for _ in range(2)]
    os.dup2(null_fds[0], 1)
    os.dup2(null_fds[1], 2)

    # 2. Port Discovery
    def get_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    global free_port
    free_port = get_free_port()

    # 3. Start Streamlit in a manually managed thread
    # We do this because we need to wait for the port before showing the UI
    t = threading.Thread(target=start_streamlit, daemon=True)
    t.start()

    # 4. Wait for Streamlit to be ready
    if wait_for_port(free_port):
        # 5. Launch UI
        # 'server=dummy_server' satisfies the positional argument requirement
        FlaskUI(
            server=dummy_server, 
            port=free_port,
            width=1200,
            height=800
        ).run()
    else:
        sys.exit(1)