import logging
from typing import List

from django.conf import settings
from ollama import Client

logger = logging.getLogger(__name__)


def generate_image_tags(image_file_path: str) -> List[str]:
    """
    :returns: ['Disneyland', 'Disney', 'Paris', 'France', 'theme park', 'attraction']
    """
    logger.info("Generating ollama tags for: %s", image_file_path)

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


def generate_description(image_file_path: str) -> str:
    logger.info("Generating ollama description for: %s", image_file_path)

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
