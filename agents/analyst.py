"""
agents/analyst.py
=================
Analyst Agent — ResearchOps Multi-Agent Pipeline

The second specialist in the pipeline. It receives the raw research output
from the Researcher Agent and identifies the 3-5 most significant insights,
patterns, and trends within it.

Key concepts demonstrated:
- Specialist agent pattern: one agent, one job, one system prompt
- Context passing: receives researcher output, produces structured analysis
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
#   Real testing → MOCK_MODE = False  (uses API credits, real analysis)
# ---------------------------------------------------------------------------

MOCK_MODE = True

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

ANALYST_SYSTEM_PROMPT = """You are a senior research analyst. You receive raw research 
and identify the most important insights, patterns, and trends.

Your job is to:
1. Identify exactly 3-5 key insights from the research
2. Explain why each insight is significant
3. Spot patterns or connections between different pieces of information
4. Highlight what the data is really telling us beneath the surface

Be concise, sharp, and analytical. Avoid repeating the raw research — synthesise it."""


def run_analyst(topic: str, research: str) -> str:
    """
    Run the Analyst Agent on the researcher's output.

    Receives raw research from the Researcher Agent and produces a structured
    analysis of the most significant insights and patterns.

    This output is passed forward to the Critic Agent in the pipeline.

    Args:
        topic (str): The original research topic from the CLI.
        research (str): The full text output from the Researcher Agent.

    Returns:
        str: A structured analysis of 3-5 key insights.
    """

    print(f"\n[Analyst] Analysing research on: {topic}")

    # ---------------------------------------------------------------------------
    # Mock Mode — returns fake analysis, no API call made
    # ---------------------------------------------------------------------------

    if MOCK_MODE:
        print("[Analyst] MOCK MODE active — returning fake analysis (no API call)")
        return f"""
## Analysis: {topic}

### Key Insight 1 — Rapid Mainstream Adoption
The 40% year-on-year growth rate signals this is no longer experimental.
Organisations that delay risk being structurally disadvantaged within 2-3 years.

### Key Insight 2 — The Regulation Gap
Despite strong adoption, regulatory frameworks are lagging behind deployment.
This creates both risk (liability uncertainty) and opportunity (first-mover advantage
for compliant implementations).

### Key Insight 3 — ROI is Proven but Unevenly Distributed
The 30% cost reduction in early adopter case studies is significant, but the
67% pilot rate versus actual deployment suggests many organisations are stuck
in proof-of-concept without a clear path to scale.

### Key Insight 4 — Market Concentration Risk
A $45 billion market projection will attract consolidation. Smaller players
and open-source alternatives may be squeezed out, raising dependency risks
for organisations that have not locked in flexible contracts.

### Patterns Identified
- There is a clear gap between awareness and execution across the sector
- Regulatory uncertainty is the single biggest blocker to full deployment
- Early adopters are pulling ahead rapidly, compressing the window for others
"""

    # ---------------------------------------------------------------------------
    # Live Mode — real API call
    # ---------------------------------------------------------------------------

    print("[Analyst] Live mode — contacting Claude API...")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8096,
        system=ANALYST_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nResearch to analyse:\n{research}"
            }
        ]
    )

    print("[Analyst] Analysis complete.")
    return response.content[0].text


# ---------------------------------------------------------------------------
# Direct execution — for testing this agent in isolation
# ---------------------------------------------------------------------------
# Provides mock research input so analyst can be tested without running
# the full pipeline or incurring researcher API costs.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mock_research = """
    AI in healthcare is growing rapidly. Market size is $45 billion.
    67% of organisations are piloting solutions. Early adopters report
    30% cost reductions. Regulatory frameworks are still catching up.
    Key areas: diagnostics, drug discovery, patient monitoring.
    """
    result = run_analyst("artificial intelligence in healthcare 2025", mock_research)
    print("\n--- ANALYSIS OUTPUT ---")
    print(result)