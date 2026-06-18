class MajorityVote:

    def decide(self, agent_results):

        attack_votes = sum(
            1
            for result in agent_results
            if result["vote"] == "attack"
        )

        benign_votes = sum(
            1
            for result in agent_results
            if result["vote"] == "benign"
        )

        if attack_votes > benign_votes:
            verdict = "attack"
        else:
            verdict = "benign"

        return {
            "verdict": verdict,
            "attack_votes": attack_votes,
            "benign_votes": benign_votes
        }