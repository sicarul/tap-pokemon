"""Stream type classes for tap-pokemon."""

from __future__ import annotations

import typing as t
from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_pokemon.client import BasePokemonStream

class PokemonIDStream(BasePokemonStream):
    """Define custom stream."""

    name = "pokemon_id"
    path = "/pokemon"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    records_jsonpath = "$.results[*]"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property(
            "id",
            th.IntegerType,
            description="The pokemon's ID",
        )
    ).to_dict()


    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        
        row['id'] = int(row['url'].split('/')[-2])
        return row


    def get_child_context(self, record: dict, context: t.Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "id": record["id"]
        }

# NamedAPIResource is a common type in the API so we define it here to avoid redefining it each time in the schema
NamedAPIResource = th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("url", th.StringType),
        )

class PokemonStream(BasePokemonStream):
    """Define custom stream."""

    name = "pokemon"
    path = "/pokemon/{id}"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    parent_stream_type = PokemonIDStream
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("order", th.IntegerType),
        th.Property("base_experience", th.IntegerType),
        th.Property("height", th.IntegerType),
        th.Property("weight", th.IntegerType),
        th.Property("abilities", th.ArrayType(th.ObjectType(
            th.Property("ability", NamedAPIResource),
            th.Property("is_hidden", th.BooleanType),
            th.Property("slot", th.IntegerType)
        ))),
        th.Property("forms", th.ArrayType(NamedAPIResource)),
        th.Property("game_indices", th.ArrayType(th.ObjectType(
            th.Property("game_index", th.IntegerType),
            th.Property("version", NamedAPIResource)),
        )),
        th.Property("held_items", th.ArrayType(th.ObjectType(
            th.Property("item", NamedAPIResource),
            th.Property("version_details", th.ArrayType(th.ObjectType(
                th.Property("version", NamedAPIResource),
                th.Property("rarity", th.IntegerType),
            ))
        )))),
        th.Property("is_default", th.BooleanType),
        th.Property("location_area_encounters", th.StringType),
        th.Property("moves", th.ArrayType(th.ObjectType(
            th.Property("move", NamedAPIResource),
            th.Property("version_group_details", th.ArrayType(th.ObjectType(
                th.Property("move_learn_method", NamedAPIResource),
                th.Property("version_group", NamedAPIResource),
                th.Property("level_learned_at", th.IntegerType),
            ))
        )))),
        th.Property("past_types", th.ArrayType(th.ObjectType(
            th.Property("generation", NamedAPIResource),
            th.Property("types", th.ArrayType(th.ObjectType(
                th.Property("type", NamedAPIResource),
                th.Property("slot", th.IntegerType),
            ))
        )))),
        th.Property("species", NamedAPIResource),
        th.Property("sprites", th.ObjectType(
            th.Property("back_default", th.StringType),
            th.Property("back_female", th.StringType),
            th.Property("back_shiny", th.StringType),
            th.Property("back_shiny_female", th.StringType),
            th.Property("front_default", th.StringType),
            th.Property("front_female", th.StringType),
            th.Property("front_shiny", th.StringType),
            th.Property("front_shiny_female", th.StringType),
            th.Property("other", th.ObjectType(additional_properties=True)),
            th.Property("versions", th.ObjectType(additional_properties=True)),
        )),
        th.Property("stats", th.ArrayType(th.ObjectType(
            th.Property("base_stat", th.IntegerType),
            th.Property("effort", th.IntegerType),
            th.Property("stat", NamedAPIResource)
        ))),
        
    ).to_dict()
