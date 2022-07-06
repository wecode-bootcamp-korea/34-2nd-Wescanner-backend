import json
from os import access
import re
import jwt
import requests

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from wescanner.settings import SECRET_KEY,ALGORITHM
from users.models       import User
from core.utils         import KakaoAPI

class EmailLoginView(View):
    def post(self,request):
        try: 
            data     = json.loads(request.body)
            email    = data['email']

            REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'

            if not re.match(REGEX_EMAIL,email) :
                return JsonResponse({"message":"INVALID_EMAIL"}, status=404)

            if not User.objects.filter(email = email).exists():
                User.objects.create(
                    email = email
                )

            user = User.objects.get(email = email)

            token  = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({"access_token" : token},status=200)

        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class KakaoLoginView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization']
            kakao_api    = KakaoAPI(access_token)
            response     = kakao_api.get_kakao_user_information()
            
            kakao_id = response['id']

            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_id
            )
            
            status  = 201 if is_created else 200
            message = 'CREATE_USER' if is_created else 'LOGIN'
            
            access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
            
            message = {
                'message'      : message,
                'access_token' : access_token
                }
            
            return JsonResponse(message, status=status)            
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=404)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
