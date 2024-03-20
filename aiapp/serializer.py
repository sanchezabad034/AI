import os
import requests
from django.http import JsonResponse
import json

#In this function we add the text and the image
def generateImgtxt(prompt):
    text_generated, image_url = None, None
    api_key = os.getenv('OPENAI_API_KEY')
    
    multiImagekeyword = ['imagenes', 'fotos', 'ilustraciones', 'images', 'pictures', 'illustrations', 'imagens', 'fotografias', 'ilustrações']
    imageKeyword = ['imagen', 'foto', 'ilustracion','image', 'photo', 'illustration','imagem', 'foto', 'ilustração', 'imagem', 'foto', 'ilustração']
    
    faqs = ragFaq()
    text_generated = findRag(prompt, faqs)
    
    if not text_generated: 
        text_generated = generateText(prompt, api_key)
        
    multiImage = any(keyboard in prompt.lower() for keyboard in multiImagekeyword)
    image = any(keyboard in prompt.lower() for keyboard in imageKeyword)
    
    if multiImage or image: 
        if multiImage: 
            image_url = generateMultipleImages(prompt, api_key, num_images=4)
        elif image: 
            image_url = generateImage(prompt,api_key)
            
        else: 
            image_url = None
            
    return text_generated, image_url

#In this function we generate the text 
def generateText(prompt, api_key):
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
    
    
#In this function we generate the images whit DALLE
def generateImage(prompt, api_key):
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
        image_urls = [img['url'] for img in response.json()['data']]
        return image_urls
    else:
        print("Error al generar imagen:", response.json())
        return []
    
    
#The rag function work with info about AMCO
def ragFaq():
    with open('manual_organizado.json', 'r' , encoding='utf-8') as file:
        return json.load(file)
        
def findRag(prompt, faqs):
    for i, faq in enumerate(faqs):
        if faq['role'] == 'user' and prompt.lower() in faq['content'].lower():
            if i + 1 < len(faqs) and faqs[i + 1]['role'] == 'assistant':
                return faqs[i + 1]['content']
    return None

#Generate multiple imgaes work making different images 
def generateMultipleImages(prompt, api_key, num_images=4):
    image_urls = []
    for _ in range(num_images):
        url = 'https://api.openai.com/v1/images/generations'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024',
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            image_url = response.json()['data'][0]['url']
            image_urls.append(image_url)
        else:
            print("Error al generar imagen:", response.json())
            break
    return image_urls
