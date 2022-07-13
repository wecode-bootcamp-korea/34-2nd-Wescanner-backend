import jwt

from unittest.mock import patch, MagicMock
from django.test import Client, TestCase
from django.conf import settings

from .models import (
    Country,
    City,
    Hotel,
    Conformation,
    ImageUrl,
    Site,
    HotelSite,
)

class test_HotelList(TestCase):
    def setUp(self):
        self.client = Client()
        self.maxDiff = None 
        Country.objects.bulk_create([
            Country(
                id =1,
                name = "일본"
            ),
            Country(
                id=2,
                name = "미국"
            ),
            Country(
                id=3,
                name = "베트남"
            )
        ]) 
        City.objects.bulk_create([
            City(
                id =1,
                country_id = 1,
                name = "오사카"
            ),
            City(
                id=2,
                country_id = 1,
                name = "삿포로"
            ),
            City(
                id=3,
                country_id = 1,
                name = "후쿠오카"
            ),
            City(
                id=4,
                country_id = 2,
                name = "뉴욕"
            ),
            City(
                id=5,
                country_id = 2,
                name = "워싱턴"
            ),
            City(
                id=6,
                country_id = 2,
                name = "시애틀"
            ),
            City(
                id=7,
                country_id = 3,
                name = "다낭"
            ),
            City(
                id=8,
                country_id = 3,
                name = "하노이"
            ),
            City(
                id=9,
                country_id = 3,
                name = "호치민"
            )
        ])
        Conformation.objects.bulk_create([
            Conformation(
                id=1,
                contents = '가족'
            ),
            Conformation(
                id=2,
                contents = '비즈니스'
            ),
            Conformation(
                id=3,
                contents = '커플'
            ),
            Conformation(
                id=4,
                contents = '1인 여행객'
            ),
            Conformation(
                id=5,
                contents = '출장 여행객'
            )
        ])
        Site.objects.bulk_create([
            Site(
                id=1,
                name='노랑풍선',
                site_url="노랑풍선.url",
                logo_image_url="노랑풍선.로고.url"
            ),
            Site(
                id=2,
                name='노랑풍선',
                site_url="노랑풍선.url",
                logo_image_url="노랑풍선.로고.url"
            ),
            Site(
                id=3,
                name='파랑풍선',
                site_url="파랑풍선.url",
                logo_image_url="파랑풍선.로고.url"
            ),
            Site(
                id=4,
                name='초록풍선',
                site_url="초록풍선.url",
                logo_image_url="초록풍선.로고.url"
            ),
            Site(
                id=5,
                name='빨강풍선',
                site_url="빨강풍선.url",
                logo_image_url="빨강풍선.로고.url"
            )
        ])  
        Hotel.objects.bulk_create([
            Hotel(
                id = 1,
                city_id = 1,
                conformation_id=1,
                name = "호텔 1",
                rating = 5,
                address =  "호텔 1 주소",
                latitude = 13.60000000000000,
                longitude = 3.45550000000000 
            ),
            Hotel(
                id = 2,
                city_id = 2,
                conformation_id=2,
                name = "호텔 2",
                rating = 4,
                address = "호텔 2 주소",
                latitude = 3.63434000000000,
                longitude = 3.43434000000000
            ),
        ])
        HotelSite.objects.bulk_create([
            HotelSite(
                id=1,
                hotel_id=1,
                site_id=1,
                price=1000.000,
                is_free_cancel=True
            ),
            HotelSite(
                id=2,
                hotel_id=2,
                site_id=1,
                price=120000.000,
                is_free_cancel=False
            )
        ])
       
        ImageUrl.objects.bulk_create([
            ImageUrl(
                id = 1,
                hotel_id = 1,
                image_urls="image.1"
            ),
            ImageUrl(
                id = 2,
                hotel_id = 1,
                image_urls="image.2"
            ),
            ImageUrl(
                id = 3,
                hotel_id = 2,
                image_urls="image.3"
            ),
            ImageUrl(
                id = 4,
                hotel_id = 2,
                image_urls="image.4"
            )
        ])
    
    
    def tearDown(self):
        Hotel.objects.all().delete()
        City.objects.all().delete()
        Country.objects.all().delete()
        HotelSite.objects.all().delete()
        Site.objects.all().delete()
        ImageUrl.objects.all().delete()
        Conformation.objects.all().delete()

    def test_success_hotel_list_all(self):
        response = self.client.get('/hotels')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": [
                {
                    "hotels": {
                        "hotel_id": 1,
                        "hotel_name": "호텔 1",
                        "country_id": 1,
                        "country_name": "일본",
                        "city_id": 1,
                        "city_name": "오사카",
                        "rating": 5,
                        "address": "호텔 1 주소",
                        "latitude": "13.60000000000000",
                        "longitude": "3.45550000000000",
                        "hotel_image": [
                            {
                                "id": 1,
                                "image_url": "image.1"
                            },
                            {
                                "id": 2,
                                "image_url": "image.2"
                            }
                        ],
                        "conformation_id": 1,
                        "conformation_contents": "가족",
                        "hotel_sites": [
                            {
                                "id":1,
                                "price": "1000.000",
                                "is_free_cancel": True,
                                "site_id": 1,
                                "site_name": "노랑풍선",
                                "site_url": "노랑풍선.url",
                                "site_logo_image_url": "노랑풍선.로고.url"
                            }
                        ]
                    }
                },
                {
                    "hotels": {
                        "hotel_id": 2,
                        "hotel_name": "호텔 2",
                        "country_id": 1,
                        "country_name": "일본",
                        "city_id": 2,
                        "city_name": "삿포로",
                        "rating": 4,
                        "address": "호텔 2 주소",
                        "latitude": "3.63434000000000",
                        "longitude": "3.43434000000000",
                        "hotel_image": [
                            {
                                "id": 3,
                                "image_url": "image.3"
                            },
                            {
                                "id": 4,
                                "image_url": "image.4"
                            }
                        ],
                        "conformation_id": 2,
                        "conformation_contents": "비즈니스",
                        "hotel_sites": [
                            {
                                "id":2,
                                "price": "120000.000",
                                "is_free_cancel": False,
                                "site_id": 1,
                                "site_name": "노랑풍선",
                                "site_url": "노랑풍선.url",
                                "site_logo_image_url": "노랑풍선.로고.url"
                            }
                        ]
                    }
                }
            ]
        })