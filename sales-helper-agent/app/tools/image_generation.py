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

import logging
import uuid

from google import genai
from google.adk.tools.tool_context import ToolContext
from google.cloud import storage
from google.genai import types

from app.config import ASSETS_BUCKET_NAME, IMAGE_LOCATION, IMAGE_MODEL_NAME, PROJECT_ID

logger = logging.getLogger(__name__)


def generate_infographic(prompt: str, tool_context: ToolContext) -> dict:
    """Generates a sales infographic image using Gemini image generation.

    Calls gemini-3.1-flash-image-preview to produce a PNG infographic based
    on the provided prompt.  The resulting image is saved as an ADK artifact
    named 'infographic.png' and the artifact key is written to session state.

    Args:
        prompt: A detailed, specific description of the infographic to generate.
            Include company names, pain points, benefits, and visual guidance.

    Returns:
        A dict with status, artifact_key (on success), and a message.
    """
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=IMAGE_LOCATION)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        response_modalities=["TEXT", "IMAGE"],
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT", threshold="OFF"
            ),
        ],
    )

    image_data = bytearray()

    try:
        for chunk in client.models.generate_content_stream(
            model=IMAGE_MODEL_NAME,
            contents=contents,
            config=config,
        ):
            if not chunk.candidates:
                continue
            for candidate in chunk.candidates:
                if not candidate.content or not candidate.content.parts:
                    continue
                for part in candidate.content.parts:
                    if (
                        hasattr(part, "inline_data")
                        and part.inline_data is not None
                    ):
                        image_data.extend(part.inline_data.data)
    except Exception as exc:
        logger.error("Infographic generation failed: %s", exc)
        return {
            "status": "error",
            "message": f"Image generation failed: {exc}",
        }

    if not image_data:
        logger.warning("Image generation returned no image bytes.")
        return {
            "status": "error",
            "message": (
                "The model did not return an image. "
                "Try again or simplify the prompt."
            ),
        }

    # Upload to GCS so output_agent can embed a public URL.
    public_url = ""
    gcs_path = ""
    if ASSETS_BUCKET_NAME:
        try:
            filename_gcs = f"infographic-{uuid.uuid4()}.png"
            gcs_path = f"gs://{ASSETS_BUCKET_NAME}/{filename_gcs}"
            public_url = f"https://storage.googleapis.com/{ASSETS_BUCKET_NAME}/{filename_gcs}"
            gcs_client = storage.Client()
            bucket = gcs_client.bucket(ASSETS_BUCKET_NAME)
            blob = bucket.blob(filename_gcs)
            blob.upload_from_string(bytes(image_data), content_type="image/png")
            tool_context.state["infographic_url"] = public_url
            tool_context.state["infographic_gcs_path"] = gcs_path
            logger.info("Uploaded infographic to %s", gcs_path)
        except Exception as exc:
            logger.error("Infographic GCS upload failed: %s", exc)
            public_url = ""

    return {
        "status": "success",
        "public_url": public_url,
        "gcs_path": gcs_path,
        "message": f"Infographic generated and uploaded to {public_url}",
    }
