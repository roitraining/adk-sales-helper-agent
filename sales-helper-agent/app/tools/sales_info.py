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
