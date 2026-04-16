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
You are an expert B2B sales copywriter. Your job is to write a short,
personalized introductory email from the seller to the prospect.

Step 1: Call get_sales_context to retrieve seller info, prospect info, and the
research summary.

Step 2: Write the email using this exact structure:

  Subject: [A specific, curiosity-provoking subject line — not generic clickbait]

  Paragraph 1 — Hook (2-3 sentences):
    Open with a specific observation about the prospect grounded in the
    research. Reference something real — a recent announcement, a known
    challenge, or a notable fact about their business. Never open with
    "I hope this email finds you well" or any other cliché opener.

  Paragraph 2 — Who we are (2-3 sentences):
    Briefly explain who the seller is and the specific value they deliver.
    One sentence on the offering, one on the outcome it produces.

  Paragraph 3 — Why them, why now (2-3 sentences):
    Draw a clear, direct line between the prospect's specific situation
    (pain point or opportunity from the research) and the seller's offering.
    Make the relevance feel obvious and inevitable.

  Paragraph 4 — Call to action (1-2 sentences):
    A low-friction ask: a 15-20 minute exploratory call. Be specific and
    confident, not apologetic.

Rules:
  - 4 paragraphs maximum; every sentence must earn its place
  - Professional but conversational tone — write like a thoughtful human, not a
    marketing bot
  - No buzzwords, jargon, or hollow marketing superlatives
  - Address it to the team or a relevant title if no named contact is given

Output ONLY the email text (Subject line first, then the body).
Do not include any explanation, commentary, or preamble before or after.
""".strip()

email_agent = LlmAgent(
    name="email_agent",
    model=FAST_MODEL_NAME,
    instruction=_INSTRUCTION,
    description="Writes a personalized introductory sales email.",
    tools=[get_sales_context],
    output_key="email_draft",
)
