import os
import shutil
from subprocess import Popen, PIPE
from typing import Union

EXECUTABLE_PATH = "../eidppr4-bjarne2/cmake-build-debug/eidppr4_bjarne2"


shutil.copy(EXECUTABLE_PATH, "executable")


def get_response(command: str):
    commands = ["./executable"] + command.split()
    process = Popen(commands, stdout=PIPE, stderr=PIPE)

    stdoutput, stderrput = process.communicate()
    return stdoutput.decode("UTF-8")


def code_test(command: str, code: str | int):
    response = get_response(command)
    assert response.startswith(str(code)), f"Expected {code}. Got {response}"


def contained_text_test(command: str, texts: list[str] | str):
    response = get_response(command)

    if isinstance(texts, str):
        texts = [texts]

    for text in texts:
        assert text in response, f"Expected {text} in {response}"


def write_lib(library: str):
    with open("library", "w") as f:
        f.write(library)


STANDARD_INITAL_LIB = """[tags]
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


if __name__ == "__main__":
    rest = get_response("show user 0")
    print(rest, type(rest))
