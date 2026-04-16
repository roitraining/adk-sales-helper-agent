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

from google.adk.tools.tool_context import ToolContext


def save_sales_info(
    seller_company: str,
    seller_description: str,
    seller_offering: str,
    prospect_company: str,
    prospect_website: str,
    tool_context: ToolContext,
) -> dict:
    """Saves seller and prospect information to session state.

    Call this tool once all five pieces of information have been collected
    from the user.  The data is written to the session state so that all
    downstream pipeline agents can read it.

    Args:
        seller_company: Name of the company doing the selling.
        seller_description: Brief description of the seller's business.
        seller_offering: The specific product or service being pitched.
        prospect_company: Name of the prospect (target) company.
        prospect_website: Website URL of the prospect company.

    Returns:
        A dict with status and a confirmation message.
    """
    tool_context.state["seller_company"] = seller_company
    tool_context.state["seller_description"] = seller_description
    tool_context.state["seller_offering"] = seller_offering
    tool_context.state["prospect_company"] = prospect_company
    tool_context.state["prospect_website"] = prospect_website

    return {
        "status": "success",
        "message": (
            f"Information saved. Ready to research {prospect_company} "
            f"on behalf of {seller_company}."
        ),
    }
