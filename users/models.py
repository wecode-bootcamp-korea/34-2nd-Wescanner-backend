from django.db import models

from core.models import TimeStampModel

# Create your models here.
class User(TimeStampModel):   
    email    = models.CharField(max_length = 45,unique = True)
    kakao_id = models.BigIntegerField(unique = True, null=True)
    class Meta:
        db_table = 'users'

class Review(TimeStampModel):   
    user     = models.ForeignKey("User",on_delete = models.CASCADE)
    hotel    = models.ForeignKey("hotels.Hotel",on_delete = models.CASCADE)
    contents = models.TextField()
    rating   = models.IntegerField()
    
    class Meta:
        db_table = 'reviews'

class ReviewImage(TimeStampModel):   
    review = models.ForeignKey("Review",on_delete = models.CASCADE)
    url    = models.URLField()
    
    class Meta:
        db_table = 'review_images'
        
class WishList(TimeStampModel):   
    user   = models.ForeignKey("User",on_delete = models.CASCADE)
    hotel  = models.ForeignKey("hotels.Hotel",on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'wish_lists'
