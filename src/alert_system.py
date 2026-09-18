import threading
import sys
import platform

class AlertSystem:
    def __init__(self, frequency=2500, duration=400):
        self.frequency = frequency
        self.duration = duration
        self.is_playing = False
        self.os_type = platform.system()

    def _play_sound(self):
        if self.os_type == "Windows":
            try:
                import winsound
                winsound.Beep(self.frequency, self.duration)
            except Exception:
                sys.stdout.write('\a')
                sys.stdout.flush()
        else:
            sys.stdout.write('\a')
            sys.stdout.flush()
        self.is_playing = False

    def trigger_alarm(self):
        if not self.is_playing:
            self.is_playing = True
            thread = threading.Thread(target=self._play_sound, daemon=True)
            thread.start()