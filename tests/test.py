import pytest

def test_import():
    from debuggy import core
    return core._get_caller_path()

def test_stackoverflow_parser():
    from stalkoverflow import parsers
    assert parsers.StackOverflow('https://stackoverflow.com/questions/28665528/while-do-while-for-loops-in-assembly-language-emu8086')

def test_google_parser():
    from stalkoverflow import parsers
    assert parsers.GSearch('how to use loops')

def test_ui():
    from stalkoverflow import ui
    assert ui.start_app(['https://stackoverflow.com/questions/28665528/while-do-while-for-loops-in-assembly-language-emu8086'],['While, Do While, For loops in Assembly Language (emu8086)'])


def test_handler():
    from stalkoverflow import handler
    assert handler.execute('\data\log.err',4)


