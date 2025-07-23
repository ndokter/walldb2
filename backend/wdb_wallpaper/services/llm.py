import base64
import logging
import mimetypes
from typing import List

import deepinfra
from django.conf import settings
from ollama import Client

logger = logging.getLogger(__name__)


def generate_image_tags(provider:str, image_file_path: str) -> List[str]:
    """
    :returns: ['Disneyland', 'Disney', 'Paris', 'France', 'theme park', 'attraction']
    """

    logger.info("Generating %s tags for: %s", provider, image_file_path)

    if provider == 'ollama':
        client = Client(host=settings.OLLAMA_HOST)  
        response = client.chat(
                model='gemma3:4b',
            messages=[{
                'role': 'user',
                'content': 'List 6 relevant tags for this image with commas',
                'images': [image_file_path]
            }]
        )

        content = response.message.content
        content = content.strip('.')
        
        tags = content.split(',')
        tags = [tag.strip().lower() for tag in tags]

        return tags

    elif 'deepinfra':
        client = deepinfra.Client()
        
        base64_image_url = _encode_image_to_base64_url(image_file_path)

        response = client.chat.completions.create(
            # Use a model on DeepInfra that supports vision, like LLaVA
            model="llava-hf/llava-v1.6-mistral-7b-hf", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": 'List 6 relevant tags for this image with commas'
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": base64_image_url},
                        },
                    ],
                }
            ],
            max_tokens=100,
        )

        content = response.choices[0].message.content

        return content


def generate_description(provider: str, image_file_path: str) -> str:
    logger.info("Generating %s description for: %s", provider, image_file_path)

    if provider == 'ollama':
        client = Client(host=settings.OLLAMA_HOST)
        response = client.chat(
            model='llama3.2-vision:11b',
            messages=[{
                'role': 'user',
                'content': 'Describe this image in a maximum of 4 sentences',
                'images': [image_file_path]
            }]
        )

        return response.message.content



def _encode_image_to_base64_url(image_path: str) -> str:
    """
    Encodes a local image file into a Base64 data URI.
    This is required by most vision APIs, regardless of the SDK.
    """
    # Guess the MIME type of the image
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image'):
        raise ValueError(f"Could not determine image type for {image_path}")

    # Read the image in binary mode and encode it
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Format as a data URI
    return f"data:{mime_type};base64,{base64_encoded_data}"