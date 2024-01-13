import pytest
import os
from utils import (
    get_response,
    code_test,
    contained_text_test,
    write_lib,
    STANDARD_INITAL_LIB,
)


def test_search():
    # Use the standard initial library state
    write_lib(STANDARD_INITAL_LIB)

    # Search with wrong category
    code_test("search wrongcategory 0", 102)

    # Search with non-existent ID (Author)
    code_test("search author 999", 403)

    # Search with non-existent ID (Tag)
    code_test("search tag 999", 401)

    # Search with invalid ID format (Author)
    code_test("search author", 103)
    code_test("search author abc", 103)

    # Search with invalid ID format (Tag)
    code_test("search tag", 103)
    code_test("search tag abc", 103)

    # Successful search for an existing author
    contained_text_test("search author 0", "0")

    # Successful search for an existing tag
    contained_text_test("search tag 0", "0")

    code_test("add tag soe", 100)
    code_test("search tag 3", 405)

    code_test("add author new author", 100)
    code_test("search author 3", 405)


def test_help_command():
    # Test the help command
    response = get_response("help")
    expected_commands = [
        "help",
        "list",
        "add",
        "delete",
        "show",
        "borrow",
        "return",
        "status",
        "search",
    ]
    for command in expected_commands:
        assert command in response, f"Help command missing info on: {command}"


def make_file_unreadable(filename):
    """Change file permissions to make it unreadable."""
    os.chmod(filename, 0o200)  # Write-only permission


def make_file_unwritable(filename):
    """Change file permissions to make it unwritable."""
    os.chmod(filename, 0o400)  # Read-only permission


def reset_file_permissions(filename):
    """Reset file permissions to read-write."""
    os.chmod(filename, 0o600)  # Read-write permission (owner only)


def test_file_read_write_errors():
    # Ensure the library file exists for this test
    write_lib(STANDARD_INITAL_LIB)

    # Simulate file read error
    make_file_unreadable("library")
    code_test("list books", 601)

    # Reset permissions to perform next test
    reset_file_permissions("library")

    # Simulate file write error
    make_file_unwritable("library")
    code_test("add author New Author", 602)

    # Reset file permissions to normal after tests
    reset_file_permissions("library")
