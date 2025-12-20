from pydantic import StringConstraints

USERNAME_PATTERN = r"^[a-zA-z0-9-.]+$"
PASSWORD_PATTERN = r"^[a-zA-z0-9!@#$%^&*-.]+$"
PIN_PATTERN = r"\d{4}"

UsernameStringMetadata = StringConstraints(
    strip_whitespace=True,
    to_lower=True,
    strict=True,
    min_length=2,
    max_length=16,
    pattern=USERNAME_PATTERN,
)

PWStringMetadata = StringConstraints(
    strip_whitespace=True,
    to_lower=True,
    strict=True,
    min_length=2,
    max_length=16,
    pattern=USERNAME_PATTERN,
)

RoomPINMetadata = StringConstraints(
    strip_whitespace=True,
    strict=True,
    pattern=PIN_PATTERN,
)
