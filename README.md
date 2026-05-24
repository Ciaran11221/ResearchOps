# ResearchOps — Multi-Agent AI Research Pipeline

A local desktop application that uses a team of four specialist AI agents to autonomously research any topic and produce a structured markdown report.

Built directly on the **Anthropic API** (no LangChain or agent frameworks) to demonstrate orchestrator/specialist agent patterns, tool use, and context window management — the core skills required for agentic workflow engineering roles.

---

## Demo

> Enter a topic → four agents research, analyse, critique, and write → markdown report saved to disk

```
ResearchOps Pipeline Starting
Topic: The future of remote work

[Orchestrator] Stage 1 of 4 — Researcher Agent
[Researcher] Starting research on: The future of remote work
[Researcher] Searching: future of remote work trends 2025
[Researcher] Searching: remote work statistics 2025
[Researcher] Searching: remote work challenges and benefits
[Researcher] Research complete.

[Orchestrator] Stage 2 of 4 — Analyst Agent
[Analyst] Analysing research on: The future of remote work
[Analyst] Analysis complete.

[Orchestrator] Stage 3 of 4 — Critic Agent
[Critic] Critiquing analysis on: The future of remote work
[Critic] Critique complete.

[Orchestrator] Stage 4 of 4 — Writer Agent
[Writer] Writing final report on: The future of remote work
[Writer] Report saved to: output/the_future_of_remote_work_20250524.md

ResearchOps Pipeline Complete
```

---

## Architecture

```
main.py / gui.py
      │
      ▼
orchestrator.py          ← coordinates agents in sequence
      │
      ├── agents/researcher.py   ← gathers facts via web search tool
      ├── agents/analyst.py      ← identifies 3–5 key insights
      ├── agents/critic.py       ← challenges the analysis, finds gaps
      └── agents/writer.py       ← writes structured markdown report
```

Each specialist agent has its own system prompt and a single responsibility. The orchestrator passes the output of each agent as context to the next, building a progressively richer understanding before the final report is written.

---

## Key Concepts Demonstrated

| Concept | Where |
|---|---|
| Orchestrator / specialist agent pattern | `orchestrator.py` |
| Tool use with the Anthropic API | `agents/researcher.py` |
| Agent loop (`tool_use` → `tool_result` → `end_turn`) | `agents/researcher.py` |
| Context passing between agents | `orchestrator.py` |
| System prompt engineering | All agent files |
| Local API key management | `gui.py`, `config.json` |
| Mock mode for cost-free development | All agent files |

---

## Tech Stack

- **Python 3.10+**
- **Anthropic Python SDK** — raw API, no agent frameworks
- **Model** — `claude-opus-4-5`
- **Tool** — `web_search_20250305` (Claude's built-in web search)
- **GUI** — `tkinter` (Python built-in, no extra install)
- **Local config** — `config.json` (API key stored on user's machine only)

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- An Anthropic API key — get one free at [console.anthropic.com](https://console.anthropic.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/researchops.git
cd researchops

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run the GUI

```bash
python gui.py
```

On first launch you will be prompted to enter your Anthropic API key. It is stored locally in `config.json` and never shared.

### Run from the CLI

```bash
python main.py "the future of remote work"
```

### Mock Mode

All agents support **Mock Mode** — instant, free responses with no API calls. Toggle it in the GUI or set `MOCK_MODE = True` at the top of any agent file. Use this during development to test pipeline structure without spending credits.

---

## Project Structure

```
researchops/
├── main.py              # CLI entry point
├── gui.py               # Desktop GUI (tkinter)
├── orchestrator.py      # Coordinates agents in sequence
├── agents/
│   ├── researcher.py    # Gathers facts via web search
│   ├── analyst.py       # Identifies key insights
│   ├── critic.py        # Challenges the analysis
│   └── writer.py        # Writes the final report
├── tools/
│   └── search.py        # Web search tool definition
├── output/              # Generated reports saved here
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Roadmap

- [ ] PyInstaller `.exe` for one-click Windows install
- [ ] Parallel agent execution for faster pipelines
- [ ] Report history viewer in the GUI
- [ ] Export to PDF and Word
- [ ] Custom agent system prompt editor

---

## Author

**Ciaran Brennan** — Galway, Ireland
Building agentic AI systems on the Anthropic API.

[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

## License

MIT — see [LICENSE](LICENSE)