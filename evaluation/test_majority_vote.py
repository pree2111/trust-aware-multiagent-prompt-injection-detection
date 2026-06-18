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
from coalition.majority_vote import MajorityVote

voter = MajorityVote()

results = [
    {"vote":"attack"},
    {"vote":"attack"},
    {"vote":"attack"},
    {"vote":"benign"},
    {"vote":"benign"}
]

print(
    voter.decide(results)
)