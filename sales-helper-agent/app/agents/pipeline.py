# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import ParallelAgent, SequentialAgent

from app.agents.email_agent import email_agent
from app.agents.infographic_agent import infographic_agent
from app.agents.output_agent import output_agent
from app.agents.presentation_agent import presentation_agent
from app.agents.research import research_agent
from app.agents.summarizer import summarizer_agent

# --- Stage 3: Parallel asset generation ---
# Email, presentation, and infographic are independent and generated
# concurrently to minimize total pipeline latency.
assets_agent = ParallelAgent(
    name="assets_agent",
    sub_agents=[email_agent, presentation_agent, infographic_agent],

    description=(
        "Generates the introductory email, slide presentation, and "
        "infographic leave-behind in parallel."
    ),
)

# --- Full pipeline: research → summarize → generate assets → present ---
pipeline_agent = SequentialAgent(
    name="pipeline_agent",
    sub_agents=[
        research_agent,   # Stage 1: Research the prospect
        summarizer_agent, # Stage 2: Summarize into a prospect brief
        assets_agent,     # Stage 3: Generate all sales assets in parallel
        output_agent,     # Stage 4: Assemble and deliver to the user
    ],
    description=(
        "Runs the full sales preparation pipeline: research the prospect, "
        "summarize findings, generate assets, and deliver results."
    ),
)
