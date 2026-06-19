# 🔍 Multi-Agent Research Assistant

An AI research assistant that breaks down a topic, searches the live web, analyzes findings, and writes a structured report — using **4 specialized AI agents** orchestrated with LangGraph, instead of a single LLM call.

**[Live Demo](https://huggingface.co/spaces/srichakra944/multi-agent-research-assistant)**

## Why this exists

Most "AI chatbot" projects are a single prompt to an LLM. This project demonstrates **multi-agent orchestration** — multiple specialized agents, each with one job, passing structured data to each other through a defined graph, with the LLM's role limited to reasoning over real data rather than generating facts from memory.

## How it works

User Topic

↓

🧠 Planner Agent   → breaks topic into 3 focused sub-questions

↓

🔎 Search Agent    → searches the live web for each question (Tavily API)

↓

📊 Analyst Agent   → extracts key insights from search results

↓

✍️ Writer Agent    → compiles insights into a structured report


A **guardrail agent** checks the topic for safety before the pipeline runs, rejecting inappropriate topics before any API calls are made.

## Key design decision: grounded, not hallucinated

The Search agent pulls **real, current web content** via the Tavily API — not the LLM's training data. The LLM's job is restricted to *reading and writing about* that real data, not inventing facts. This significantly reduces hallucination risk compared to asking an LLM to "research" a topic directly.

## Tech Stack

| Component | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq (LLaMA 3.3 70B) |
| Web search | Tavily API |
| UI | Streamlit |
| Deployment | Hugging Face Spaces |

## Features

- 4-agent pipeline with live progress UI (each agent's status updates in real time as it runs)
- Real-time web search grounding — not just LLM-generated text
- Topic safety guardrail before execution
- Expandable sections to inspect sub-questions and intermediate insights, not just the final report

## Run locally

```bash
git clone https://github.com/Chakri944/multi-agent-research-assistant
cd multi-agent-research-assistant
pip install -r requirements.txt
```

Create a `.env` file:<br>
GROQ_API_KEY=your_groq_key <br>
TAVILY_API_KEY=your_tavily_key

Run:
```bash
streamlit run app.py
```

## Project Structure
├── app.py          # Streamlit UI<br>
├── agents.py        # 4 agent functions + safety guardrail<br>
├── graph.py          # LangGraph workflow definition<br>
└── requirements.txt

## Author

**Sri Chakradhar Reddy**
[LinkedIn](https://linkedin.com/in/srichakra944) · [GitHub](https://github.com/Chakri944) · [Hugging Face](https://huggingface.co/srichakra944)
