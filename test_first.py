import pytest
from utils import (
    get_response,
    code_test,
    contained_text_test,
    write_lib,
    STANDARD_INITAL_LIB,
)


def test_one():
    write_lib(STANDARD_INITAL_LIB)

    code_test("invalid command", "101")

    code_test("delete author 0", "202")

    code_test("add tag Mystery", "100")

    code_test("delete tag 3", "100")

    contained_text_test("list books", ["Dune"])

    code_test("add author J.K. Rowling", "100")

    code_test("delete author 3", "100")


def test_show_functionality():
    write_lib(STANDARD_INITAL_LIB)

    # Show author
    contained_text_test("show author 0", ["Frank", "Herbert"])

    # Show tag
    contained_text_test("show tag 1", ["Sci-fi"])

    # Show user
    contained_text_test("show user 2", ["DuBois"])

    # Show book
    contained_text_test("show book 0", ["Dune", "978-0441172719"])

    code_test("show borrowentry 0", "102")

    code_test("show author 999", "403")

    code_test("show tag 999", "401")

    code_test("show user 999", "404")

    code_test("show book 999", "402")
