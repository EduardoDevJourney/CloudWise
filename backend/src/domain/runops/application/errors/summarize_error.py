MAX_LENGTH = 500


def summarize_error(raw: str) -> str:
    """Boils the long Pulumi output down to a short message.

    Prefers lines containing "error:"; otherwise falls back to the last lines.
    """
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    errors = [line for line in lines if "error:" in line.lower()]
    chosen = errors or lines[-3:]
    message = " | ".join(dict.fromkeys(chosen)) or "Unknown provisioning failure"
    if len(message) > MAX_LENGTH:
        message = message[: MAX_LENGTH - 1].rstrip() + "…"
    return message
