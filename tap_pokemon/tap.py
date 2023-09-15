"""Pokemon tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_pokemon import streams


class TapPokemon(Tap):
    """Pokemon tap class."""

    name = "tap-pokemon"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_url",
            th.StringType,
            default="https://pokeapi.co/api/v2",
            description="The url for the Pokemon API",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.PokemonStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.PokemonIDStream(self),
            streams.PokemonStream(self),
        ]


if __name__ == "__main__":
    TapPokemon.cli()
