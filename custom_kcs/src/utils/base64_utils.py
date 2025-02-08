import base64
import re
import binascii

def clean_base64(base64_string):
    return re.sub(r"^data:image/\w+;base64,", "", base64_string)

def fix_base64_encoding(base64_string):
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += '=' * (4 - missing_padding)
    return base64_string

def is_valid_base64(base64_string):
    try:
        base64.b64decode(base64_string, validate=True)
        return True
    except binascii.Error:
        return False

def decode_base64(base64_string):
    base64_string = clean_base64(base64_string)
    base64_string = fix_base64_encoding(base64_string)

    if not is_valid_base64(base64_string):
        raise ValueError("Invalid base64 image data.")

    return base64.b64decode(base64_string)
