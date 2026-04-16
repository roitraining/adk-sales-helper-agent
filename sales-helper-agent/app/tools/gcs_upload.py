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

"""Tool for uploading generated assets to Google Cloud Storage."""

import logging
import uuid

from google.adk.tools.tool_context import ToolContext
from google.cloud import storage

from app.config import ASSETS_BUCKET_NAME

logger = logging.getLogger(__name__)


def upload_html_to_gcs(tool_context: ToolContext) -> dict:
    """Uploads the generated HTML presentation from state to GCS.

    Reads the HTML from state key 'presentation_html' (written by the
    presentation generator agent) and uploads it to the assets GCS bucket.

    Returns:
        A dict with:
          - status: "success" or "error"
          - public_url: The https:// URL to the uploaded file (on success)
          - gcs_path: The gs:// URI of the uploaded object (on success)
          - message: Human-readable confirmation or error detail
    """
    if not ASSETS_BUCKET_NAME:
        return {
            "status": "error",
            "message": "ASSETS_BUCKET_NAME is not configured.",
        }

    html_content = tool_context.state.get("presentation_html", "")
    if not html_content or not html_content.strip():
        return {
            "status": "error",
            "message": "No presentation_html found in state — nothing to upload.",
        }

    filename = f"{uuid.uuid4()}.html"
    gcs_path = f"gs://{ASSETS_BUCKET_NAME}/{filename}"
    public_url = f"https://storage.googleapis.com/{ASSETS_BUCKET_NAME}/{filename}"

    try:
        client = storage.Client()
        bucket = client.bucket(ASSETS_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(html_content, content_type="text/html")
        logger.info("Uploaded presentation to %s", gcs_path)
    except Exception as exc:
        logger.error("GCS upload failed: %s", exc)
        return {
            "status": "error",
            "message": f"GCS upload failed: {exc}",
        }

    # Persist URLs in state so all downstream agents can read them.
    tool_context.state["presentation_url"] = public_url
    tool_context.state["presentation_gcs_path"] = gcs_path

    return {
        "status": "success",
        "public_url": public_url,
        "gcs_path": gcs_path,
        "message": f"Presentation uploaded successfully: {public_url}",
    }
