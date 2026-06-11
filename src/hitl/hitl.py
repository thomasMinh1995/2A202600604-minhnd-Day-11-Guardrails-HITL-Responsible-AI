"""
Lab 11 — Part 4: Human-in-the-Loop Design
  TODO 12: Confidence Router
  TODO 13: Design 3 HITL decision points
"""


# ============================================================
# TODO 12: Implement ConfidenceRouter
#
# Route responses based on confidence score and action type.
# ============================================================

HIGH_RISK_ACTIONS = [
    "transfer_money",
    "delete_account",
    "send_email",
    "change_password",
    "update_personal_info",
]


class ConfidenceRouter:
    """Route agent responses based on confidence and risk level."""

    def __init__(self, high_threshold=0.9, low_threshold=0.7):
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.routing_log = []

    def route(self, response: str, confidence: float, action_type: str = "general") -> dict:
        """Route response to the correct HITL path."""
        if action_type in HIGH_RISK_ACTIONS:
            result = {
                "action": "escalate",
                "hitl_model": "Human-as-tiebreaker",
                "reason": f"High-risk action: {action_type}",
                "confidence": confidence,
                "action_type": action_type,
            }
            self.routing_log.append(result)
            return result

        if confidence >= self.high_threshold:
            result = {
                "action": "auto_send",
                "hitl_model": "Human-on-the-loop",
                "reason": "High confidence",
                "confidence": confidence,
                "action_type": action_type,
            }
            self.routing_log.append(result)
            return result

        if confidence >= self.low_threshold:
            result = {
                "action": "queue_review",
                "hitl_model": "Human-in-the-loop",
                "reason": "Medium confidence - needs review",
                "confidence": confidence,
                "action_type": action_type,
            }
            self.routing_log.append(result)
            return result

        result = {
            "action": "escalate",
            "hitl_model": "Human-as-tiebreaker",
            "reason": "Low confidence - escalating",
            "confidence": confidence,
            "action_type": action_type,
        }
        self.routing_log.append(result)
        return result


# ============================================================
# TODO 13: Design 3 HITL decision points
# ============================================================

hitl_decision_points = [
    {
        "id": 1,
        "scenario": "Customer requests a large transfer to a new beneficiary.",
        "trigger": "Transfer amount exceeds 50,000,000 VND or recipient has never been used before.",
        "hitl_model": "Human-in-the-loop",
        "context_for_human": "Transfer amount, recipient details, balance, prior transfer history, fraud alerts, and MFA status.",
        "expected_response_time": "< 5 minutes",
    },
    {
        "id": 2,
        "scenario": "Customer requests account recovery with inconsistent identity signals.",
        "trigger": "Password reset or profile update request after failed verification, new device, or unusual location.",
        "hitl_model": "Human-as-tiebreaker",
        "context_for_human": "KYC data, recent login attempts, device and location mismatch, locked-account events, and the full transcript.",
        "expected_response_time": "< 10 minutes",
    },
    {
        "id": 3,
        "scenario": "Agent gives low-confidence advice on disputes, fees, or loan obligations.",
        "trigger": "Confidence below 0.8 for policy-heavy answers that may affect customer rights or charges.",
        "hitl_model": "Human-on-the-loop",
        "context_for_human": "Draft response, confidence score, relevant policy excerpts, customer account status, and case history.",
        "expected_response_time": "< 30 minutes",
    },
]


# ============================================================
# Quick tests
# ============================================================

def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Interest rate is 5.5%", 0.95, "general"),
        ("I'll transfer 10M VND", 0.85, "transfer_money"),
        ("Rate is probably around 4-6%", 0.75, "general"),
        ("I'm not sure about this info", 0.5, "general"),
    ]

    print("Testing ConfidenceRouter:")
    print(f"{'Response':<35} {'Conf':<6} {'Action Type':<18} {'Route':<15} {'HITL Model'}")
    print("-" * 100)
    for resp, conf, action in test_cases:
        result = router.route(resp, conf, action)
        print(f"{resp:<35} {conf:<6.2f} {action:<18} {result['action']:<15} {result['hitl_model']}")


def test_hitl_points():
    """Display HITL decision points."""
    print("HITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n--- Decision Point #{point['id']} ---")
        print(f"  scenario: {point['scenario']}")
        print(f"  trigger: {point['trigger']}")
        print(f"  hitl_model: {point['hitl_model']}")
        print(f"  context_for_human: {point['context_for_human']}")
        print(f"  expected_response_time: {point['expected_response_time']}")


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
