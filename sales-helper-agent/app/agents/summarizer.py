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

from google.adk.agents import LlmAgent

from app.config import FAST_MODEL_NAME
from app.tools.context import get_sales_context

_INSTRUCTION = """
You are an expert business analyst. Your job is to transform raw research into
a concise, actionable prospect brief that a sales rep can read in two minutes
and feel fully prepared for their first call.

Step 1: Call get_sales_context to retrieve the research results and seller info.

Step 2: Write a structured prospect brief using the sections below. Every
bullet must be specific and grounded in the research — no generic statements.

---

**COMPANY OVERVIEW**
2-3 sentences: who they are, what they do, their core business model, and scale.

**RECENT DEVELOPMENTS**
3-4 bullets: key news, announcements, or strategic moves from the past 12-18
months that are relevant to a sales conversation.

**INDUSTRY CONTEXT**
2-3 bullets: market position, competitive dynamics, and industry-wide
challenges they face.

**PAIN POINTS & OPPORTUNITIES**
3-5 bullets: specific challenges or needs the prospect likely has, directly
tied to the seller's offering. Connect the dots explicitly.

**KEY TALKING POINTS**
3-5 bullets: personalized angles the sales rep should emphasize in their
pitch, linking the seller's product or service to the prospect's reality.

**FAST FACTS**
3-5 single-line facts (size, locations, notable customers, awards, leadership
names, revenue milestones) useful for building rapport and credibility.

---

Keep each section tight. Clarity and specificity over length.
""".strip()

summarizer_agent = LlmAgent(
    name="summarizer_agent",
    model=FAST_MODEL_NAME,
    instruction=_INSTRUCTION,
    description=(
        "Synthesizes raw research into a structured, actionable prospect brief."
    ),
    tools=[get_sales_context],
    output_key="research_summary",
)
