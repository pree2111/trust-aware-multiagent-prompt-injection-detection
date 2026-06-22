import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from trust.trust_manager import TrustManager
from coalition.weighted_vote import WeightedVote

trust_manager = TrustManager()

trust_manager.trust["semantic"] = 0.8
trust_manager.trust["override"] = 0.7
trust_manager.trust["leakage"] = 0.7
trust_manager.trust["role_hijack"] = 0.5
trust_manager.trust["benign_validator"] = 0.6

voter = WeightedVote(
    trust_manager
)

agent_results = [

    {
        "agent":"semantic",
        "vote":"attack",
        "confidence":0.90
    },

    {
        "agent":"override",
        "vote":"attack",
        "confidence":0.80
    },

    {
        "agent":"leakage",
        "vote":"attack",
        "confidence":0.95
    },

    {
        "agent":"role_hijack",
        "vote":"benign",
        "confidence":0.70
    },

    {
        "agent":"benign_validator",
        "vote":"benign",
        "confidence":0.90
    }

]

result = voter.decide(
    agent_results
)

print(result)