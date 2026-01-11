from pydantic import StringConstraints

NAME_PATTERN = r"^[a-zA-Z0-9-.]+$"
PASSWORD_PATTERN = r"^[a-zA-Z0-9!@#$%^&*-.]+$"
ROOMID_PATTERN = r"^[a-zA-Z0-9]+$"
PIN_PATTERN = r"\d"

NameStringMetadata = StringConstraints(
    strip_whitespace=True,
    to_lower=True,
    strict=True,
    min_length=2,
    max_length=16,
    pattern=NAME_PATTERN,
)

PWStringMetadata = StringConstraints(
    strip_whitespace=True,
    to_lower=True,
    strict=True,
    min_length=2,
    max_length=16,
    pattern=PASSWORD_PATTERN,
)

RoomIDMetadata = StringConstraints(
    strip_whitespace=True,
    strict=True,
    min_length=8,
    max_length=8,
    pattern=ROOMID_PATTERN,
)

RoomPINMetadata = StringConstraints(
    strip_whitespace=True,
    strict=True,
    min_length=4,
    max_length=4,
    pattern=PIN_PATTERN,
)
