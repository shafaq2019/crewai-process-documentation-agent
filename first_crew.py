"""
Shafaq's First Crew — Process Documentation Team
================================================
2 agents: Process Analyst (breaks down a business process)
          + SOP Writer (turns it into a clean SOP)

Run:  python first_crew.py
Requires: pip install crewai
          GEMINI_API_KEY set as environment variable
"""

import os
from crewai import Agent, Task, Crew, LLM

# ---- LLM setup (Gemini free tier via Google AI Studio key) ----
# Key terminal mein set karna best practice hai:
#   Windows:   set GEMINI_API_KEY=your_key
#   Mac/Linux: export GEMINI_API_KEY=your_key
# Agar quota error aaye to "gemini/gemini-2.5-flash" ki jagah
# "gemini/gemini-1.5-flash" try karo.

llm = LLM(
     model="gemini/gemini-3-flash-preview",
    temperature=0.3,
)

# ---- Agent 1: Process Analyst ----
# n8n analogy: yeh tumhara pehla AI node hai, lekin role-based.
analyst = Agent(
    role="Business Process Analyst",
    goal="Break down the given business process into clear, "
         "numbered steps with inputs, outputs, and decision points.",
    backstory="You are an experienced analyst who has mapped dozens "
              "of business processes. You think in flowcharts: every "
              "step has an input, an action, an output, and you always "
              "identify decision points and failure risks.",
    llm=llm,
    verbose=True,
)

# ---- Agent 2: SOP Writer ----
writer = Agent(
    role="SOP Writer",
    goal="Convert the process breakdown into a professional SOP "
         "with measurable thresholds and clear ownership per step.",
    backstory="You write standard operating procedures that real "
              "teams actually follow. You insist on measurable "
              "criteria (timeframes, quantities, pass/fail checks) "
              "instead of vague instructions.",
    llm=llm,
    verbose=True,
)

# ---- Task 1: Analyze the process ----
analyze_task = Task(
    description=(
        "Analyze this business process: {process}. "
        "Produce a numbered step-by-step breakdown. For each step "
        "identify: input, action, output, and any decision point."
    ),
    expected_output="A numbered list of process steps with "
                    "input/action/output for each, plus decision points.",
    agent=analyst,
)

# ---- Task 2: Write the SOP (uses Task 1 output as context) ----
# n8n analogy: context=[analyze_task] == pehle node ka output
# agle node mein pass karna ({{ $json.output }} wali cheez).
sop_task = Task(
    description=(
        "Using the process breakdown, write a complete SOP document "
        "with: title, purpose, scope, step-by-step procedure with "
        "measurable thresholds, and an exceptions section."
    ),
    expected_output="A complete, professional SOP in markdown format.",
    agent=writer,
    context=[analyze_task],
)

# ---- Crew: team + task order ----
crew = Crew(
    agents=[analyst, writer],
    tasks=[analyze_task, sop_task],
    verbose=True,
)

# ---- Run it! ----
if __name__ == "__main__":
    result = crew.kickoff(inputs={
        "process": "Student admission process at a private school: "
                   "inquiry, application form, entrance test, "
                   "interview, fee payment, enrollment confirmation."
    })
    print("\n\n===== FINAL SOP =====\n")
    print(result)

    # Output ko file mein save karna ho to:
    with open("generated_sop.md", "w", encoding="utf-8") as f:
        f.write(str(result))
    print("\nSOP saved to generated_sop.md ✔")
