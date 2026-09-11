import argparse
import os
from pathlib import Path


def analyze_directory(root_path):
    """Analyze a directory and return statistics."""
    total_files = 0
    total_size = 0
    extensions = {}

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            total_files += 1
            file_path = Path(dirpath) / filename
            try:
                total_size += file_path.stat().st_size
            except FileNotFoundError:
                pass

            ext = file_path.suffix.lower()
            extensions[ext] = extensions.get(ext, 0) + 1

    return {
        "total_files": total_files,
        "total_size_bytes": total_size,
        "extensions": extensions
    }


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Report workspace statistics")
    parser.add_argument("path", nargs="?", default=".", help="Directory to analyze")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a directory")
        return 1

    stats = analyze_directory(args.path)

    print(f"Directory: {args.path}")
    print(f"Total Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size_bytes']} bytes")
    print("Extensions:")
    for ext, count in sorted(stats['extensions'].items()):
        print(f"  {ext}: {count}")
    return 0


if __name__ == "__main__":
    exit(main())
