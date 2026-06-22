from itertools import combinations
from math import factorial


class Shapley:

    def __init__(self):

        self.agents = [
            "semantic",
            "override",
            "leakage",
            "role_hijack",
            "benign_validator"
        ]

    def powerset(self, agents):

        subsets = []

        for r in range(
            len(agents) + 1
        ):

            subsets.extend(
                combinations(
                    agents,
                    r
                )
            )

        return subsets

    def coalition_value(
        self,
        coalition,
        results_df
    ):

        if len(coalition) == 0:

            return 0.0

        correct = 0

        for _, row in results_df.iterrows():

            attack_votes = 0
            benign_votes = 0

            for agent in coalition:

                vote = row[
                    f"{agent}_vote"
                ]

                if vote == "attack":

                    attack_votes += 1

                else:

                    benign_votes += 1

            prediction = (
                "attack"
                if attack_votes >
                benign_votes
                else "benign"
            )

            if prediction == row["label"]:

                correct += 1

        return (
            correct /
            len(results_df)
        )

    def calculate(
        self,
        results_df
    ):

        n = len(
            self.agents
        )

        shapley = {
            agent: 0.0
            for agent
            in self.agents
        }

        for agent in self.agents:

            others = [
                a
                for a
                in self.agents
                if a != agent
            ]

            for coalition in self.powerset(
                others
            ):

                coalition = set(
                    coalition
                )

                coalition_with_agent = (
                    coalition |
                    {agent}
                )

                v_s = (
                    self.coalition_value(
                        coalition,
                        results_df
                    )
                )

                v_si = (
                    self.coalition_value(
                        coalition_with_agent,
                        results_df
                    )
                )

                marginal = (
                    v_si -
                    v_s
                )

                weight = (
                    factorial(
                        len(coalition)
                    )
                    *
                    factorial(
                        n -
                        len(coalition)
                        -
                        1
                    )
                    /
                    factorial(n)
                )

                shapley[
                    agent
                ] += (
                    weight *
                    marginal
                )

        return shapley