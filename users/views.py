import json
import re
import jwt
import requests
import boto3

from django.db              import transaction
from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from wescanner.settings import SECRET_KEY,ALGORITHM
from users.models       import User, Review

from core.utils import KakaoAPI, login_decorator
from core.s3    import AWSFileUploader, FileHandler

from wescanner.settings  import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_KEY,
    AWS_STORAGE_BUCKET_NAME,
    AWS_REGION,
    IMAGE_URL,
    AWS_LOCATION
    )

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


boto3_client = boto3.client(
    's3',
    aws_access_key_id     =  AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_KEY
)

config = {
    "bucket_name" : AWS_STORAGE_BUCKET_NAME,
    "region"      : AWS_REGION
}

aws_file_uploader  =  AWSFileUploader(boto3_client, config)

file_handler = FileHandler(aws_file_uploader)

class ReviewView(View):
    @login_decorator
    def post(self, request):
        try:
            user             = request.user
            hotel_id         = request.POST['hotel_id']
            rating           = request.POST['rating']
            contents         = request.POST['content']
            review_image     = request.FILES['review_image']

            review_image_url = file_handler.upload(directory = AWS_LOCATION, file = review_image)

            with transaction.atomic():
                reviews = Review.objects.create(
                    user_id   = user.id,
                    hotel_id  = hotel_id,
                    rating    = rating,
                    contents  = contents,
                )

            Review.objects.get(id = reviews.id).reviewimage_set.create(url = review_image_url)

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status = 400)
        except transaction.TransactionManagementError:
            return JsonResponse({'message': 'TransactionManagementError'}, status = 400)

    @login_decorator
    def delete(self, request):
        try:
            review_id = request.GET.get('review_id')
            file_url  = Review.objects.get(id = review_id).reviewimage_set.url

            file_handler.delete(file_url)

            return JsonResponse(status = 204)

        except Review.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Review'}, status = 400)

   
