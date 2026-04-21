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
from google.adk.tools import google_search

from app.config import DEFAULT_MODEL


def _build_instruction(ctx: ReadonlyContext) -> str:
    """Builds a research instruction dynamically from session state.

    Using a callable instruction avoids needing a custom tool to read state,
    which allows google_search to be the sole tool (required by the Gemini
    API — google_search cannot be mixed with custom function tools).
    """
    prospect_company = ctx.state.get("prospect_company", "the prospect company")
    prospect_website = ctx.state.get("prospect_website", "")
    seller_company = ctx.state.get("seller_company", "our company")
    seller_offering = ctx.state.get("seller_offering", "our product/service")

    website_note = (
        f"Their website is {prospect_website}." if prospect_website else ""
    )

    critique_feedback = ctx.state.get("critique_feedback", "")
    critique_section = (
        f"\nPREVIOUS CRITIQUE — address these gaps in your research this iteration:\n"
        f"{critique_feedback}\n"
        if critique_feedback
        else ""
    )

    return f"""
You are an expert business research analyst. Your job is to thoroughly research
a prospect company so the sales team can walk into their meeting fully prepared.

CONTEXT:
  - Prospect company: {prospect_company}
  - Prospect website: {prospect_website}
  - Selling company:  {seller_company}
  - Offering:         {seller_offering}

{website_note}
{critique_section}
Conduct exactly 3 targeted Google searches:

  Search 1 — Company overview and business model:
    Query: "{prospect_company} company overview about business"

  Search 2 — Recent news and strategic initiatives:
    Query: "{prospect_company} news 2025 2026 announcement"

  Search 3 — Industry challenges and technology needs:
    Query: "{prospect_company} industry challenges technology digital transformation"

After completing all 3 searches, synthesize the findings into comprehensive
research notes. Be specific and use real facts — no generic filler.
Your notes must cover:

  - Company description, core products/services, and business model
  - Company size, scale, employee count, revenue (if available)
  - Key leadership and decision-makers (if found)
  - Recent news, strategic initiatives, and press releases
  - Industry trends, competitive landscape, and market position
  - Likely pain points and technology or operational gaps
  - Anything that connects the prospect's situation to what {seller_company}
    offers ({seller_offering})

Your research will drive the personalization of all sales materials —
specificity and accuracy are critical.
""".strip()


research_agent = LlmAgent(
    name="research_agent",
  model=DEFAULT_MODEL,
    instruction=_build_instruction,
    description=(
        "Researches the prospect company via Google Search to build a "
        "detailed company profile."
    ),
    tools=[google_search],
    output_key="research_results",
)
