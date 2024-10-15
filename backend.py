import os
import time
from PIL import Image
import pandas as pd
from openai import OpenAI
import base64
from pillow_heif import register_heif_opener
import pillow_heif
import io

# Register HEIF opener
register_heif_opener()

def is_image(filename):
    try:
        if filename.lower().endswith('.heic'):
            pillow_heif.read_heif(filename)
        else:
            Image.open(filename)
        return True
    except Exception:
        return False

def get_image_mime_type(filename):
    if filename.lower().endswith('.heic'):
        return 'image/heic'
    with Image.open(filename) as img:
        return f'image/{img.format.lower()}'

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        if image_path.lower().endswith('.heic'):
            heif_file = pillow_heif.read_heif(image_file)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(client, image_path):
    try:
        base64_image = get_image_base64(image_path)
        mime_type = get_image_mime_type(image_path)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Provide a detailed description of this "
                         "image for FEMA in the US. Focus on any visible damage, "
                         "environmental conditions, or infrastructure elements that "
                         "might be relevant for disaster assessment and response."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": "low"
                            }
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing image: {str(e)}"

def process_images(api_key, folder_path, progress_callback):
    client = OpenAI(api_key=api_key)
    
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file_path):
                image_files.append(file_path)
    
    results = []
    for i, image_path in enumerate(image_files):
        description = get_image_description(client, image_path)
        results.append({
            "Image": os.path.basename(image_path),
            "Description": description
        })
        progress_callback(
            (i + 1) / len(image_files),
            f"Processing image {i+1} of {len(image_files)}"
        )
        
        if (i + 1) % 10 == 0 and i + 1 < len(image_files):
            progress_callback(
                (i + 1) / len(image_files),
                "Taking a 2-second break..."
            )
            time.sleep(2)
    
    return pd.DataFrame(results)
