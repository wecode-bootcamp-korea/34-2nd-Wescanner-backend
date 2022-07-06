import jwt

from unittest.mock import patch, MagicMock
from django.test import Client, TestCase
from django.conf import settings

from users.models import User

class test_KakaoLogin(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 5,
            kakao_id = '2323232',
            email    = 'q1w2e3r4@naver.com'
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('core.utils.requests')
    def test_success_kakao_login(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id'            : 2323232, 
                    'connected_at'  : '2022-07-06T08:16:22Z', 
                    'kakao_account' : {
                        'has_email'             : True, 
                        'email_needs_agreement' : False, 
                        'is_email_valid'        : True, 
                        'is_email_verified'     : True, 
                        'email'                 : 'q1w2e3r4@naver.com'
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': '1343434'}
        response            = client.get('/users/kakao', **headers)
        access_token        = jwt.encode({'user_id': User.objects.get(id=5).id}, settings.SECRET_KEY, settings.ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'message'      : 'LOGIN',
            'access_token' : access_token
        })

    @patch('core.utils.requests')
    def test_success_kakao_create(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id'            : 2342342, 
                    'connected_at'  : '2022-07-06T08:16:22Z', 
                    'kakao_account' : {
                        'has_email'             : True, 
                        'email_needs_agreement' : False, 
                        'is_email_valid'        : True, 
                        'is_email_verified'     : True, 
                        'email'                 : 'a12s2d34f4@naver.com'
                        }
                    }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': '3434346'}
        response            = client.get('/users/kakao', **headers)
        access_token        = jwt.encode({'user_id': 6}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),{
                'message'      : 'CREATE_USER',
                'access_token' : access_token 
        })