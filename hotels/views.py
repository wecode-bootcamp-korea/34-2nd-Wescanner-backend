import json
from datetime import datetime, timedelta

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Min, Max

from .models import (
    Country,
    Hotel
)

# Create your views here.
class SearchView(View):
    def get(self, request):
        countries = Country.objects.all()
        
        results = [
                    {   
                        'id'     : country.id,
                        'name'   : country.name,
                        'cities' : [
                            {
                                'id'       : city.id,
                                'name'     : city.name,
                                'town'     : city.town,
                                'hotels' :[
                                    {   
                                        'id'  : hotel.id,
                                        'name': hotel.name
                                            }for hotel in city.hotel_set.all()
                                    ]
                            } for city in country.city_set.all()
                        ]
                        }for country in countries
                    ]
        return JsonResponse({'result' : results}, status = 200)

class HotelListView(View):
    def get(self, request):
        check_in        = request.GET.get("check_in")
        check_out       = request.GET.get("check_out")
        sort            = request.GET.get('sort','id')
        
        FILTER_SET = {
            'country_id' : 'city__country_id',
            'city_id'    : 'city_id',
            'rating'     : 'rating__in',
            'hotel_id'   : 'id',
            'conformation_id' : 'conformation_id__in',
            'price_max'      :'hotelsite__price__lte',
        }

        HOTEL_FILTER_SET = {
            'price_max'      :'price__lte',
            'is_free_cancel' : 'is_free_cancel'
        }

        SORT_SET = {
            'id'         : 'id',
            'random'     : '?',
            'low_price'  : 'hotelsite__price',
            'high_price' : '-hotelsite__price'
        }
        
        q = {FILTER_SET.get(key) : json.loads(value) for key, value in request.GET.items() if key in FILTER_SET.keys()}
        p = {HOTEL_FILTER_SET.get(key) : json.loads(value) for key, value in request.GET.items() if key in HOTEL_FILTER_SET.keys()}
  
        a = Q()

        if check_in and check_out:
            check_in  = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')
             
            a &= Q(reserved__check_in__range=(check_in, check_out))
            a &= Q(reserved__check_out__range=(check_in, check_out))
        
        hotels = Hotel.objects.filter(**q).exclude(a).order_by(SORT_SET[sort])

        result = [
            {
                "hotels" : 
                    {
                        "hotel_id"     : hotel.id,
                        "hotel_name"   : hotel.name,
                        "country_id"   : hotel.city.country.id,
                        "country_name" : hotel.city.country.name,
                        "city_id"      : hotel.city.id,
                        "city_name"    : hotel.city.name,
                        "rating"       : hotel.rating,
                        "address"      : hotel.address,
                        "latitude"     : str(hotel.latitude),
                        "longitude"    : str(hotel.longitude),
                        "hotel_image" : [
                            {
                            "id"        : image_url.id,
                            "image_url" : image_url.image_urls
                        } for image_url in hotel.imageurl_set.all()
                        ],
                        "conformation_id"       : hotel.conformation.id,
                        "conformation_contents" : hotel.conformation.contents,
                        "hotel_sites" : [
                            {
                                "id"                  : hotelsite.id,
                                "price"               : str(hotelsite.price),
                                "is_free_cancel"      : hotelsite.is_free_cancel,
                                "site_id"             : hotelsite.site.id,
                                "site_name"           : hotelsite.site.name,
                                "site_url"            : hotelsite.site.site_url,
                                "site_logo_image_url" : hotelsite.site.logo_image_url,
                            } for hotelsite in hotel.hotelsite_set.filter(**p)
                        ]
                    }
            } for hotel in hotels
        ]
        
        return JsonResponse({"message" : result}, status = 200)