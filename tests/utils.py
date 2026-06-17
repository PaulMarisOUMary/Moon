def clean_type(token_type: str) -> str:
    return token_type.split("__")[-1]