import json
from datetime import datetime, timedelta

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

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
        price_min       = request.GET.get('price_min',0)
        price_max       = request.GET.get('price_max',1000000)
        country_id      = request.GET.get('country_id')
        hotel_id        = request.GET.get('hotel_id')
        city_id         = request.GET.get('city_id')
        rating          = request.GET.get('rating')
        is_free_cancel  = request.GET.get('is_free_cancel')
        conformation_id = request.GET.get('conformation_id')
        sort            = request.GET.get('sort','?')

        q = Q()

        if country_id:
            q &= Q(city__country_id = country_id)
            
        if city_id:
            q &= Q(city_id = city_id)

        if hotel_id:
            q &= Q(id = hotel_id)

        if conformation_id :
            q &= Q(conformation_id=conformation_id)

        if rating :
            q &= Q(rating=rating)
            
        p = Q()

        if price_min and price_max :
           p &= Q(price__range = (price_min,price_max))
        
        if price_max == '100000' :
            p &=  Q(price__lte=100000)
        
        elif price_max == '200000' : 
            p &=  Q(price__lte=200000)
        
        elif price_max == '400000' : 
            p &=  Q(price__lte=400000)
        
        elif price_max == '600000' : 
            p &=  Q(price__lte=600000)
        
        elif price_max == '800000' : 
            p &=  Q(price__lte=800000)

        elif price_max == '1000000' : 
            p &=  Q(price__lte=1000000)

        if is_free_cancel :
            p &= Q(is_free_cancel = is_free_cancel)
        
        a = Q()

        if check_in and check_out:
            check_in  = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')
             
            a &= Q(reserved__check_in__range=(check_in, check_out))
            a &= Q(reserved__check_out__range=(check_in, check_out))
        
        sort_set = {
            'random'     : '?',
            'low_price'  : 'hotelsite__price',
            'high_price' : '-hotelsite__price'
        } 
        
        order_field = sort_set.get(sort, 'id')

        hotels = Hotel.objects.filter(q).exclude(a).order_by(order_field)
        
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
                        "latitude"     : hotel.latitude,
                        "longitude"    : hotel.longitude,
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
                                "price"               : hotelsite.price,
                                "is_free_cancel"      : hotelsite.is_free_cancel,
                                "site_id"             : hotelsite.site.id,
                                "site_name"           : hotelsite.site.name,
                                "site_url"            : hotelsite.site.site_url,
                                "site_logo_image_url" : hotelsite.site.logo_image_url,
                           
                            } for hotelsite in hotel.hotelsite_set.filter(p)
                        ]
                    }
            } for hotel in hotels
        ]
        
        return JsonResponse({"message" : result}, status = 200)