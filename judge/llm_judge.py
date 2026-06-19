import json
import re

DEBUG = False

SYSTEM_PROMPT = """
You are a Trust-Aware Security Judge.

A coalition of security agents has already
classified a user prompt.

The coalition verdict is FINAL.

You must accept the coalition verdict.

You are NOT allowed to determine whether
the prompt is benign or an attack.

These are your ONLY tasks:
1. Assess consensus strength

Allowed values:

- low
- medium
- high

2. Explain the coalition decision. 
Focus primarily on the security implications
of the prompt and the coalition decision.

Do not simply repeat confidence scores.

Explain WHY the attack is dangerous
or WHY it is benign.
Coalition Evidence:

Attack Weight:
{coalition_result["attack_score"]}

Benign Weight:
{coalition_result["benign_score"]}

These are weighted coalition scores,
not severity scores.

Return ONLY valid JSON:

{
  "consensus": "low|medium|high",
  "explanation": "short explanation"
}
"""


def extract_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:

        return json.loads(
            match.group()
        )

    raise ValueError(
        f"No JSON found:\n{text}"
    )


def normalize_consensus(consensus):

    consensus = str(
        consensus
    ).lower().strip()

    if consensus in [
        "low",
        "medium",
        "high"
    ]:
        return consensus

    return "medium"


class LLMJudge:

    def __init__(self, llm):

        self.llm = llm

    def evaluate(
        self,
        prompt,
        coalition_result,
        agent_results
    ):

        judge_prompt = f"""
{SYSTEM_PROMPT}

Prompt:
{prompt}

Coalition Verdict:
{coalition_result["verdict"]}

Coalition Evidence:

Attack Weight:
{coalition_result["attack_score"]}

Benign Weight:
{coalition_result["benign_score"]}

Attack Coalition:
{coalition_result["attack_coalition"]}

Benign Coalition:
{coalition_result["benign_coalition"]}

Agent Results:
{json.dumps(agent_results, indent=2)}
"""

        response = self.llm.ask(
            judge_prompt
        )

        if DEBUG:

            print("JUDGE RAW RESPONSE:")
            print(response)
            print("-" * 50)

        try:

            result = extract_json(
                response
            )

            severity = int(
                result.get(
                    "severity",
                    0
                )
            )

            severity = max(
                0,
                min(
                    severity,
                    10
                )
            )

            consensus = normalize_consensus(
                result.get(
                    "consensus",
                    "medium"
                )
            )

            explanation = str(
                result.get(
                    "explanation",
                    "No explanation provided."
                )
            )

            return {
                "severity": severity,
                "consensus": consensus,
                "explanation": explanation
            }

        except Exception:

            return {
                "severity": 0,
                "consensus": "low",
                "explanation": "Judge parse failure"
            }