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


def _build_instruction(ctx):
    seller = ctx.state.get("seller_company", "")
    prospect = ctx.state.get("prospect_company", "")
    email_draft = ctx.state.get("email_draft", "*(email not generated)*")
    research_summary = ctx.state.get("research_summary", "*(not available)*")
    presentation_url = ctx.state.get("presentation_url", "")
    infographic_url = ctx.state.get("infographic_url", "")

    presentation_section = (
        f"👉 **[Open Presentation]({presentation_url})**\n\n"
        "*(Click the link above to open the deck in your browser — no downloads needed.)*"
        if presentation_url
        else "*(Presentation could not be uploaded — check ASSETS_BUCKET_NAME configuration.)*"
    )

    infographic_section = (
        f"![Infographic]({infographic_url})\n\n"
        f"👉 **[Download Infographic]({infographic_url})**"
        if infographic_url
        else "*(Infographic could not be generated — check IMAGE_MODEL_NAME configuration.)*"
    )

    return f"""You are a professional sales preparation assistant. Your only job is to
output the sales materials report below — exactly as written, with no additions,
changes, or commentary.

Output this exact markdown document:

---

# Sales Preparation Complete

**Seller:** {seller} | **Prospect:** {prospect}

---

## Email Draft

Ready to send — personalize the recipient name before hitting send.

```
{email_draft}
```

---

## Slide Presentation

{presentation_section}

---

## Infographic Leave-Behind

{infographic_section}

---

## Research Summary

{research_summary}

---

*All materials are customized for {prospect} based on live research.
Review and personalize before use.*
"""


output_agent = LlmAgent(
    name="output_agent",
    model=FAST_MODEL_NAME,
    instruction=_build_instruction,
    description=(
        "Assembles and presents all generated sales materials to the user "
        "in a clean, structured format."
    ),
)
