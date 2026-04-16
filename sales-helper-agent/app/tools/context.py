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


def get_sales_context(tool_context: ToolContext) -> dict:
    """Retrieves all sales context data from session state.

    Returns seller info, prospect info, research results, and all
    generated asset content stored by previous pipeline agents.

    Returns:
        A dict containing all available session state values for the
        sales pipeline.
    """
    return {
        "seller_company": tool_context.state.get("seller_company", ""),
        "seller_description": tool_context.state.get("seller_description", ""),
        "seller_offering": tool_context.state.get("seller_offering", ""),
        "prospect_company": tool_context.state.get("prospect_company", ""),
        "prospect_website": tool_context.state.get("prospect_website", ""),
        "research_results": tool_context.state.get("research_results", ""),
        "research_summary": tool_context.state.get("research_summary", ""),
        "email_draft": tool_context.state.get("email_draft", ""),
        "presentation_result": tool_context.state.get("presentation_result", ""),
        "presentation_url": tool_context.state.get("presentation_url", ""),
        "presentation_gcs_path": tool_context.state.get("presentation_gcs_path", ""),
        "infographic_artifact_key": tool_context.state.get(
            "infographic_artifact_key", ""
        ),
        "infographic_status": tool_context.state.get("infographic_status", ""),
        "infographic_url": tool_context.state.get("infographic_url", ""),
        "infographic_gcs_path": tool_context.state.get("infographic_gcs_path", ""),
    }
