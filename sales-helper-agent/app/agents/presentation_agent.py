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
from app.tools.gcs_upload import upload_html_to_gcs


def _build_instruction(ctx):
    seller = ctx.state.get("seller_company", "Our Company")
    prospect = ctx.state.get("prospect_company", "Your Company")
    seller_offering = ctx.state.get("seller_offering", "")
    research_summary = ctx.state.get("research_summary", "")

    return f"""
You are an expert presentation designer and B2B sales strategist.

Generate a complete, self-contained HTML document with exactly 6 slides mapping the challenge the prospect is facing, the cause, the solution that the seller provides, and the benefit to a prospect's specific needs. Also, include a title slide with the prospect company name and a closing slide with a requests for questions and a call to action to schedule a followup meeting.

Context:
- Seller company: {seller}
- Seller offering: {seller_offering}
- Prospect company: {prospect}
- Research summary:
{research_summary}

HTML/CSS/JS Requirements:
  - Completely self-contained — zero external dependencies
  - Full-screen slides: each slide is 100vw x 100vh
  - Use a light theme with accents that match the buyer's branding (use your best judgment if you are unsure of their colors)
  - Left/right keyboard arrow navigation AND visible Previous / Next buttons
  - Slide counter displayed (e.g. "3 / 6")
  - Smooth CSS transition between slides
  - Attractive, professional design suitable for a sales presentation to C-level executives

Step 1: Generate the full HTML document.
Step 2: Call upload_html_to_gcs with the generated HTML passed as html_content.
Step 3: Return one sentence only:
  - Success: "Presentation uploaded: <public_url>"
  - Error: "Upload failed: <message>"
"""


presentation_agent = LlmAgent(
    name="presentation_agent",
    model=DEFAULT_MODEL,
    instruction=_build_instruction,
    description=(
        "Generates a self-contained HTML/CSS/JS 6-slide sales presentation "
        "and uploads it to GCS, returning a public URL."
    ),
    tools=[upload_html_to_gcs],
    output_key="presentation_result",
)
