"""
agents/researcher.py
====================
Researcher Agent — ResearchOps Multi-Agent Pipeline

This is the first specialist agent in the pipeline. Its sole responsibility is
to gather raw information on a given topic using Claude's built-in web search tool.

Key concepts demonstrated:
- Built-in tool use with the Anthropic API (web_search_20250305)
- The agent loop pattern: send message → handle tool call → loop until end_turn
- Separation of concerns: each agent has one job and one system prompt
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
# The mock returns realistic fake data so you can build and test the full
# pipeline without spending credits.
#
# HOW TO SWITCH:
#   Development  → MOCK_MODE = True   (free, instant, no API calls)
#   Real testing → MOCK_MODE = False  (uses API credits, real web search)
# ---------------------------------------------------------------------------

MOCK_MODE = True

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

RESEARCHER_SYSTEM_PROMPT = """You are a research specialist with access to a web search tool.
You MUST use the web_search tool multiple times before writing your summary.
Search at least 3 times covering: overview, recent 2025 developments, and key statistics.
Do not write your final summary until you have completed all searches."""


def run_researcher(topic: str) -> str:
    """
    Run the Researcher Agent on a given topic.

    In MOCK_MODE, returns realistic fake data instantly at zero cost.
    In live mode, uses Claude's built-in web_search_20250305 tool to
    perform real web searches via the Anthropic beta API.

    Args:
        topic (str): The research topic provided by the user via CLI.

    Returns:
        str: A structured summary of research findings.
    """

    print(f"\n[Researcher] Starting research on: {topic}")

    # ---------------------------------------------------------------------------
    # Mock Mode — returns fake data, no API call made
    # ---------------------------------------------------------------------------
    # Use this during development to test pipeline structure without API costs.
    # The mock data is realistic enough to flow through analyst, critic, writer.
    # ---------------------------------------------------------------------------

    if MOCK_MODE:
        print("[Researcher] MOCK MODE active — returning fake data (no API call)")
        return f"""
## Research Summary: {topic}

### Overview
This is mock research data for development and testing purposes.
The topic '{topic}' is a rapidly evolving field with significant implications.

### Key Facts
- Fact 1: Major organisations are investing heavily in this area in 2025
- Fact 2: Recent studies show a 40% increase in adoption rates year on year
- Fact 3: Key challenges remain around regulation, ethics, and implementation

### Recent Developments (2025)
- Development A: New frameworks have been introduced by leading bodies
- Development B: Several high-profile case studies have demonstrated ROI
- Development C: Regulatory guidance is expected later this year

### Key Statistics
- Market size projected at $45 billion by end of 2025
- 67% of organisations report piloting or deploying solutions
- Cost reduction of 30% reported in early adopter case studies

### Sources
- Industry reports, academic publications, and news sources consulted
- Data reflects the current state of knowledge as of 2025
"""

    # ---------------------------------------------------------------------------
    # Live Mode — real API call with web search
    # ---------------------------------------------------------------------------
    # Only runs when MOCK_MODE = False.
    # Uses the Anthropic beta API to perform real web searches.
    # ---------------------------------------------------------------------------

    print("[Researcher] Live mode — contacting Claude API with web search...")

    response = client.beta.messages.create(
        model="claude-opus-4-5",
        max_tokens=8096,
        system=RESEARCHER_SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {
                "role": "user",
                "content": f"Search the web and research this topic thoroughly: {topic}"
            }
        ],
        betas=["web-search-2025-03-05"]
    )

    print(f"[Researcher] Response received. Stop reason: {response.stop_reason}")

    # Extract all text blocks from the response
    result = []
    for block in response.content:
        if hasattr(block, "text"):
            result.append(block.text)
        elif block.type == "tool_use":
            print(f"[Researcher] Searched: {block.input.get('query', '')}")

    print("[Researcher] Research complete.")
    return "\n".join(result)


# ---------------------------------------------------------------------------
# Direct execution — for testing this agent in isolation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    result = run_researcher("artificial intelligence in healthcare 2025")
    print("\n--- RESEARCH OUTPUT ---")
    print(result)