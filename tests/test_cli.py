import os
import tempfile
import pytest
from workspace_stats.cli import analyze_directory


def test_analyze_empty_directory():
    """Test analysis of an empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        stats = analyze_directory(tmpdir)
        assert stats["total_files"] == 0
        assert stats["total_size_bytes"] == 0


def test_analyze_single_file():
    """Test analysis with a single file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("hello")
        stats = analyze_directory(tmpdir)
        assert stats["total_files"] == 1
        assert stats["total_size_bytes"] == 5
        assert ".txt" in stats["extensions"]


def test_analyze_multiple_extensions():
    """Test extension counting."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .py file
        py_file = os.path.join(tmpdir, "script.py")
        with open(py_file, "w") as f:
            f.write("print('hi')")
        
        # Create .md file
        md_file = os.path.join(tmpdir, "readme.md")
        with open(md_file, "w") as f:
            f.write("# Hello")

        stats = analyze_directory(tmpdir)
        assert stats["total_files"] == 2
        assert stats["extensions"].get(".py", 0) == 1
        assert stats["extensions"].get(".md", 0) == 1
