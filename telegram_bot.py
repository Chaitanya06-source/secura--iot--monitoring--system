import io
import time
from typing import Optional

from telegram import Bot
from telegram.error import TelegramError


class TelegramNotifier:
    """Sends alerts and polls for owner decision via Telegram."""

    def __init__(self, token: str, chat_id: int) -> None:
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self._last_update_id: Optional[int] = None

    def send_photo_with_caption(self, image_bgr, caption: str) -> bool:
        """Send a NumPy BGR image. Returns True if successful."""
        import cv2

        try:
            success, buf = cv2.imencode(".jpg", image_bgr)
            if not success:
                print("ERROR: Failed to encode image for Telegram.")
                return False
            bio = io.BytesIO(buf.tobytes())
            bio.name = "visitor.jpg"
            self.bot.send_photo(chat_id=self.chat_id, photo=bio, caption=caption)
            return True
        except TelegramError as e:
            print(f"ERROR: Failed to send photo to Telegram: {e}")
            return False

    def send_message(self, text: str) -> bool:
        """Send a text message. Returns True if successful."""
        try:
            self.bot.send_message(chat_id=self.chat_id, text=text)
            return True
        except TelegramError as e:
            print(f"ERROR: Failed to send message to Telegram: {e}")
            print(f"TIP: Make sure you've sent a message to your bot first!")
            return False
    
    def test_connection(self) -> bool:
        """Test if bot can send messages to chat_id."""
        return self.send_message("Security bot connection test.")

    def wait_for_decision(self, timeout_sec: int = 120) -> Optional[str]:
        """Poll for 'open' or 'close'. Returns the lowercased decision or None."""
        end_time = time.time() + timeout_sec
        while time.time() < end_time:
            updates = self.bot.get_updates(offset=self._next_offset(), timeout=10)
            for upd in updates:
                self._last_update_id = upd.update_id + 1
                text = (upd.message.text or "").strip().lower() if upd.message else ""
                if text in {"open", "close"}:
                    return text
            time.sleep(1)
        return None

    def _next_offset(self) -> Optional[int]:
        return self._last_update_id

