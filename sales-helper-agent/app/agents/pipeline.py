from google.adk.agents import LoopAgent, ParallelAgent, SequentialAgent

from app.agents.critique import critique_agent
from app.agents.email_agent import email_agent
from app.agents.exec_summary_agent import exec_summary_agent
from app.agents.output_agent import output_agent
from app.agents.presentation_agent import presentation_agent
from app.agents.research import research_agent
from app.agents.writer import writer_agent

# --- Stage 3: Parallel asset generation ---
# Email, presentation, and executive summary are independent and generated
# concurrently to minimize total pipeline latency.
assets_agent = ParallelAgent(
    name="assets_agent",
    sub_agents=[email_agent, presentation_agent, exec_summary_agent],
    description=(
        "Generates the introductory email, slide presentation, and "
        "executive summary leave-behind in parallel."
    ),
)

# --- Stages 1-2: Research loop (research → summarize → critique) ---
# LoopAgent reruns the sub-agents until the critique_agent approves the
# summary quality by calling exit_loop, or until max_iterations is reached.
research_loop = LoopAgent(
    name="research_loop",
    sub_agents=[research_agent, writer_agent, critique_agent],
    max_iterations=2,
    description=(
        "Iteratively researches the prospect and summarizes findings, "
        "looping until the critique agent approves the quality or the "
        "iteration limit is reached."
    ),
)

# --- Full pipeline: research loop → generate assets → present ---
pipeline_agent = SequentialAgent(
    name="pipeline_agent",
    sub_agents=[
        research_loop,  # Stages 1-2: Research + Summarize with quality loop
        assets_agent,   # Stage 3: Generate all sales assets in parallel
        output_agent,   # Stage 4: Assemble and deliver to the user
    ],
    description=(
        "Runs the full sales preparation pipeline: research the prospect, "
        "summarize findings, generate assets, and deliver results."
    ),
)
