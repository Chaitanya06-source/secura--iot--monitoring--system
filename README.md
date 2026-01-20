# Smart Home Security Door (IoT + Face Recognition)

This project ties an Arduino-based sensor/servo setup to a Python service that:
- Waits for an ultrasonic trigger from the microcontroller over serial.
- Captures a photo from a USB camera.
- Compares the face to family photos in `fam/` using OpenCV (LBPH, no dlib/AWS).
- If recognized, opens the servo immediately.
- If unknown, sends the photo to a Telegram chat and waits for the owner to reply `open` or `close` to decide.

## Quick start
1) **Install dependencies** (Python 3.10+ recommended):
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) **Configure secrets**  
Copy `env.sample` to `.env` and fill in:
- `TELEGRAM_TOKEN` – your bot token.
- `TELEGRAM_CHAT_ID` – your Telegram user ID (see below).
- `SERIAL_PORT` – e.g. `COM3` on Windows.
- `CAMERA_INDEX` – usually `0`.

**Getting your Telegram Chat ID:**
- Run `python get_chat_id.py` and send a message to your bot in Telegram.
- It will print your chat_id - copy this to `.env`.
- **Important:** You must send at least one message to your bot before it can send messages to you!

3) **Put family photos**  
Place 1+ clear, frontal photos in `fam/`. The file name (without extension) is used as the label (e.g., `pallavi.jpeg` → `pallavi`).

4) **Run**  
With the Arduino connected and sending the text `TRIGGER` when motion is detected:
```
.venv\Scripts\activate
python main.py
```

## Flow details
- Arduino sends `TRIGGER` → Python captures a frame from the webcam.
- Face is extracted with a Haar cascade and compared via LBPH (OpenCV contrib).
- If confidence is better than the threshold (default 70), Python sends `OPEN\n` over serial.
- Otherwise, the image is sent to Telegram; the script polls for an `open` or `close` reply (case-insensitive). Owner decision is forwarded over serial.

## Files
- `main.py` – orchestrates serial, camera, face auth, and Telegram loop.
- `face_auth.py` – loads family faces and performs LBPH recognition.
- `hardware.py` – serial bridge for trigger + servo commands.
- `telegram_bot.py` – Telegram send/poll utilities.
- `requirements.txt` – Python dependencies (no dlib/AWS).
- `.env.example` – sample config.

## Notes & tuning
- LBPH confidence: lower is better. Adjust `RECOG_THRESHOLD` in `.env` (typical 50–90).
- Make sure lighting is good and faces are frontal in `fam/`.
- If multiple faces are in one frame, the first detected face is used.
- Serial protocol is simple text: incoming `TRIGGER\n`; outgoing `OPEN\n`/`CLOSE\n`.


