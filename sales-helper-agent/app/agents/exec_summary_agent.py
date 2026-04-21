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

from app.config import DEFAULT_MODEL
from app.tools.gcs_upload import upload_exec_summary_to_gcs


def _build_instruction(ctx):
    seller = ctx.state.get("seller_company", "Our Company")
    prospect = ctx.state.get("prospect_company", "Your Company")
    seller_description = ctx.state.get("seller_description", "")
    seller_offering = ctx.state.get("seller_offering", "")
    research_summary = ctx.state.get("research_summary", "")

    return f"""
You are an expert business writer and B2B sales strategist specializing in
C-suite communications.

Create a polished, single-page executive summary HTML document — a leave-behind
intended for a prospect's executive team after an initial meeting. It must be
visually refined, data-aware, and tied to the prospect's real strategic context.

Context:
- Seller company: {seller}
- Seller description: {seller_description}
- Seller offering: {seller_offering}
- Prospect company: {prospect}
- Research summary:
{research_summary}

Document structure (all on one scrollable page, no slide navigation):

  1. Header — "{seller} × {prospect}" headline, seller tagline, date
  2. The Business Opportunity — 2-3 sentences connecting {prospect}'s current
     strategic priorities (from the research) to a measurable gap or risk that
     {seller} addresses. Reference specific initiatives, market dynamics, or
     financial pressures found in the research.
  3. Strategic Alignment — a 2-column layout:
     Left: "{prospect}'s Priorities" — 3-4 bullet points drawn from their
       known strategic goals, financial outlook, or market position
     Right: "How {seller} Helps" — matching bullets showing direct relevance
       of the offering to each priority on the left
  4. Recommended Next Step — one short paragraph proposing a concrete,
     low-friction action (e.g., a focused working session or proof-of-concept)
     with a clear rationale tied to the prospect's context
  5. Footer — {seller} contact line and a subtle "Confidential — prepared for
     {prospect}" note

HTML/CSS Requirements:
  - Completely self-contained — zero external dependencies
  - Single scrollable page (no slides, no navigation buttons)
  - A4-proportioned content area (max-width ~800px, centered)
  - Clean, boardroom-appropriate typography: dark headings, generous whitespace
  - Light background with a subtle accent color that matches {prospect}'s
    branding (use your best judgment if their colors are unknown)
  - Print-friendly: the page should look good if printed or saved as PDF
  - No images — text and layout only

Step 1: Generate the complete HTML document.
Step 2: Call upload_exec_summary_to_gcs with the generated HTML passed as html_content.
Step 3: Return one sentence only:
  - Success: "Executive summary uploaded: <public_url>"
  - Error: "Upload failed: <message>"
"""


exec_summary_agent = LlmAgent(
    name="exec_summary_agent",
  model=DEFAULT_MODEL,
    instruction=_build_instruction,
    description=(
        "Generates a single-page executive summary HTML document linking "
        "the seller's offering to the prospect's strategic goals, financial "
        "context, and market dynamics, then uploads it to GCS."
    ),
    tools=[upload_exec_summary_to_gcs],
    output_key="exec_summary_result",
)
