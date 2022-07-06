from django.db import models

from core.models import TimeStampModel
# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length = 50)
    
    class Meta:
        db_table = 'countries'
    
class City(models.Model):
    country = models.ForeignKey("Country",on_delete=models.CASCADE)
    name    = models.CharField(max_length = 50)
    town    = models.CharField(max_length = 50)
    
    class Meta:
        db_table = 'cities'

class Conformation(models.Model):
    contents = models.CharField(max_length = 50)
    
    class Meta:
        db_table = 'conformations'
        
class Hotel(models.Model):   
    city         = models.ForeignKey("City",on_delete = models.CASCADE)
    conformation = models.ForeignKey("Conformation",on_delete = models.CASCADE, null=True)
    name         = models.CharField(max_length = 100)
    rating       = models.IntegerField()
    address      = models.CharField(max_length = 200)
    latitude     = models.DecimalField(max_digits=16, decimal_places=14, default=0.0)
    longitude    = models.DecimalField(max_digits=17, decimal_places=14, default=0.0)
    
    class Meta:
        db_table = 'hotels'
        
class ImageUrl(models.Model):
    hotel      = models.ForeignKey("Hotel",on_delete = models.CASCADE)
    image_urls = models.URLField()
    
    class Meta:
        db_table = 'image_urls'

class Site(models.Model):   
    name           = models.CharField(max_length = 50)
    site_url       = models.URLField()
    logo_image_url = models.URLField()
    
    class Meta:
        db_table = 'sites'
        
class HotelSite(models.Model):   
    hotel          = models.ForeignKey("Hotel",on_delete = models.CASCADE)
    site           = models.ForeignKey("Site",on_delete = models.CASCADE)
    price          = models.DecimalField(max_digits = 10, decimal_places = 3)
    is_free_cancel = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'hotels_sites'

class Reserved(TimeStampModel):
    hotel     = models.ForeignKey("Hotel",on_delete = models.CASCADE)
    check_in  = models.DateField()
    check_out = models.DateField()
    
    class Meta:
        db_table = 'reserved'