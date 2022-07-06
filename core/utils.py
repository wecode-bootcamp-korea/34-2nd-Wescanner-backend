import json
import re
import jwt
import requests

from django.http            import JsonResponse
from django.views           import View

from wescanner.settings import SECRET_KEY,ALGORITHM
from users.models       import User

# kakao.py
class KakaoAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.user_url     = "https://kapi.kakao.com/v2/user/me"

    def get_kakao_user_information(self):
        headers = {"Authorization": f'bearer{self.access_token}'}
        response = requests.get(self.user_url, headers=headers, timeout=3).json()

        if response.get('code') == -1:
                return JsonResponse({'message' : 'KAKAO_ERROR'}, status=400)

        if response.get('code') == -401:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)
        
        if 'email' not in response['kakao_account']:
            return JsonResponse({'message': 'NONE_EMAIL'}, status = 405)
            
        return response

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            assess_token = request.headers.get('Authorization',None) 
            payload      = jwt.decode(assess_token, SECRET_KEY, ALGORITHM) 
            user         = User.objects.get(id=payload['user_id']) 
            request.user = user
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.InvalidSignatureError: 
            return JsonResponse({'message': 'INVALID_SIGNATURE_ERROR'}, status=401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR' }, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST_ERROR'}, status=401)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=401)
    return wrapper   