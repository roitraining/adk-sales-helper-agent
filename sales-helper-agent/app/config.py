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

"""Centralized runtime configuration loaded from environment variables.

This file is the single source of truth for app-level configuration.

Important location split:
- AGENT_ENGINE_LOCATION controls where Vertex AI Agent Engine is deployed.
- MODEL_LOCATION controls where Gemini model calls are routed.
"""

import os

import google.auth


def _resolve_project_id() -> str:
    """Resolve GCP project ID from env first, then ADC as a fallback."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    if project_id:
        return project_id

    try:
        _, inferred_project_id = google.auth.default()
        return inferred_project_id or ""
    except Exception:
        return ""


# GCP project that owns the Vertex AI and GCS resources.
PROJECT_ID: str = _resolve_project_id()

# Agent Engine deployment region (Vertex AI infrastructure location).
AGENT_ENGINE_LOCATION: str = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-east4")

# Gemini model serving location for ADK model calls.
MODEL_LOCATION: str = os.environ.get("GOOGLE_CLOUD_MODEL_LOCATION", "global")

# Bucket for generated sales assets (presentations and executive summaries).
ASSETS_BUCKET_NAME: str = os.environ.get("ASSETS_BUCKET_NAME", "tmp-adk-test-assets")

# Bucket for Agent Engine artifacts and telemetry logs.
LOGS_BUCKET_NAME: str = os.environ.get("LOGS_BUCKET_NAME", "tmp-adk-test-logs")

# Single model selector used by all agents.
DEFAULT_MODEL: str = os.environ.get("CURRENT_MODEL", "gemini-3.1-flash-lite-preview")

# Enables Gemini-on-Vertex behavior in the SDK.
GOOGLE_GENAI_USE_VERTEXAI: str = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Telemetry-related settings used by setup_telemetry.
TELEMETRY_CAPTURE_MESSAGE_CONTENT: str = os.environ.get(
    "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "false"
)
TELEMETRY_PATH: str = os.environ.get("GENAI_TELEMETRY_PATH", "completions")
COMMIT_SHA: str = os.environ.get("COMMIT_SHA", "dev")



