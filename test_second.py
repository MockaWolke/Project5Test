import pytest
from utils import (
    get_response,
    code_test,
    contained_text_test,
    write_lib,
    STANDARD_INITAL_LIB,
)


def test_status_command_scenarios():
    # Setup the initial library state
    initial_library = """
    [tags]
        0 Novel
        1 Sci-fi
        2 Fantasy

    [authors]
        0 Frank Herbert
        1 William Gibson
        2 Neil Gaiman

    [books]
        0 0 %Dune% 978-0441172719 0 2
        1 1 %Neuromancer% 978-3608504880 0 1
        2 2 %American Gods% 978-3847905875 2

    [users]
        0 Arthur Morgan
        1 Corvo Attano
        2 Harry DuBois
        4 Gerr  Anasda

    [borrowentries]
        2 1
        1 0
    """

    write_lib(initial_library)

    code_test("status book 2", "300")

    code_test("status book 0", "301")

    code_test("status user 4", "302")

    code_test("status user 42", "404")

    code_test("status book 42", "402")


def test_empty_library():
    write_lib("")

    code_test("add tag sometag", "100")

    contained_text_test("list tags", "sometag")

    code_test("list authors", "405")  # suche gab kein ergebniss?


def test_add_invalid_data():
    write_lib("")

    # testinng books

    code_test("add book noid", "104")
    code_test("add book 1 nodelimiter", "104")

    # author yet in there
    code_test("add book 0 %American Gods 2% 978-3847905872 1", "403")

    code_test("add author Frank Herbert", "100")  # add it

    # tag not in there
    code_test("add book 0 %American Gods 2% 978-3847905872 1", "401")

    code_test("add tag sometag", "100")  # add it
    code_test("add tag anothertag", "100")  # add it
    code_test("add book 0 %American Gods 2% 978-3847905872 1", "100")

    contained_text_test("show book 0", "%American Gods 2%")

    # testing tags

    code_test("add tag", "107")

    # testing authors

    code_test("add author", "106")
    code_test("add author OnlyFirst", "106")
    code_test("add author Valid Name", "100")

    contained_text_test("list authors", ["Valid", "Name"])

    # testing users

    code_test("add user", "105")
    code_test("add user OnlyFirst", "105")

    code_test("add user Valid Name", "100")

    contained_text_test("list users", ["Valid", "Name"])


def test_borrow():
    write_lib(
        """[tags]
    0 Novel
    1 Sci-fi
    2 Fantasy

[authors]
    0 Frank Herbert
    1 William Gibson
    2 Neil Gaiman

[books]
    0 0 %Dune% 978-0441172719 0 2
    1 1 %Neuromancer% 978-3608504880 0 1
    2 2 %American Gods% 978-3847905875 2

[users]
    0 Arthur Morgan
    1 Corvo Attano
    2 Harry DuBois
    4 Gerr  Anasda

[borrowentries]

"""
    )

    code_test("borrow", 103)
    code_test("borrow sas assa", 103)
    code_test("borrow sas 123", 103)
    code_test("borrow 122 as 123", 103)

    # user or book not found
    code_test("borrow 10 10", 404)
    code_test("borrow 0 10", 402)

    # success
    code_test("borrow 0 0", 100)

    # someone else
    code_test("borrow 1 0", 301)


def test_return():
    write_lib(
        """[tags]
    0 Novel
    1 Sci-fi
    2 Fantasy

[authors]
    0 Frank Herbert
    1 William Gibson
    2 Neil Gaiman

[books]
    0 0 %Dune% 978-0441172719 0 2
    1 1 %Neuromancer% 978-3608504880 0 1
    2 2 %American Gods% 978-3847905875 2

[users]
    0 Arthur Morgan
    1 Corvo Attano
    2 Harry DuBois
    4 Gerr  Anasda

[borrowentries]
     0 0 
     1 1
"""
    )

    code_test("return", 103)
    code_test("return sas assa", 103)
    code_test("return sas 123", 103)
    code_test("return 122 as 123", 103)

    # user or book not found
    code_test("return 10 10", 404)
    code_test("return 0 10", 402)

    code_test("return 2 2", 304)
    code_test("return 1 0", 304)
    code_test("return 0 1", 304)

    code_test("return 0 0", 100)

    code_test("status user 0", 302)
    code_test("status book 0", 300)

    code_test("status book 1", 301)
    contained_text_test("status user 1", "1")


def test_delete_function():
    # Custom initial library state
    initial_library = """
    [tags]
    0 Novel
    1 Sci-fi
    2 Fantasy

    [authors]
    0 Frank Herbert
    1 William Gibson
    2 Neil Gaiman

    [books]
    0 0 %Dune% 978-0441172719 0 2
    1 1 %Neuromancer% 978-3608504880 0 1
    2 2 %American Gods% 978-3847905875 2
    3 2 %American Gods2% 978-3847905875 2

    [users]
    0 Arthur Morgan
    1 Corvo Attano
    2 Harry DuBois
    4 Gerr  Anasda

    [borrowentries]
    0 2
    1 0
    """

    write_lib(initial_library)

    # Non-existent entities
    code_test("delete tag 999", 401)
    code_test("delete author 999", 403)
    code_test("delete user 999", 404)
    code_test("delete book 999", 402)

    # Entities in use
    code_test("delete tag 0", 201)
    code_test("delete author 0", 202)
    code_test("delete user 0", 203)
    code_test("delete book 0", 204)

    # valid deletes
    code_test("delete user 4", 100)

    code_test("add author not me", 100)
    code_test("delete author 3", 100)

    code_test("add tag sometag", 100)
    code_test("delete tag 3", 100)

    code_test("delete book 3", 100)
