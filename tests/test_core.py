"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_pokemon.tap import TapPokemon

SAMPLE_CONFIG = {
}


# Run standard built-in tap tests from the SDK:
TestTapPokemon = get_tap_test_class(
    tap_class=TapPokemon,
    config=SAMPLE_CONFIG,
)

