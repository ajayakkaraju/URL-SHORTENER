
import random
import string
import re

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(https?://)'  # http:// or https://
        r'([\w.-]+)'    # domain
        r'([:/?#][^\s]*)?$', re.IGNORECASE)
    return re.match(regex, url) is not None