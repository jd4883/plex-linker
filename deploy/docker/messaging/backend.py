"""Simple logging helper. Replaces the old status-code debug_message layer."""


def log_debug(g, msg: str, *args) -> str:
    """Format a debug line for g.LOG.debug(log_debug(g, 'message', var1, var2))."""
    parts = [str(msg)]
    for a in args:
        parts.append(str(a))
    return ": ".join(parts) if len(parts) > 1 else msg
