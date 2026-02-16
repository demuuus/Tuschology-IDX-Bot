KEYWORDS = [
    "saham", "ihsg", "emiten", "idx", "bei", "bank", "bumn",
    "rupiah", "inflasi", "dividen", "buyback", "akuisisi",
    "bbca", "bbri", "bmri", "bumi", "dewa", "gtsi", "bbrm",
    "netv", "emas", "bitcoin",
    "stock", "shares", "inflation", "coal", "gold"
]

def is_relevant(title: str) -> bool:
    t = title.lower()
    return any(k in t for k in KEYWORDS)