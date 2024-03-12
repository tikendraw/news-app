import os 
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s:')



files=[
    ".github/workflows/.gitkeep",

]

def check_path(path):
    p = Path(path)
    if p.is_file and not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        logging.info(f"Created file: {path}")
        return
    else:
        p.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")
        return


if __name__ == "__main__":
    for f in files:
        check_path(f)
