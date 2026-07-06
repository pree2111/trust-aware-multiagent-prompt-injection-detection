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

Your ONLY task is to explain the coalition's decision.

Focus primarily on the security implications
of the prompt and the coalition decision.

Do not simply repeat confidence scores.

Explain WHY the attack is dangerous
or WHY it is benign.

When writing the explanation:

- Focus on the attack behavior.
- Focus on the security implications.
- Do not discuss confidence scores.
- Do not discuss numerical weights.
- Do not explain how weighted voting works.

Return ONLY valid JSON:

{
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


class LLMJudge:

    def __init__(self, llm):

        self.llm = llm

    def evaluate(
        self,
        prompt,
        coalition_result,
        agent_results,
        row_id
    ):

        judge_prompt = f"""
{SYSTEM_PROMPT}

Prompt:
{prompt}

Coalition Verdict:
{coalition_result["verdict"]}

Attack Score:
{coalition_result["attack_score"]}

Benign Score:
{coalition_result["benign_score"]}

Consensus Level:
{coalition_result["consensus"]}

Agent Results:
{json.dumps(agent_results, indent=2)}
"""

        response = self.llm.ask(
            prompt=judge_prompt,
            context=SYSTEM_PROMPT,
            agent="judge",
            row_id=row_id
        )

        if DEBUG:

            print("JUDGE RAW RESPONSE:")
            print(response)
            print("-" * 50)

        try:

            result = extract_json(
                response
            )

            explanation = str(
                result.get(
                    "explanation",
                    "No explanation provided."
                )
            )

            return {
                "explanation": explanation
            }

        except Exception:

            return {
                "explanation": "Judge parse failure"
            }