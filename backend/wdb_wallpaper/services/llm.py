import base64
import logging
import mimetypes
from typing import List

import deepinfra
import requests
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
        response = requests.post(
            settings.DEEPINFRA_API_URL, 
            headers={
                "Authorization": f"Bearer {settings.DEEPINFRA_API_KEY}",
                "Content-Type":  "application/json",
            }, 
            json={
                "model": 'google/gemma-3-12b-it',
                "messages": [
                    {
                        "role":  "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": _encode_image_to_base64_url(image_file_path)}
                            },
                            {
                                "type": "text",
                                "text":  "List 8 relevant tags for this image with commas. Dont say anything else."
                            }
                        ]
                    }
                ]
            }
        )

        response.raise_for_status()
        tags = response.json()["choices"][0]["message"]["content"]
    
        tags = tags.split(',')
        tags = [tag.strip().lower() for tag in tags]

        return tags


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

    elif provider == 'deepinfra':
        response = requests.post(
            settings.DEEPINFRA_API_URL, 
            headers={
                "Authorization": f"Bearer {settings.DEEPINFRA_API_KEY}",
                "Content-Type":  "application/json",
            }, 
            json={
                "model": 'google/gemma-3-12b-it',
                "messages": [
                    {
                        "role":  "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": _encode_image_to_base64_url(image_file_path)}
                            },
                            {
                                "type": "text",
                                "text": "Generate a paragraph of search terms that describes the image in both contents, style, color use and atmosphere and show me the paragraph only"
                            }
                        ]
                    }
                ]
            }
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def _encode_image_to_base64_url(image_path: str) -> str:
    """
    Encodes a local image file into a Base64 data URI.
    This is required used to send image to OpenAI compatible vision APIs.
    """
    # Guess MIME type
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith('image'):
        raise ValueError(f"Could not determine image type for {image_path}")

    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Format as a data URI
    return f"data:{mime_type};base64,{base64_encoded_data}"