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
    }
