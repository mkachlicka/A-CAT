from acat.backend.utils import bind_ffmpeg
from acat.ui import start_application


#def main() -> None:
#    bind_ffmpeg()
#    start_application()

import sys
import traceback
from pathlib import Path

from acat.backend.utils import bind_ffmpeg
from acat.ui import start_application


def main() -> None:
    # Create log file in user's home directory so it's accessible
    log_file = Path.home() / "acat_error_log.txt"
    
    try:
        with open(log_file, "w") as f:
            f.write("=== ACAT Starting ===\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"Platform: {sys.platform}\n\n")
        
        # Try to bind FFmpeg
        with open(log_file, "a") as f:
            f.write("Binding FFmpeg...\n")
        bind_ffmpeg()
        
        with open(log_file, "a") as f:
            f.write("FFmpeg bound successfully\n")
            f.write("Starting UI...\n")
        
        start_application()
        
    except Exception as e:
        # Log any errors
        with open(log_file, "a") as f:
            f.write(f"\n=== ERROR ===\n")
            f.write(f"Error: {str(e)}\n")
            f.write(f"Type: {type(e).__name__}\n\n")
            f.write("Traceback:\n")
            f.write(traceback.format_exc())
        
        # Re-raise so the app still crashes visibly
        raise