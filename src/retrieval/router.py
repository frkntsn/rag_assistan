from typing import Literal

RouteType = Literal["person", "place", "both"]


PERSON_HINTS = {"who", "person", "scientist", "artist", "singer", "player"}
PLACE_HINTS = {"where", "located", "place", "city", "country", "monument"}
COMPARE_HINTS = {"compare", "difference", "versus", " vs "}
PERSON_SPECIFIC_HINTS = {"discover", "famous", "known for", "associated with", "who was"}
PLACE_SPECIFIC_HINTS = {"used for", "important", "located", "where is", "what is"}


def route_query(query: str) -> RouteType:
    q = f" {query.lower()} "
    if any(token in q for token in COMPARE_HINTS):
        return "both"

    has_person = any(token in q for token in PERSON_HINTS)
    has_place = any(token in q for token in PLACE_HINTS)
    has_person_specific = any(token in q for token in PERSON_SPECIFIC_HINTS)
    has_place_specific = any(token in q for token in PLACE_SPECIFIC_HINTS)

    if (has_person or has_person_specific) and not (has_place or has_place_specific):
        return "person"
    if (has_place or has_place_specific) and not (has_person or has_person_specific):
        return "place"
    return "both"
