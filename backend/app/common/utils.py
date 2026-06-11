from __future__ import annotations

import hashlib
import json
import re
import secrets
import string
import uuid

from datetime import datetime
from datetime import timezone

from urllib.parse import urlparse


# =========================================================
# IDs
# =========================================================

def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_short_id(
    length: int = 12,
) -> str:

    alphabet = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def generate_share_id(
    length: int = 16,
) -> str:

    return secrets.token_urlsafe(
        length
    )


def is_valid_uuid(
    value: str,
) -> bool:

    try:
        uuid.UUID(str(value))
        return True

    except Exception:
        return False


# =========================================================
# Datetime
# =========================================================

def utc_now() -> datetime:

    return datetime.now(
        timezone.utc
    )


def utc_iso() -> str:

    return utc_now().isoformat()


# =========================================================
# Text Helpers
# =========================================================

def normalize_text(
    text: str,
) -> str:

    return " ".join(
        text.split()
    )


def normalize_search_text(
    text: str,
) -> str:

    return normalize_text(
        text.strip().lower()
    )


def truncate(
    text: str,
    length: int = 100,
) -> str:

    if len(text) <= length:
        return text

    return text[:length] + "..."


# =========================================================
# Slugs
# =========================================================

def slugify(
    text: str,
) -> str:

    text = normalize_text(
        text.lower()
    )

    text = re.sub(
        r"[^a-z0-9\s-]",
        "",
        text,
    )

    text = re.sub(
        r"\s+",
        "-",
        text,
    )

    text = re.sub(
        r"-+",
        "-",
        text,
    )

    return text.strip("-")


# =========================================================
# Security
# =========================================================

def generate_token(
    length: int = 32,
) -> str:

    return secrets.token_urlsafe(
        length
    )


def sha256_hash(
    value: str,
) -> str:

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def mask_email(
    email: str,
) -> str:

    if "@" not in email:
        return email

    username, domain = email.split(
        "@",
        1,
    )

    if len(username) <= 2:
        return (
            username[0]
            + "***@"
            + domain
        )

    return (
        username[:2]
        + "***@"
        + domain
    )


def mask_token(
    token: str,
) -> str:

    if len(token) < 10:
        return "***"

    return (
        token[:5]
        + "..."
        + token[-5:]
    )


# =========================================================
# Email
# =========================================================

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def is_valid_email(
    email: str,
) -> bool:

    return bool(
        EMAIL_REGEX.match(
            email.strip()
        )
    )


def normalize_email(
    email: str,
) -> str:

    return (
        email
        .strip()
        .lower()
    )


# =========================================================
# Username
# =========================================================

USERNAME_REGEX = re.compile(
    r"^[a-z0-9_]{3,30}$"
)


def normalize_username(
    username: str,
) -> str:

    username = (
        username
        .strip()
        .lower()
    )

    username = re.sub(
        r"\s+",
        "_",
        username,
    )

    username = re.sub(
        r"[^a-z0-9_]",
        "",
        username,
    )

    return username


def is_valid_username(
    username: str,
) -> bool:

    username = normalize_username(
        username
    )

    return bool(
        USERNAME_REGEX.match(
            username
        )
    )


# =========================================================
# URL
# =========================================================

def is_valid_url(
    url: str,
) -> bool:

    try:

        result = urlparse(
            url.strip()
        )

        return (
            result.scheme
            in {"http", "https"}
            and bool(result.netloc)
        )

    except Exception:

        return False


# =========================================================
# Collections
# =========================================================

def remove_none_values(
    data: dict,
) -> dict:

    return {
        key: value
        for key, value in data.items()
        if value is not None
    }


def unique_list(
    items: list,
) -> list:

    seen = set()

    result = []

    for item in items:

        if item not in seen:

            seen.add(item)

            result.append(item)

    return result


# =========================================================
# Pagination
# =========================================================

def calculate_offset(
    page: int,
    limit: int,
) -> int:

    page = max(page, 1)

    limit = max(limit, 1)

    return (
        page - 1
    ) * limit


# =========================================================
# File Utilities
# =========================================================

def safe_filename(
    filename: str,
) -> str:

    return re.sub(
        r"[^\w.\-]",
        "_",
        filename,
    )


# =========================================================
# Debug
# =========================================================

def pretty_dict(
    data: dict,
) -> str:

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
        default=str,
    )