import itertools
import tempfile
from pathlib import Path
from termcolor import colored
import re


# Simple colorized output decorator
def colorized_output(func):
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    cycle = itertools.cycle(colors)

    def wrapper(*args, **kwargs):
        color = next(cycle)
        result = func(*args, **kwargs)
        if isinstance(result, str):
            print(colored(result, color))
        return result

    return wrapper


class FileReader:  # basic file reader class
    def __init__(self, filepath: str):
        self._filepath = Path(filepath)

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, path_str: str):
        self._filepath = Path(path_str)

    def _line_gen(self):
        with self._filepath.open("r", encoding="utf-8") as file:
            for line in file:
                yield line.strip()

    def get_content(self):
        return [line for line in self._line_gen()]

    @staticmethod
    def default_extension():
        return ".txt"

    @classmethod
    def from_name(cls, name: str):
        return cls(name)

    def __str__(self):
        return f"FileReader({self._filepath})"

    def __add__(self, other):
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
            with self._filepath.open(encoding="utf-8") as f1, other._filepath.open(encoding="utf-8") as f2:
                tmp.writelines(f1.readlines() + f2.readlines())
            return FileReader(tmp.name)


class FancyFileReader(FileReader):
    @colorized_output
    def print_content(self):
        return "\n".join(self.get_content())

    def concat_many(self, *files):
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
            for file in (self, *files):
                with file.filepath.open(encoding="utf-8") as f:
                    tmp.writelines(f.readlines())
            return FancyFileReader(tmp.name)

    def search_string(self, query: str, highlight_color: str = "red"):
        print(f"\n🔍 Searching for: '{query}' in {self.filepath.name}")
        found = False
        for idx, line in enumerate(self._line_gen(), start=1):
            if query.lower() in line.lower():
                found = True
                # Case-insensitive replacement
                pattern = re.compile(re.escape(query), re.IGNORECASE)
                highlighted = pattern.sub(
                    colored(query, highlight_color, attrs=["bold"]), line
                )
                print(f"Line {idx}: {highlighted}")
        if not found:
            print("No matches found.")


# Interactive usage
if __name__ == "__main__":
    search_dir = Path("search")
    search_dir.mkdir(exist_ok=True)

    file_defaults = {
        "fruit_vegetables_big.txt": "Apple\nBanana\nCarrot\n",
        "countries_cities.txt": "USA\nNew York\nFrance\nParis\n",
        "cities_fruits.txt": "London\nOrange\nTokyo\nGrape\n",
    }
    for fname, content in file_defaults.items():
        path = search_dir / fname
        if not path.exists():
            with path.open("w") as f:
                f.write(content)

    query = input("Enter a string to search in all files in the 'venv' folder: ").strip()

    valid_colors = [
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "grey",
    ]
    color = input(f"Choose a highlight color {valid_colors}: ").strip().lower()

    if color not in valid_colors:
        print(f" Invalid color. Defaulting to 'red'.")
        color = "red"

    # Search in all files in the 'venv' folder
    for file_path in search_dir.glob("*.txt"):
        reader = FancyFileReader(str(file_path))
        reader.search_string(query, color)
