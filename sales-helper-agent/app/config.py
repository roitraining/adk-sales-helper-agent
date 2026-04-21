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

# Region used for Vertex AI calls.
LOCATION: str = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-east4")

# ---------------------------------------------------------------------------
# GCS buckets
# ---------------------------------------------------------------------------
# Bucket for generated sales assets (HTML presentations).
ASSETS_BUCKET_NAME: str = os.environ.get("ASSETS_BUCKET_NAME", "tmp-adk-test-assets")

# Bucket for agent run logs and ADK artifacts.
LOGS_BUCKET_NAME: str = os.environ.get("LOGS_BUCKET_NAME", "tmp-adk-test-logs")

# ---------------------------------------------------------------------------
# Model names
# ---------------------------------------------------------------------------
# Full-quality model — reserved for production quality generation.
PRO_MODEL_NAME: str = os.environ.get("PRO_MODEL_NAME", "gemini-3.1-pro-preview")

# Fast, cost-effective model — used for agents that do not require full-quality generation.
FAST_MODEL_NAME: str = os.environ.get("FAST_MODEL_NAME", "gemini-3.1-flash-preview")

# Lightweight, minimal context model — used in development/testing to reduce latency and cost.
LITE_MODEL_NAME: str = os.environ.get("LITE_MODEL_NAME", "gemini-3.1-flash-lite-preview")

# Single model selector used by all agents (override with CURRENT_MODEL env var).
DEFAULT_MODEL: str = os.environ.get("CURRENT_MODEL", LITE_MODEL_NAME)



