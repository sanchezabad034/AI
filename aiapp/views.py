from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import generateText  
import openai
import os
import requests
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import whiperFunction, generateText, generateImgtxt

openai.api_key = os.getenv('OPENAI_API_KEY')

class GenerateTextImageView(APIView):
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')

        if prompt:
            text_generated, image_url = generateImgtxt(prompt)
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
            transcribed_text = Whisper(audio_file.temporary_file_path())
            response_text = generateText(transcribed_text)
            return JsonResponse({'transcribed_text': transcribed_text, 'response': response_text})
        else:
            return JsonResponse({'error': 'No audio file provided'}, status=400)