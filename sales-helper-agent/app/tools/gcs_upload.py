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


def _upload_html_asset(
    *,
    html_content: str,
    tool_context: ToolContext,
    filename_prefix: str,
    log_label: str,
    state_prefix: str,
    success_label: str,
) -> dict:
    """Shared uploader for generated HTML assets."""
    if not ASSETS_BUCKET_NAME:
        return {
            "status": "error",
            "message": "ASSETS_BUCKET_NAME is not configured.",
        }

    if not html_content or not html_content.strip():
        return {
            "status": "error",
            "message": "No HTML content provided — nothing to upload.",
        }

    filename = f"{filename_prefix}{uuid.uuid4()}.html"
    gcs_path = f"gs://{ASSETS_BUCKET_NAME}/{filename}"
    public_url = f"https://storage.googleapis.com/{ASSETS_BUCKET_NAME}/{filename}"

    try:
        client = storage.Client()
        bucket = client.bucket(ASSETS_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(html_content, content_type="text/html")
        logger.info("Uploaded %s to %s", log_label, gcs_path)
    except Exception as exc:
        logger.error("GCS upload failed: %s", exc)
        return {
            "status": "error",
            "message": f"GCS upload failed: {exc}",
        }

    tool_context.state[f"{state_prefix}_html"] = html_content
    tool_context.state[f"{state_prefix}_url"] = public_url
    tool_context.state[f"{state_prefix}_gcs_path"] = gcs_path

    return {
        "status": "success",
        "public_url": public_url,
        "gcs_path": gcs_path,
        "message": f"{success_label} uploaded successfully: {public_url}",
    }


def upload_html_to_gcs(html_content: str, tool_context: ToolContext) -> dict:
    """Uploads generated HTML presentation content to GCS.

    The HTML is provided directly as a tool argument by the calling agent and
    then uploaded to the assets GCS bucket.

    Returns:
        A dict with:
          - status: "success" or "error"
          - public_url: The https:// URL to the uploaded file (on success)
          - gcs_path: The gs:// URI of the uploaded object (on success)
          - message: Human-readable confirmation or error detail
    """
    return _upload_html_asset(
        html_content=html_content,
        tool_context=tool_context,
        filename_prefix="",
        log_label="presentation",
        state_prefix="presentation",
        success_label="Presentation",
    )


def upload_exec_summary_to_gcs(html_content: str, tool_context: ToolContext) -> dict:
    """Uploads a generated executive summary HTML document to GCS.

    The HTML is provided directly as a tool argument by the calling agent and
    uploaded to the assets GCS bucket under a unique filename.

    Returns:
        A dict with:
          - status: "success" or "error"
          - public_url: The https:// URL to the uploaded file (on success)
          - gcs_path: The gs:// URI of the uploaded object (on success)
          - message: Human-readable confirmation or error detail
    """
    return _upload_html_asset(
        html_content=html_content,
        tool_context=tool_context,
        filename_prefix="exec-summary-",
        log_label="executive summary",
        state_prefix="exec_summary",
        success_label="Executive summary",
    )
