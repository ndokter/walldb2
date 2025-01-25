from typing import List

from ollama import Client


def generate_image_tags(image_file_path: str) -> List[str]:
    """
    :returns: ['Disneyland', 'Disney', 'Paris', 'France', 'theme park', 'attraction']
    """
    client = Client(host='http://localhost:11434')  # TODO settings/env var
    response = client.chat(
        model='llama3.2-vision:11b',
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