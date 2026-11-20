MAX_LENGTH = 500


def summarize_error(raw: str) -> str:
    """Resume a saída (longa) do Pulumi numa mensagem curta e legível.

    Prefere as linhas que contêm "error:"; se não houver, usa as últimas linhas.
    """
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    errors = [line for line in lines if "error:" in line.lower()]
    chosen = errors or lines[-3:]
    message = " | ".join(dict.fromkeys(chosen)) or "Falha desconhecida no provisionamento"
    if len(message) > MAX_LENGTH:
        message = message[: MAX_LENGTH - 1].rstrip() + "…"
    return message
