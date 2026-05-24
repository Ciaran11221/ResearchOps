"""
main.py
=======
CLI Entry Point — ResearchOps Multi-Agent Pipeline

This is the file the user runs. It accepts a topic as a command line argument
and passes it to the orchestrator, which coordinates the full agent pipeline.

Usage:
    python main.py "your topic here"

Example:
    python main.py "artificial intelligence in healthcare 2025"
    python main.py "the future of remote work"
    python main.py "electric vehicles market 2025"

Key concepts demonstrated:
- Clean CLI entry point using sys.argv
- Input validation with helpful error messages
- Separation of concerns: main.py only handles CLI, orchestrator handles logic
"""

import sys
from orchestrator import run_pipeline


def main():
    """
    Parse the command line argument and launch the ResearchOps pipeline.

    Validates that the user has provided a topic, then passes it to the
    orchestrator. All pipeline logic lives in orchestrator.py — this file
    is intentionally thin.
    """

    # ---------------------------------------------------------------------------
    # Input Validation
    # ---------------------------------------------------------------------------
    # sys.argv[0] is always the script name (main.py)
    # sys.argv[1] is the topic the user types after the script name
    # ---------------------------------------------------------------------------

    if len(sys.argv) < 2:
        print("\n  ResearchOps — Multi-Agent Research Pipeline")
        print("\n  Usage:   python main.py \"your topic here\"")
        print("  Example: python main.py \"artificial intelligence in healthcare 2025\"")
        print("\n  Please provide a topic and try again.\n")
        sys.exit(1)

    # Join all arguments in case the user forgot quotes
    # e.g. python main.py artificial intelligence in healthcare
    # works the same as python main.py "artificial intelligence in healthcare"
    topic = " ".join(sys.argv[1:])

    # ---------------------------------------------------------------------------
    # Launch the pipeline
    # ---------------------------------------------------------------------------

    run_pipeline(topic)


if __name__ == "__main__":
    main()