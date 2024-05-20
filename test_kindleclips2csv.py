import pytest
from kindleclips2csv import parse_clippings


def test_parse_clippings_english_location():
    clippings_text = """The Master Algorithm
- Your Highlight on Location 177-179 | Added on Monday, May 13, 2024 3:34:35 PM

what it requires is stepping back from the mathematical arcana to see the overarching pattern of learning phenomena; and for this the layman, approaching the forest from a distance, is in some ways better placed than the specialist, already deeply immersed in the study of particular trees.
==========
"""
    clippings = parse_clippings(clippings_text)

    # Ensure that the correct number of clippings are parsed
    assert len(clippings) == 1

    # Check the content of the clipping
    assert clippings[0]['bookTitle'] == 'The Master Algorithm'
    assert clippings[0]['clipping_type'] == 'Highlight'
    assert clippings[0]['location_type'] == 'Location'
    assert clippings[0]['location_start'] == 177
    assert clippings[0]['location_end'] == 179
    assert clippings[0]['content'] == 'what it requires is stepping back from the mathematical arcana to see the overarching pattern of learning phenomena; and for this the layman, approaching the forest from a distance, is in some ways better placed than the specialist, already deeply immersed in the study of particular trees.'
    assert clippings[0]['addedDate'] == 'Monday, May 13, 2024 3:34:35 PM'


def test_parse_clippings_english_page():
    clippings_text = """The Master Algorithm
- Your Highlight on page 232 | Added on Monday, May 13, 2024 3:34:35 PM

what it requires is stepping back from the mathematical arcana to see the overarching pattern of learning phenomena; and for this the layman, approaching the forest from a distance, is in some ways better placed than the specialist, already deeply immersed in the study of particular trees.
==========
"""
    clippings = parse_clippings(clippings_text)

    # Ensure that the correct number of clippings are parsed
    assert len(clippings) == 1

    # Check the content of the clipping
    assert clippings[0]['bookTitle'] == 'The Master Algorithm'
    assert clippings[0]['clipping_type'] == 'Highlight'
    assert clippings[0]['location_type'] == 'page'
    assert clippings[0]['location_start'] == 232
    assert clippings[0]['content'] == 'what it requires is stepping back from the mathematical arcana to see the overarching pattern of learning phenomena; and for this the layman, approaching the forest from a distance, is in some ways better placed than the specialist, already deeply immersed in the study of particular trees.'
    assert clippings[0]['addedDate'] == 'Monday, May 13, 2024 3:34:35 PM'


def test_parse_clippings_german_location():
    clippings_text = """Kotlin in Action
- Ihre Markierung bei Position 3552-3553 | Hinzugefügt am Montag, 10. September 2018 16:05:47

Wenn wir über Kotlin sprechen, sagen wir gerne, dass es eine pragmatische, präzise, sichere Sprache mit Schwerpunkt auf Interoperabilität ist.
==========
"""
    clippings = parse_clippings(clippings_text)

    # Ensure that the correct number of clippings are parsed
    assert len(clippings) == 1

    # Check the content of the clipping
    assert clippings[0]['bookTitle'] == 'Kotlin in Action'
    assert clippings[0]['clipping_type'] == 'Highlight'
    assert clippings[0]['location_type'] == 'Location'
    assert clippings[0]['location_start'] == 3552
    assert clippings[0]['location_end'] == 3553
    assert clippings[0]['content'] == 'Wenn wir über Kotlin sprechen, sagen wir gerne, dass es eine pragmatische, präzise, sichere Sprache mit Schwerpunkt auf Interoperabilität ist.'
    assert clippings[0]['addedDate'] == 'Montag, 10. September 2018 16:05:47'


def test_parse_clippings_german_page():
    clippings_text = """Kotlin in Action
- Ihre Markierung auf Seite 232 | Hinzugefügt am Montag, 10. September 2018 16:05:47

Wenn wir über Kotlin sprechen, sagen wir gerne, dass es eine pragmatische, präzise, sichere Sprache mit Schwerpunkt auf Interoperabilität ist.
==========
"""
    clippings = parse_clippings(clippings_text)

    # Ensure that the correct number of clippings are parsed
    assert len(clippings) == 1

    # Check the content of the clipping
    assert clippings[0]['bookTitle'] == 'Kotlin in Action'
    assert clippings[0]['clipping_type'] == 'Highlight'
    assert clippings[0]['location_type'] == 'page'
    assert clippings[0]['location_start'] == 232
    assert clippings[0]['content'] == 'Wenn wir über Kotlin sprechen, sagen wir gerne, dass es eine pragmatische, präzise, sichere Sprache mit Schwerpunkt auf Interoperabilität ist.'
    assert clippings[0]['addedDate'] == 'Montag, 10. September 2018 16:05:47'


def test_parse_bookmark_german_position():
    clippings_text = """The Girl with the Dragon Tattoo (Stieg Larsson)
- Ihr Lesezeichen bei Position 1978 | Hinzugefügt am Montag, 3. September 2018 00:34:42


==========
"""
    clippings = parse_clippings(clippings_text)

    assert len(clippings) == 1
    assert clippings[0]['bookTitle'] == 'The Girl with the Dragon Tattoo (Stieg Larsson)'
    assert clippings[0]['clipping_type'] == 'Bookmark'
    assert clippings[0]['location_type'] == 'Location'
    assert clippings[0]['location_start'] == 1978
