import json

from django.http      import JsonResponse
from django.views     import View

from .models import Country

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