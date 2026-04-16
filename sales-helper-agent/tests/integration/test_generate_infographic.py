"""Standalone integration test for generate_infographic tool.

Usage:
    uv run python tests/integration/test_generate_infographic.py

Requires ADC credentials and GOOGLE_CLOUD_PROJECT set (or defaults in config.py).
"""

import logging

logging.basicConfig(level=logging.INFO)


TEST_PROMPT = """
Create a professional single-page business infographic with a navy and blue
color scheme.

Headline: "Acme Corp × TechStartup Inc"

Section 1 — Challenges TechStartup Faces:
  - Slow manual sales outreach slowing pipeline velocity
  - Lack of personalized prospect research at scale
  - Sales reps spending 60% of time on admin instead of selling

Section 2 — How Acme Corp Helps:
  - AI-powered prospect research in under 2 minutes
  - Auto-generated personalized emails and presentations
  - Frees reps to focus on high-value conversations

Section 3 — Why Acme Corp:
  - 3x faster deal cycles reported by customers
  - Integrates with existing CRM in one click
  - SOC2 compliant, enterprise-ready

Call to Action (bottom): "Book a 20-min Discovery Call Today"

Layout: clean modern design, icons for each bullet, prominent company name
at the top, professional typography.
""".strip()


class MockToolContext:
    """Minimal stand-in for ADK ToolContext."""

    def __init__(self):
        self.state = {}


def main():
    # Import here so config is loaded after env is set
    from app.tools.image_generation import generate_infographic

    ctx = MockToolContext()
    print("Calling generate_infographic...")
    result = generate_infographic(prompt=TEST_PROMPT, tool_context=ctx)

    print("\n--- Result ---")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\n--- State written ---")
    for k, v in ctx.state.items():
        print(f"  {k}: {v}")

    if result.get("status") == "success":
        url = result.get("public_url", "")
        if url:
            print(f"\nInfographic URL: {url}")
        else:
            print("\nGenerated OK but GCS upload skipped (ASSETS_BUCKET_NAME not set?).")
    else:
        print("\nTest FAILED:", result.get("message"))


if __name__ == "__main__":
    main()
