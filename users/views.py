import json
import re
import jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from wescanner.settings import SECRET_KEY,ALGORITHM
from users.models   import User

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
            return JsonResponse({"message":"KEY_ERROR"},status=400)
