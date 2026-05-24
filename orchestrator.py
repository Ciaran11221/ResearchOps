"""
orchestrator.py
===============
Orchestrator — ResearchOps Multi-Agent Pipeline

The orchestrator is the brain of the pipeline. It does not do any research,
analysis, or writing itself — its sole job is to coordinate the four specialist
agents in the correct sequence, passing each agent's output as context to the next.

Pipeline sequence:
    User Topic
        → Researcher  (gathers raw facts and sources)
        → Analyst     (identifies key insights and patterns)
        → Critic      (challenges the analysis, finds gaps)
        → Writer      (synthesises everything into a final report)

Key concepts demonstrated:
- Orchestrator/specialist agent pattern
- Context passing between agents (output of each becomes input of next)
- Sequential pipeline execution with progress logging
- Clean separation between coordination logic and agent logic
"""

from agents.researcher import run_researcher
from agents.analyst import run_analyst
from agents.critic import run_critic
from agents.writer import run_writer


def run_pipeline(topic: str) -> str:
    """
    Run the full ResearchOps multi-agent pipeline on a given topic.

    Coordinates all four specialist agents in sequence. Each agent's output
    is passed as context to the next, building a progressively richer
    understanding of the topic before the final report is written.

    Args:
        topic (str): The research topic entered by the user via CLI.

    Returns:
        str: The final markdown report produced by the Writer Agent.
    """

    print("\n" + "=" * 60)
    print(f"  ResearchOps Pipeline Starting")
    print(f"  Topic: {topic}")
    print("=" * 60)

    # ---------------------------------------------------------------------------
    # Stage 1 — Researcher
    # ---------------------------------------------------------------------------
    # Gathers raw facts, background, and sources on the topic.
    # Output: a structured research summary (str)
    # ---------------------------------------------------------------------------

    print("\n[Orchestrator] Stage 1 of 4 — Researcher Agent")
    research = run_researcher(topic)

    # ---------------------------------------------------------------------------
    # Stage 2 — Analyst
    # ---------------------------------------------------------------------------
    # Receives the raw research and identifies 3-5 key insights and patterns.
    # Output: a structured analysis (str)
    # ---------------------------------------------------------------------------

    print("\n[Orchestrator] Stage 2 of 4 — Analyst Agent")
    analysis = run_analyst(topic, research)

    # ---------------------------------------------------------------------------
    # Stage 3 — Critic
    # ---------------------------------------------------------------------------
    # Receives the analysis and challenges it — finds gaps, weaknesses,
    # counterarguments, and missed angles.
    # Output: a structured critique (str)
    # ---------------------------------------------------------------------------

    print("\n[Orchestrator] Stage 3 of 4 — Critic Agent")
    critique = run_critic(topic, analysis)

    # ---------------------------------------------------------------------------
    # Stage 4 — Writer
    # ---------------------------------------------------------------------------
    # Receives all three upstream outputs and synthesises them into a polished
    # markdown report, saved to the output/ folder.
    # Output: the final report text (str), saved as a .md file
    # ---------------------------------------------------------------------------

    print("\n[Orchestrator] Stage 4 of 4 — Writer Agent")
    report = run_writer(topic, research, analysis, critique)

    # ---------------------------------------------------------------------------
    # Pipeline complete
    # ---------------------------------------------------------------------------

    print("\n" + "=" * 60)
    print("  ResearchOps Pipeline Complete")
    print("  Check the output/ folder for your report")
    print("=" * 60 + "\n")

    return report


# ---------------------------------------------------------------------------
# Direct execution — for testing the full pipeline without the CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_pipeline("artificial intelligence in healthcare 2025")