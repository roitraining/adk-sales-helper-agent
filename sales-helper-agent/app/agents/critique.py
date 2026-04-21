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
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import exit_loop

import app.config


def _build_instruction(ctx: ReadonlyContext) -> str:
    """Builds the critique instruction dynamically from session state.

    Using a callable instruction lets us embed the research_summary directly
    into the prompt, so the agent can evaluate it without any additional tool
    calls — leaving exit_loop as the sole tool, which keeps the API contract
    simple and the teaching example clear.
    """
    prospect_company = ctx.state.get("prospect_company", "the prospect company")
    seller_offering = ctx.state.get("seller_offering", "our product/service")
    research_summary = ctx.state.get("research_summary", "(no summary yet)")

    return f"""
You are a rigorous quality reviewer for sales research briefs.

Evaluate the prospect brief for **{prospect_company}** against ALL four criteria:

<brief>
{research_summary}
</brief>

EVALUATION CRITERIA:

1. **Specificity** — Does it contain real, concrete facts?
   Reject vague filler like "the company focuses on growth" or
   "they face industry challenges." Require actual names, numbers, dates,
   product names, or verifiable events.

2. **Coverage** — Does it address all required sections?
   Required: Company Overview, Recent Developments, Industry Context,
   Pain Points & Opportunities, Key Talking Points, Fast Facts.

3. **Seller Relevance** — Do the Pain Points and Talking Points explicitly
   connect to the seller's offering: "{seller_offering}"?
   Generic pain points that could apply to any vendor do not qualify.

4. **Actionability** — Could a sales rep use this brief to hold a credible,
   personalized conversation without doing any additional research?

DECISION:

- If the brief meets ALL four criteria, call the `exit_loop` tool to approve
  it, and include a brief explanation of what made the brief strong.

- If the brief fails ANY criterion, do NOT call `exit_loop`. Instead, output
  a concise critique — list exactly which criteria failed and what specific
  information is missing or too vague. Be precise so the research agent knows
  what to improve on the next iteration.
""".strip()


critique_agent = LlmAgent(
    name="critique_agent",
    model=app.config.DEFAULT_MODEL,
    instruction=_build_instruction,
    description=(
        "Reviews the research summary for quality and specificity. "
        "Calls exit_loop when the brief meets all criteria; otherwise "
        "returns a targeted critique so the loop runs another iteration."
    ),
    tools=[exit_loop],
    output_key="critique_feedback",
)
