from datetime import datetime, timezone
from slugify import slugify

def utc_now() -> datetime:
    """Returns the current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)

def generate_slug(name: str) -> str:
    """Generate a URL-friendly slug from a name string, supporting Vietnamese characters."""
    return slugify(name, allow_unicode=False)
