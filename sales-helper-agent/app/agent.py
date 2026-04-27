import os
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.agents.pipeline import pipeline_agent
from app.tools.sales_info import save_sales_info

import app.config as config

if config.PROJECT_ID:
    os.environ["GOOGLE_CLOUD_PROJECT"] = config.PROJECT_ID

# Model serving location for Gemini calls (distinct from Agent Engine region).
os.environ["GOOGLE_CLOUD_LOCATION"] = config.MODEL_LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = config.GOOGLE_GENAI_USE_VERTEXAI

_GATHER_INSTRUCTION = """
You are a sales proposal engine that helps sales teams create highly
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
      model=config.DEFAULT_MODEL,
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
