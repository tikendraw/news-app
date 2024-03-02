from pathlib import Path

files = []


def check_path(path):
    p = Path(path)
    if p.is_file and not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return
    else:
        p.mkdir(parents=True, exist_ok=True)
        return


if __name__ == "__main__":
    for f in files:
        check_path(f)
