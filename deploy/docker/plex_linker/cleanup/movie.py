"""Strip known keys from movie dict before use."""
FIELDS_TO_CLEAN = (
    "Absolute Movie File Path", "Absolute Movie Path", "Has File", "Parsed Extension",
    "Parsed Movie Quality", "Parsed Movie Extension", "Relative Movie File Path",
    "Relative Movie Path", "Title", "Unparsed Title", "Year",
)


def cleanup_dict(dict_obj: dict) -> None:
    for k in FIELDS_TO_CLEAN:
        dict_obj.pop(k, None)
