import os
import shutil
from pathlib import Path

def cleanup_media():
    # Get the base directory
    base_dir = Path(__file__).resolve().parent.parent
    
    # Media directories to clean
    dirs_to_clean = [
        base_dir / 'media' / 'uploads',
        base_dir / 'media' / 'processed'
    ]
    
    for directory in dirs_to_clean:
        if directory.exists():
            # Remove all files except .gitkeep
            for item in directory.iterdir():
                if item.name != '.gitkeep':
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            print(f"Cleaned {directory}")
        else:
            # Create directory if it doesn't exist
            directory.mkdir(parents=True, exist_ok=True)
            # Create .gitkeep file
            (directory / '.gitkeep').touch()
            print(f"Created {directory}")

if __name__ == "__main__":
    cleanup_media()
