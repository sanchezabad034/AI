import os
import requests
from django.http import JsonResponse
import json

def generate_text_and_image(prompt):
    text_generated, image_url = None, None
    api_key = os.getenv('OPENAI_API_KEY')
    
    faqs = ragFaq()
    text_generated = findRag(prompt, faqs)
    
    if not text_generated:
        text_generated = generate_text_via_api(prompt, api_key)
    
    image_url = generate_image_via_api(text_generated if text_generated else prompt, api_key)
    
    return text_generated, image_url

def generate_text_via_api(prompt, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    url = 'https://api.openai.com/v1/chat/completions'
    data = {
        'model': 'gpt-4-0125-preview',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        text = response.json()['choices'][0]['message']['content'].strip()
        print(text)
        return text
    else:
        print("Error al generar texto:", response.json())
        return "Error al generar texto: revisa la solicitud o la configuración de la API."

def generate_image_via_api(prompt, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    url = 'https://api.openai.com/v1/images/generations'
    data = {
        'model': 'dall-e-3',
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024',
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        image_url = response.json()['data'][0]['url']
        return image_url
    else:
        print("Error al generar imagen:", response.json())
        return "Error al generar imagen: revisa la solicitud o la configuración de la API."

def ragFaq():
    with open('manual_organizado.json', 'r' , encoding='utf-8') as file:
        return json.load(file)
        
def findRag(prompt, faqs):
    for i, faq in enumerate(faqs):
        if faq['role'] == 'user' and prompt.lower() in faq['content'].lower():
            if i + 1 < len(faqs) and faqs[i + 1]['role'] == 'assistant':
                return faqs[i + 1]['content']
    return None

def transcribe_audio_with_whisper(audio_file_path):
    model = whisper.load_model("whisper-1")  
    result = model.transcribe(audio_file_path)
    return result["text"]