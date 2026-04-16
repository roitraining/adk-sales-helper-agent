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

"""Centralised configuration loaded from environment variables.

All runtime settings are read here once and imported by the rest of the
application.  Set overrides in a .env file or via the shell before running.
"""

import os

# ---------------------------------------------------------------------------
# Google Cloud project
# ---------------------------------------------------------------------------

# GCP project that owns the Vertex AI and GCS resources.
PROJECT_ID: str = os.environ.get("GOOGLE_CLOUD_PROJECT", "")

# Region used for Vertex AI calls (image generation requires a concrete region,
# not "global").
LOCATION: str = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-east4")
# Image generation models do not support "global" — fall back to us-east4.
IMAGE_LOCATION: str = LOCATION if LOCATION != "global" else "us-east4"

# ---------------------------------------------------------------------------
# GCS buckets
# ---------------------------------------------------------------------------

# Bucket for generated sales assets (HTML presentations, infographic PNGs).
ASSETS_BUCKET_NAME: str = os.environ.get("ASSETS_BUCKET_NAME", "tmp-adk-test-assets")

# Bucket for agent run logs and ADK artifacts.
LOGS_BUCKET_NAME: str = os.environ.get("LOGS_BUCKET_NAME", "tmp-adk-test-logs")

# ---------------------------------------------------------------------------
# Model names
# ---------------------------------------------------------------------------

# Full-quality model — reserved for production quality generation.
PRO_MODEL_NAME: str = os.environ.get("PRO_MODEL_NAME", "gemini-2.5-pro")

# Fast, cost-effective model — used for all agents during development/testing.
FAST_MODEL_NAME: str = os.environ.get("FAST_MODEL_NAME", "gemini-2.5-flash")

# Image generation model.
IMAGE_MODEL_NAME: str = os.environ.get(
    "IMAGE_MODEL_NAME", "gemini-2.5-flash-image"
)
