from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def is_topic_safe(topic: str) -> bool:
    prompt = f"""You are a content safety checker for a research assistant tool.
Determine if the following topic is appropriate for an AI research assistant to research and write a report on.

REJECT topics that involve: violence, sexual content, self-harm, hate speech, illegal activities, or graphic/disturbing subject matter.
ACCEPT topics that are general, educational, business, technology, science, or current-events related — even if serious (e.g. "causes of climate change" or "history of war crimes tribunals" are fine).

Topic: "{topic}"

Respond with ONLY one word: SAFE or UNSAFE"""

    response = llm.invoke([HumanMessage(content=prompt)])
    answer = response.content.strip().upper()
    return "SAFE" in answer and "UNSAFE" not in answer

# ── Agent 1: Planner ──────────────────────────────────────────
def planner_agent(topic: str) -> list[str]:
    prompt = f"""You are a research planner.
Break the following research topic into exactly 3 focused sub-questions.
Return ONLY a numbered list. No extra text.

Topic: {topic}"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    lines = response.content.strip().split("\n")
    questions = [l.split(". ", 1)[-1].strip() for l in lines if l.strip()]
    return questions[:3]


# ── Agent 2: Search ───────────────────────────────────────────
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_agent(questions: list[str]) -> list[dict]:
    results = []
    for q in questions:
        response = tavily.search(query=q, max_results=3)
        results.append({
            "question": q,
            "results": response["results"]
        })
    return results


# ── Agent 3: Analyst ──────────────────────────────────────────
def analyst_agent(search_data: list[dict]) -> list[dict]:
    analyses = []
    for item in search_data:
        question = item["question"]
        context = "\n".join([r["content"] for r in item["results"]])
        
        prompt = f"""You are a research analyst.
Based on the search results below, write a concise 3-4 sentence insight answering the question.

Question: {question}

Search Results:
{context}

Insight:"""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        analyses.append({
            "question": question,
            "insight": response.content.strip()
        })
    return analyses


# ── Agent 4: Writer ───────────────────────────────────────────
def writer_agent(topic: str, analyses: list[dict]) -> str:
    sections = "\n\n".join([
        f"**{a['question']}**\n{a['insight']}" for a in analyses
    ])
    
    prompt = f"""You are a professional research writer.
Using the insights below, write a well-structured research report on the topic.
Include: a short introduction, the key findings, and a conclusion.
Use clear headings and professional language.

Topic: {topic}

Insights:
{sections}

Report:"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()