def is_maintenance_page(html: str) -> bool:
    checks = [
        "maintenance",
        "under maintenance",
        "sedang pemeliharaan",
        "sementara tidak dapat diakses",
        "currently unavailable"
    ]
    h = html.lower()
    return any(k in h for k in checks) or len(html) < 20000

def escape_markdown(text: str) -> str:
    for ch in ["*", "_", "`", "[", "]"]:
        text = text.replace(ch, f"\\{ch}")
    return text