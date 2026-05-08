# scoring/ci_score.py
# Takes a listing title → returns a CI score (0-100) and a grade (A/B/C/D)
# v0.1: keyword matching only. No ML, no image analysis yet.

KEYWORDS = {
    # Positive signals
    "sealed":           25,
    "brand new":        22,
    "like new":         20,
    "mint":             18,
    "excellent":        15,
    "tested working":   12,
    "fully functional": 12,
    "works perfectly":  12,
    "all accessories":  8,
    "original box":     8,
    "good condition":   8,
    "great condition":  8,

    # Negative signals
    "for parts":       -30,
    "not working":     -28,
    "broken":          -25,
    "faulty":          -22,
    "cracked":         -20,
    "damaged":         -18,
    "spares":          -18,
    "repair":          -15,
    "scratches":       -10,
    "worn":            -8,
    "missing":         -8,
}

GRADE_BOUNDARIES = [
    (80, "A"),
    (60, "B"),
    (40, "C"),
    (0,  "D"),
]

BASE_SCORE = 50  # every listing starts here


def get_grade(score: int) -> str:
    for threshold, grade in GRADE_BOUNDARIES:
        if score >= threshold:
            return grade
    return "D"


def score_title(title: str) -> dict:
    """
    Takes a listing title string.
    Returns a dict with: score, grade, matched keywords.
    """
    title_lower = title.lower()
    adjustments = []

    for keyword, points in KEYWORDS.items():
        if keyword in title_lower:
            adjustments.append((keyword, points))

    total_adjustment = sum(points for _, points in adjustments)
    raw_score = BASE_SCORE + total_adjustment
    score = max(0, min(100, raw_score))  # clamp between 0 and 100

    return {
        "score": score,
        "grade": get_grade(score),
        "matched": adjustments,
    }