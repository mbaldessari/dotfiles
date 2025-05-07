import os
import codecs
from pathlib import Path


def rmdir(directory: Path):
    assert directory.is_dir()
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


if __name__ == "__main__":
    repo_path = Path("simple-icons")
    icons_path = Path("icons")

    if not repo_path.exists():  # Check if the GitHub repo is not there
        print("Downloading GitHub repository...")
        os.system("git clone https://github.com/simple-icons/simple-icons.git")

    # Delete and create "icons" directory
    if icons_path.exists():
        rmdir(icons_path)

    icons_path.mkdir()
    (icons_path / "black").mkdir()
    (icons_path / "white").mkdir()

    # Find every icon
    for root, dirs, files in (repo_path / "icons").walk():
        for file in files:
            icon_path = root / file

            if icon_path.suffix == ".svg":
                target_path = icons_path / "black" / file
                # Copy icon
                target_path.write_bytes(icon_path.read_bytes())

                # Open icon
                with codecs.open(str(icon_path), encoding="utf-8", errors="ignore") as svg:
                    content = svg.read()

                    content = content.replace('path d=', 'path fill="white" d=')
                    (icons_path / "white" / file).write_text(content)

rmdir(Path("simple-icons/"))
