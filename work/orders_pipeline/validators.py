""" Checks whether values and records are valid, tells the reason why they aren't"""

def safe_to_float(value):
    """Return value as a float, or raise a clear error for bad input."""
    try:
        result = float(value)
    except ValueError as err:
        raise ValueError(f"{value!r} cannot be converted into a float") from err
    except TypeError as err:
        raise TypeError(f"Expected a number or string, got {type(value).__name__}") from err
    else:
        return result


def is_number(value):
    """Return True if value can be converted to a float, False otherwise."""
    try:
        safe_to_float(value)
    except (ValueError, TypeError):
        return False
    return True


def validate_record(fields):
    """Return the reason a record is invalid, or None if it's valid."""
    if len(fields) != 4:
        return f"expected 4 fields, got {len(fields)}"
    if fields[0] == "":
        return "empty order_id"
    if fields[1] == "":
        return "empty product"
    # reject policy: quantity must be a whole number above 0
    if not fields[2].isdigit() or int(fields[2]) <= 0:
        return "quantity is not a whole number or is <= 0"
    if not is_number(fields[3]):
        return "price is not a number"
    return None