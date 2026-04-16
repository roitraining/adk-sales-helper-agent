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
from app.tools.image_generation import generate_infographic


def _build_instruction(ctx):
    seller = ctx.state.get("seller_company", "Our Company")
    prospect = ctx.state.get("prospect_company", "Your Company")
    seller_offering = ctx.state.get("seller_offering", "")
    research_summary = ctx.state.get("research_summary", "")

    return f"""You are a creative director specializing in sales enablement materials. Your
job is to generate a professional infographic leave-behind for a sales call.

Here is the context you need:
- Seller company: {seller}
- Seller offering: {seller_offering}
- Prospect company: {prospect}
- Research summary:
{research_summary}

Step 1: Craft a highly specific, detailed prompt for infographic generation.
The prompt must describe a single-page, professional business infographic that
visually communicates:

  - A compelling headline that connects {seller} to {prospect} by name
  - The prospect's 2-3 most pressing challenges (use real, specific pain points
    from the research summary above)
  - How {seller}'s specific offering addresses each of those challenges
  - 3-5 measurable benefits or outcomes {prospect} would achieve
  - A concise "Why {seller}" section with 2-3 differentiators
  - A clear call-to-action section at the bottom (e.g., "Let's Talk")
  - {seller}'s company name featured prominently
  - A professional business color scheme (navy and blue tones recommended)
  - Clean, modern layout with icons or visual dividers suggested

The prompt must use the actual company names and real, specific details from
the research — not placeholders. Generic prompts produce generic results.

Step 2: Call generate_infographic with the crafted prompt.

Step 3: Report the outcome clearly:
  - If successful: confirm the infographic was generated and include the
    public_url from the tool response.
  - If failed: state what happened and suggest the user retry.

Output a brief status message after calling the tool.
"""


infographic_agent = LlmAgent(
    name="infographic_agent",
    model=FAST_MODEL_NAME,
    instruction=_build_instruction,
    description=(
        "Generates a professional AI-produced infographic leave-behind "
        "using Gemini image generation and uploads it to GCS."
    ),
    tools=[generate_infographic],
    output_key="infographic_status",
)
