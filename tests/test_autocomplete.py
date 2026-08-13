"""
Unit Tests for Devanagari Autocomplete Engine (`nepalinlplibrary.library.autocomplete`)
"""

import pytest

try:
    from nepalinlplibrary.library.autocomplete import AutocompleteEngine
except ModuleNotFoundError:
    from library.autocomplete import AutocompleteEngine

def test_autocomplete_insert_and_search():
    engine = AutocompleteEngine()
    engine.insert("नेपाल", 100)
    engine.insert("नमस्ते", 50)
    engine.insert("नेपाली", 80)

    results = engine.get_top_k("ने", k=2)
    words = [r[0] for r in results]

    assert "नेपाल" in words
    assert "नेपाली" in words
    assert len(results) == 2

def test_autocomplete_frequency_learning():
    engine = AutocompleteEngine()
    engine.insert("कुकुर", 10)
    engine.insert("काठमाडौँ", 20)

    engine.learn_frequency("कुकुर", count=30)
    results = engine.get_top_k("क", k=2)
    assert results[0][0] == "कुकुर"
    assert results[0][1] == 40
