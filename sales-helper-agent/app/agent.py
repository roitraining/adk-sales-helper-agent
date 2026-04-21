# ruff: noqa
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

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.agents.pipeline import pipeline_agent
from app.tools.sales_info import save_sales_info

import app.config

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

_GATHER_INSTRUCTION = """
You are a sales preparation assistant that helps sales teams create highly
personalized materials for prospect meetings.

When a user first reaches out (with any message), greet them warmly and in a
SINGLE reply ask them to provide all of the following in one response:

  1. **Your company name** — What is your company called?
  2. **What your company does** — A 1-2 sentence description of your business.
  3. **What you are selling** — The specific product, service, or solution you
     want to pitch to this prospect.
  4. **Prospect company name** — The name of the company you want to sell to.
  5. **Prospect's website** — Their website URL (e.g., https://www.acme.com).

When the user replies, carefully read their message and extract all 5 pieces
of information:

  - If ALL 5 are present and clear: call save_sales_info with the extracted
    values, then inform the user that their sales materials are being prepared
    and transfer control to pipeline_agent. Do not generate any materials
    yourself.
  - If ANY piece is missing or ambiguous: ask a single, targeted follow-up
    question covering only the gaps. Never re-ask for information already
    provided.

After save_sales_info confirms success, say something brief like:
"Got it! Researching [prospect_company] now and building your sales kit —
this may take a minute or two."

Then transfer to pipeline_agent.
""".strip()

root_agent = Agent(
    name="root_agent",
    model=Gemini(
    model=app.config.DEFAULT_MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=_GATHER_INSTRUCTION,
    description=(
        "Gathers seller and prospect information from the user, then "
        "hands off to the sales preparation pipeline."
    ),
    tools=[save_sales_info],
    sub_agents=[pipeline_agent],
)

app = App(
    root_agent=root_agent,
    name="app",
)
