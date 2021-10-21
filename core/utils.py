
import math
import random
import re
import string
import unicodedata

from fastapi import Depends, HTTPException


def random_string(size: int, chars: str = string.ascii_lowercase+string.digits) -> str:
    """
    Generate random strings from a given size
    """
    return "".join(random.choices(chars, k = size))


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def unique_slug_generator(value, new_slug=False):
    """
    This generates a unique slug using your model slug value
    assuming there's a model with a slug field and 
    a title character (char) field.
    If a slug exists, it generates a unique slug with the old and random
    otherwise, it generates a new slug
    """
    if new_slug:
        return f"{slugify(value)}-{random_string(4)}"
    return slugify(value)


def count_words(content):
    """Count all the words received from a parameter."""
    matching_words = re.findall(r'\w+', content)
    count = len(matching_words)
    return count


def get_read_time(content):
    """Get the read length by dividing with an average of 200wpm """
    count = count_words(content)
    read_length_min = math.ceil(count/200.0)
    return int(read_length_min)
