import ctypes
import os
import platform

class SystemController:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"

    def lock_session(self):
        """Verrouille la session Windows."""
        if self.is_windows:
            print("Verrouillage de la session...")
            ctypes.windll.user32.LockWorkStation()
        else:
            print("[Simulé] Verrouillage de la session (Non-Windows)")

    def prevent_sleep(self):
        """
        Empêche la mise en veille en simulant une activité (optionnel).
        Sur Windows, on peut utiliser SetThreadExecutionState.
        """
        if self.is_windows:
            # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)

    def allow_sleep(self):
        if self.is_windows:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
