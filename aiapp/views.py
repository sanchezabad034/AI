from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import generate_text_and_image  
import openai
import os
import requests
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import transcribe_audio_with_whisper, generate_text_via_api

openai.api_key = os.getenv('OPENAI_API_KEY')

class GenerateTextImageView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')

        if prompt:
            text_generated, image_url = generate_text_and_image(prompt)
            return JsonResponse({
                'text_generated': text_generated,
                'image_url': image_url
            })

        return JsonResponse({'error': 'Falta el prompt.'}, status=400)
    
    
    
class AudioGenerator(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']
            transcribed_text = transcribe_audio_with_whisper(audio_file.temporary_file_path())
            response_text = generate_text_via_api(transcribed_text)
            return JsonResponse({'transcribed_text': transcribed_text, 'response': response_text})
        else:
            return JsonResponse({'error': 'No audio file provided'}, status=400)