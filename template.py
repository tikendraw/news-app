from pathlib import Path

files = [
    ".github/workflow/ci.yaml",
    ".github/workflow/publish_python_package.yaml",
    "src/__init__.py",
    "src/demo.py",
    "src/croc.py",
    "tests/__init__.py",
    "tox.ini",
    ".pre-commit-config.yaml",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "requirements.txt",
    "README.md",
    "LICENSE",
    ".gitignore",
    "data",
    "src/piplines",
    "models",

]


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