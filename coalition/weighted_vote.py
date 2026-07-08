class WeightedVote:

    def __init__(self, trust_manager):

        self.trust_manager = trust_manager

    def decide(self, agent_results):

        attack_score = 0.0
        benign_score = 0.0

        attack_coalition = []
        benign_coalition = []

        detailed_results = []

        for result in agent_results:

            agent_name = result["agent"]

            vote = result["vote"]

            confidence = float(
                result.get(
                    "confidence",
                    0.0
                )
            )

            trust = self.trust_manager.get_trust(
                agent_name
            )

            weight = (
                confidence
                *
                trust
            )

            detailed_results.append(
                {
                    "agent": agent_name,
                    "vote": vote,
                    "confidence": confidence,
                    "trust": round(
                        trust,
                        4
                    ),
                    "weight": round(
                        weight,
                        4
                    )
                }
            )

            if vote == "attack":

                attack_score += weight

                attack_coalition.append(
                    agent_name
                )

            else:

                benign_score += weight

                benign_coalition.append(
                    agent_name
                )

        
        

        if attack_score > benign_score:

            verdict = "attack"

        else:

            verdict = "benign"


       
        total_score = (
            attack_score +
            benign_score
        )

        if total_score == 0:

            severity = 0

            consensus = "low"

        else:

            severity = round(
                10 *
                attack_score /
                total_score
            )

        
            consensus_strength = (
                abs(
                    attack_score -
                    benign_score
                )
                /
                total_score
            )

            if consensus_strength >= 0.70:

                consensus = "high"

            elif consensus_strength >= 0.40:

                consensus = "medium"

            else:

                consensus = "low"

        return {

    "verdict": verdict,

    "severity": severity,

    "consensus": consensus,

    "attack_score": round(
        attack_score,
        4
    ),

    "benign_score": round(
        benign_score,
        4
    ),

    "attack_coalition":
        attack_coalition,

    "benign_coalition":
        benign_coalition,

    "agent_details":
        detailed_results
} 