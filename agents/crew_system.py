from crewai import Agent, Task, Crew
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME, DISCLAIMER

genai.configure(api_key=GEMINI_API_KEY)

# Research Agent
research_agent = Agent(
    role="Legal Research Specialist",
    goal="Analyze legal context and extract relevant legal principles.",
    backstory="Expert in Indian law and legal case analysis.",
    verbose=True
)

# Verification Agent
verification_agent = Agent(
    role="Legal Accuracy Validator",
    goal="Ensure the response strictly follows retrieved context.",
    backstory="Ensures no hallucination and checks legal consistency.",
    verbose=True
)

# Report Agent
report_agent = Agent(
    role="Legal Report Formatter",
    goal="Format the legal findings in structured format.",
    backstory="Expert legal documentation specialist.",
    verbose=True
)

def run_crew(context, query):

    task1 = Task(
        description=f"""
Using the following legal context:
{context}

Answer the legal question:
{query}

Extract relevant sections, cases, and explanation.
""",
        agent=research_agent
    )

    task2 = Task(
        description="Verify the previous answer for accuracy and ensure it only uses provided context.",
        agent=verification_agent
    )

    task3 = Task(
        description="Format the final output in structured legal format and append disclaimer.",
        agent=report_agent
    )

    crew = Crew(
        agents=[research_agent, verification_agent, report_agent],
        tasks=[task1, task2, task3],
        verbose=True
    )

    result = crew.kickoff()

    return result + "\n\n" + DISCLAIMER