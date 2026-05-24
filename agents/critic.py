"""
agents/critic.py
================
Critic Agent — ResearchOps Multi-Agent Pipeline

The third specialist in the pipeline. It receives the Analyst's insights
and challenges them — finding weaknesses, gaps, counterarguments, and
assumptions that have not been examined.

Key concepts demonstrated:
- Adversarial agent pattern: one agent's job is to challenge another's output
- This improves final report quality by stress-testing the analysis
- Mock mode for cost-free development and testing
"""

from dotenv import load_dotenv
load_dotenv()

import anthropic

# Initialise the Anthropic client. API key is picked up automatically
# from the ANTHROPIC_API_KEY environment variable set in .env
client = anthropic.Anthropic()

# ---------------------------------------------------------------------------
# Mock Mode
# ---------------------------------------------------------------------------
# Set MOCK_MODE = True during development to avoid API costs.
#
# HOW TO SWITCH:
#   Development  → MOCK_MODE = True   (free, instant, no API calls)
#   Real testing → MOCK_MODE = False  (uses API credits, real critique)
# ---------------------------------------------------------------------------

MOCK_MODE = True

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

CRITIC_SYSTEM_PROMPT = """You are a sharp, sceptical research critic. You receive 
an analysis and your job is to challenge it rigorously.

Your job is to:
1. Identify 2-3 weaknesses or gaps in the analysis
2. Find assumptions that have not been examined or justified
3. Raise counterarguments that contradict the key insights
4. Highlight what important angles have been missed entirely

Be direct and specific. Do not be contrarian for its own sake — only raise 
genuine, substantive challenges that would improve the final report."""


def run_critic(topic: str, analysis: str) -> str:
    """
    Run the Critic Agent on the analyst's output.

    Receives the structured analysis from the Analyst Agent and stress-tests
    it by identifying weaknesses, gaps, and counterarguments.

    This adversarial step improves the quality and balance of the final report.
    The critique output is passed forward to the Writer Agent.

    Args:
        topic (str): The original research topic from the CLI.
        analysis (str): The full text output from the Analyst Agent.

    Returns:
        str: A structured critique identifying gaps and counterarguments.
    """

    print(f"\n[Critic] Critiquing analysis on: {topic}")

    # ---------------------------------------------------------------------------
    # Mock Mode — returns fake critique, no API call made
    # ---------------------------------------------------------------------------

    if MOCK_MODE:
        print("[Critic] MOCK MODE active — returning fake critique (no API call)")
        return f"""
## Critique: {topic}

### Weakness 1 — The 40% Growth Statistic is Unverified
The analysis treats the 40% year-on-year growth figure as established fact,
but the source is not identified. A single industry report from a vendor with
a commercial interest in inflating adoption figures could produce this number.
The conclusion about competitive disadvantage rests entirely on this claim.

### Weakness 2 — ROI Evidence is Survivorship Bias
The 30% cost reduction statistic comes from early adopter case studies — by
definition the most motivated and well-resourced organisations. Failed
implementations are rarely published. The true average ROI across all
deployments is likely significantly lower.

### Weakness 3 — Market Concentration Framing is Speculative
The insight about consolidation risk is presented as near-certain, but the
$45 billion market projection is a forecast, not an outcome. Open-source
movements in this space are strong and may counteract consolidation pressure.

### Missed Angles
- No consideration of workforce impact and resistance to adoption
- Ethical and bias risks in automated decision-making are completely absent
- Geographic variation — adoption rates differ sharply between markets

### Overall Assessment
The analysis is directionally sound but overstates certainty. The final report
should present these insights as informed perspectives rather than conclusions.
"""

    # ---------------------------------------------------------------------------
    # Live Mode — real API call
    # ---------------------------------------------------------------------------

    print("[Critic] Live mode — contacting Claude API...")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8096,
        system=CRITIC_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nAnalysis to critique:\n{analysis}"
            }
        ]
    )

    print("[Critic] Critique complete.")
    return response.content[0].text


# ---------------------------------------------------------------------------
# Direct execution — for testing this agent in isolation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mock_analysis = """
    Key Insight 1 — Rapid Mainstream Adoption: 40% year-on-year growth.
    Key Insight 2 — Regulation Gap: frameworks lagging behind deployment.
    Key Insight 3 — ROI is proven: 30% cost reduction in early adopters.
    Key Insight 4 — Market Concentration Risk: $45 billion market incoming.
    """
    result = run_critic("artificial intelligence in healthcare 2025", mock_analysis)
    print("\n--- CRITIQUE OUTPUT ---")
    print(result)