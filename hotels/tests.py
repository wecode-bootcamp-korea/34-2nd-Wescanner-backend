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
            Hotel(
                id = 3,
                city_id = 3,
                conformation_id=3,
                name = "호텔 3",
                rating = 5,
                address = "호텔 3 주소",
                latitude = 3.62323000000000,
                longitude = 3.42323000000000
            ),
            Hotel(
                id = 4,
                city_id = 4,
                conformation_id=4,
                name = "호텔 4",
                rating = 3,
                address = "호텔 4 주소",
                latitude = 3.62332300000000,
                longitude = 3.42332300000000 
            ),
            Hotel(
                id = 5,
                city_id = 5,
                conformation_id=5,
                name = "호텔 5",
                rating = 5,
                address = "호텔 5 주소",
                latitude = 39.62332300000000,
                longitude = 38.42332300000000
            ),
            Hotel(
                id = 6,
                city_id = 6,
                conformation_id=1,
                name = "호텔 6",
                rating = 2,
                address = "호텔 6 주소",
                latitude = 39.66233230000000,
                longitude = 38.46233230000000 
            ),
            Hotel(
                id = 7,
                city_id = 7,
                conformation_id=4,
                name = "호텔 7",
                rating = 5,
                address = "호텔 7 주소",
                latitude = 96.66233230000000,
                longitude = 68.46233230000000 
            ),
            Hotel(
                id = 8,
                city_id = 8,
                conformation_id=3,
                name = "호텔 8",
                rating = 4,
                address = "호텔 8 주소",
                latitude = 6.66233230000000,
                longitude = 8.46233230000000 
            ),
            Hotel(
                id = 9,
                city_id = 9,
                conformation_id=2,
                name = "호텔 9",
                rating = 5,
                address = "호텔 9 주소",
                latitude = 66.62332300000000,
                longitude = 68.46233230000000
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
        ),
        HotelSite(
            id=3,
            hotel_id=3,
            site_id=2,
            price=100000.000,
            is_free_cancel=True
        ),
        HotelSite(
            id=4,
            hotel_id=4,
            site_id=3,
            price=999900.000,
            is_free_cancel=False
        ),
        HotelSite(
            id=5,
            hotel_id=5,
            site_id=2,
            price=700000.000,
            is_free_cancel=True
        ),
        HotelSite(
            id=6,
            hotel_id=6,
            site_id=3,
            price=600000.000,
            is_free_cancel=False
        ),
        HotelSite(
            id=7,
            hotel_id=7,
            site_id=5,
            price=400000.000,
            is_free_cancel=True
        ),
        HotelSite(
            id=8,
            hotel_id=7,
            site_id=4,
            price=50000.000,
            is_free_cancel=False
        ),
        HotelSite(
            id=9,
            hotel_id=8,
            site_id=1,
            price=500000.000,
            is_free_cancel=True
        ),
        HotelSite(
            id=10,
            hotel_id=9,
            site_id=2,
            price=10000.000,
            is_free_cancel=False
        ),
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
            ),
            ImageUrl(
                id = 5,
                hotel_id = 3,
                image_urls="image.5"
            ),
            ImageUrl(
                id = 6,
                hotel_id = 3,
                image_urls="image.6"
            ),
            ImageUrl(
                id = 7,
                hotel_id = 4,
                image_urls="image.7"
            ),
            ImageUrl(
                id = 8,
                hotel_id = 4,
                image_urls="image.8"
            ),
            ImageUrl(
                id = 9,
                hotel_id = 4,
                image_urls="image.9"
            ),
            ImageUrl(
                id = 10,
                hotel_id = 5,
                image_urls="image.10"
            ),
            ImageUrl(
                id = 11,
                hotel_id = 6,
                image_urls="image.11"
            ),
            ImageUrl(
                id = 12,
                hotel_id = 6,
                image_urls="image.12"
            ),
            ImageUrl(
                id = 13,
                hotel_id = 7,
                image_urls="image.13"
            ),
            ImageUrl(
                id = 14,
                hotel_id = 8,
                image_urls="image.14"
            ),
            ImageUrl(
                id = 15,
                hotel_id = 9,
                image_urls="image.15"
            ),
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
                "latitude": 13.60000000000000,
                "longitude": 3.45550000000000,
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
                        "price": 1000.000,
                        "is_free_cancel": True,
                        "site_id": 1,
                        "site_name": "노랑풍선",
                        "site_url": "노랑풍선.url",
                        "site_logo_image_url": "노랑풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 2,
                "hotel_name": "호텔 2",
                "country_id": 1,
                "country_name": "일본",
                "city_id": 2,
                "city_name": "삿포로",
                "rating": 4,
                "address": "호텔 2 주소",
                "latitude": 3.63434000000000,
                "longitude": 3.43434000000000,
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
                        "price": 120000.000,
                        "is_free_cancel": False,
                        "site_id": 1,
                        "site_name": "노랑풍선",
                        "site_url": "노랑풍선.url",
                        "site_logo_image_url": "노랑풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 3,
                "hotel_name": "호텔 3",
                "country_id": 1,
                "country_name": "일본",
                "city_id": 3,
                "city_name": "후쿠오카",
                "rating": 5,
                "address": "호텔 3 주소",
                "latitude": 3.62323000000000,
                "longitude": 3.42323000000000,
                "hotel_image": [
                    {
                        "id": 5,
                        "image_url": "image.5"
                    },
                    {
                        "id": 6,
                        "image_url": "image.6"
                    }
                ],
                "conformation_id": 3,
                "conformation_contents": "커플",
                "hotel_sites": [
                    {
                        "id":3,
                        "price": 100000.000,
                        "is_free_cancel": True,
                        "site_id": 2,
                        "site_name": "노랑풍선",
                        "site_url": "노랑풍선.url",
                        "site_logo_image_url": "노랑풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 4,
                "hotel_name": "호텔 4",
                "country_id": 2,
                "country_name": "미국",
                "city_id": 4,
                "city_name": "뉴욕",
                "rating": 3,
                "address": "호텔 4 주소",
                "latitude": 3.62332300000000,
                "longitude": 3.42332300000000,
                "hotel_image": [
                    {
                        "id": 7,
                        "image_url": "image.7"
                    },
                    {
                        "id": 8,
                        "image_url": "image.8"
                    },
                    {
                        "id": 9,
                        "image_url": "image.9"
                    }
                ],
                "conformation_id": 4,
                "conformation_contents": '1인 여행객',
                "hotel_sites": [
                    {
                        "id":4,
                        "price": 999900.000,
                        "is_free_cancel": False,
                        "site_id": 3,
                        "site_name": "파랑풍선",
                        "site_url": "파랑풍선.url",
                        "site_logo_image_url": "파랑풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 5,
                "hotel_name": "호텔 5",
                "country_id": 2,
                "country_name": "미국",
                "city_id": 5,
                "city_name": "워싱턴",
                "rating": 5,
                "address": "호텔 5 주소",
                "latitude": 39.62332300000000,
                "longitude": 38.42332300000000,
                "hotel_image": [
                    {
                        "id": 10,
                        "image_url": "image.10"
                    }
                ],
                "conformation_id": 5,
                "conformation_contents": '출장 여행객',
                "hotel_sites": [
                    {
                        "id":5,
                        "price": 700000.000,
                        "is_free_cancel": True,
                        "site_id": 5,
                        "site_name": "빨강풍선",
                        "site_url": "빨강풍선.url",
                        "site_logo_image_url": "빨강풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 6,
                "hotel_name": "호텔 6",
                "country_id": 2,
                "country_name": "미국",
                "city_id": 6,
                "city_name": "시애틀",
                "rating": 2,
                "address": "호텔 6 주소",
                "latitude": 39.66233230000000,
                "longitude": 38.46233230000000,
                "hotel_image": [
                    {
                        "id": 11,
                        "image_url": "image.11"
                    },
                    {
                        "id": 12,
                        "image_url": "image.12"
                    }
                ],
                "conformation_id": 1,
                "conformation_contents": '가족',
                "hotel_sites": [
                    {
                        "id":6,
                        "price": 600000.000,
                        "is_free_cancel": False,
                        "site_id": 3,
                        "site_name": "파랑풍선",
                        "site_url": "파랑풍선.url",
                        "site_logo_image_url": "파랑풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 7,
                "hotel_name": "호텔 7",
                "country_id": 3,
                "country_name": "베트남",
                "city_id": 7,
                "city_name": "다낭",
                "rating": 5,
                "address": "호텔 7 주소",
                "latitude": 96.66233230000000,
                "longitude": 68.46233230000000,
                "hotel_image": [
                    {
                        "id": 13,
                        "image_url": "image.13"
                    }
                ],
                "conformation_id": 4,
                "conformation_contents": '1인 여행객',
                "hotel_sites": [
                    {
                        "id":7,
                        "price": 600000.000,
                        "is_free_cancel": True,
                        "site_id": 5,
                        "site_name": "빨강풍선",
                        "site_url": "빨강풍선.url",
                        "site_logo_image_url": "빨강풍선.로고.url"
                    },
                    {
                        "id":8,
                        "price": 50000.000,
                        "is_free_cancel": False,
                        "site_id": 4,
                        "site_name": "초록풍선",
                        "site_url": "초록풍선.url",
                        "site_logo_image_url": "초록풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 8,
                "hotel_name": "호텔 8",
                "country_id": 3,
                "country_name": "베트남",
                "city_id": 8,
                "city_name": "하노이",
                "rating": 4,
                "address": "호텔 8 주소",
                "latitude": 6.6623323,
                "longitude": 8.4623323,
                "hotel_image": [
                    {
                        "id": 14,
                        "image_url": "image.14"
                    }
                ],
                "conformation_id": 3,
                "conformation_contents": '커플',
                "hotel_sites": [
                    {
                        "id":9,
                        "price": 500000.000,
                        "is_free_cancel": True,
                        "site_id": 1,
                        "site_name": "노랑풍선",
                        "site_url": "노랑풍선.url",
                        "site_logo_image_url": "노랑풍선.로고.url"
                    }
                ]
            },
            "hotels": {
                "hotel_id": 9,
                "hotel_name": "호텔 9",
                "country_id": 3,
                "country_name": "베트남",
                "city_id": 9,
                "city_name": "호치민",
                "rating": 5,
                "address": "호텔 9 주소",
                "latitude": 66.62332300000000,
                "longitude": 68.46233230000000,
                "hotel_image": [
                    {
                        "id": 15,
                        "image_url": "image.15"
                    }
                ],
                "conformation_id": 2,
                "conformation_contents": '비즈니스',
                "hotel_sites": [
                    {
                        "id":10,
                        "price": 10000.000,
                        "is_free_cancel": False,
                        "site_id": 2,
                        "site_name": "노랑풍선",
                        "site_url": "노랑풍선.url",
                        "site_logo_image_url": "노랑풍선.로고.url"
                    }
                ]
            }
        },
            ]
        }
    
        )