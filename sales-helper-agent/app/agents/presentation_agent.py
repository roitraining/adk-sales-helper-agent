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

from google.adk.agents import LlmAgent, SequentialAgent

from app.config import FAST_MODEL_NAME
from app.tools.gcs_upload import upload_html_to_gcs


def _build_generator_instruction(ctx):
    seller = ctx.state.get("seller_company", "Our Company")
    prospect = ctx.state.get("prospect_company", "Your Company")
    seller_offering = ctx.state.get("seller_offering", "")
    research_summary = ctx.state.get("research_summary", "")

    return f"""You are an expert presentation designer and B2B sales strategist.

Generate a complete, self-contained HTML document with exactly 6 slides.

Context:
- Seller company: {seller}
- Seller offering: {seller_offering}
- Prospect company: {prospect}
- Research summary:
{research_summary}

Slide structure:

  Slide 1 — Title
    Headline: "{seller} x {prospect}"
    Subheadline: Seller's core value proposition in one punchy sentence
    Footer: Today's date

  Slide 2 — About {seller}
    Headline: "About {seller}"
    3-4 bullets: what they do, core strengths, key differentiators

  Slide 3 — We Understand Your World
    Headline: Something empathetic, e.g. "The Challenges You're Navigating"
    3-4 bullets: specific pain points {prospect} faces, drawn from the
    research summary above

  Slide 4 — Our Solution
    Headline: "How {seller} Helps"
    3-4 bullets: connecting the seller's offering to Slide 3 pain points

  Slide 5 — Why {seller}
    Headline: "Why Teams Choose {seller}"
    3-4 bullets: differentiators, proof points, or outcomes

  Slide 6 — Let's Talk
    Headline: "Ready to Explore?"
    Proposed next step and contact info line

HTML/CSS/JS Requirements:
  - Completely self-contained — zero external dependencies
  - Full-screen slides: each slide is 100vw x 100vh
  - Dark navy background (#0f172a) with vivid blue accent (#3b82f6) for
    headings; white body text; clean sans-serif font stack
  - Left/right keyboard arrow navigation AND visible Previous / Next buttons
  - Slide counter displayed (e.g. "3 / 6")
  - Smooth CSS transition between slides
  - Bullets: punchy 5-10 word fragments, never full sentences
  - Maximum 4 bullets per slide

Output ONLY the raw HTML document — no explanation, no markdown fences.
"""


def _build_uploader_instruction(ctx):
    return """You are an upload assistant. Call upload_html_to_gcs with no arguments.
Then report the result in one sentence:
  - Success: "Presentation uploaded: <public_url>"
  - Error: "Upload failed: <message>"
"""


_generator_agent = LlmAgent(
    name="presentation_generator",
    model=FAST_MODEL_NAME,
    instruction=_build_generator_instruction,
    description="Generates the HTML slide deck and saves it to state.",
    output_key="presentation_html",
)

_uploader_agent = LlmAgent(
    name="presentation_uploader",
    model=FAST_MODEL_NAME,
    instruction=_build_uploader_instruction,
    description="Uploads the HTML from state to GCS and records the public URL.",
    tools=[upload_html_to_gcs],
    output_key="presentation_result",
)

presentation_agent = SequentialAgent(
    name="presentation_agent",
    sub_agents=[_generator_agent, _uploader_agent],
    description=(
        "Generates a self-contained HTML/CSS/JS 6-slide sales presentation "
        "and uploads it to GCS, returning a public URL."
    ),
)
