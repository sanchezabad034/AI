from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import generateText  
import openai
import os
import requests
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import generateText, generateImgtxt

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