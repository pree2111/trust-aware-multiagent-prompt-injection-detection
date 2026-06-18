class TrustManager:

    def __init__(self):

        self.trust = {
            "semantic": 0.5,
            "override": 0.5,
            "leakage": 0.5,
            "role_hijack": 0.5,
            "benign_validator": 0.5
        }

        self.alpha = 0.1
    def update(self, agent_name, correct):

        old = self.trust[agent_name]

        result = 1 if correct else 0

        new = (
            self.alpha * result
            +
            (1 - self.alpha) * old
        )

        self.trust[agent_name] = new