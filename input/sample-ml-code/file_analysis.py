import os
import sys
from collections import defaultdict
from pathlib import Path

def get_file_sizes(folder_path):
    file_sizes = defaultdict(int)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.is_symlink():
                continue
            ext = file_path.suffix[1:] if file_path.suffix else "No extension"
            #if ext=='.py' or (file_path.stat().st_size != 0 and file_path.stat().st_size < 2000) :
            if ext=='py' or ext=='md' :
                file_sizes[ext] += file_path.stat().st_size
    return dict(sorted(file_sizes.items(), key=lambda x: x[1], reverse=True))

def main(folder_path="."):
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            print(f"\nFolder: {entry.name}")
            file_sizes = get_file_sizes(entry.path)
            for ext, size in file_sizes.items():
                print(f"Extension: .{ext} - Total weight: {round(size/1000000,3)} MB")

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    main(folder_path)


