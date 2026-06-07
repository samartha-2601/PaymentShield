def calculate_risk_score(amount: float) -> int:
    score = 0

    # Large transaction rule
    if amount >= 1000:
        score += 50

    # Medium transaction rule
    elif amount >= 500:
        score += 25

    return score

def determine_alert_type(score: int):

    if score >= 50:
        return (
            "Large Transaction",
            "HIGH",
            "Transaction exceeded risk threshold"
        )

    if score >= 25:
        return (
            "Medium Transaction",
            "MEDIUM",
            "Transaction requires review"
        )

    return None