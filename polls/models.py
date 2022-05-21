from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField, IntegerField

# Create your models here.
class challenge(models.Model):
    
    challenge_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.CharField(max_length=100,blank=True)
    contents = models.CharField(max_length=200)
    creator_id = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'Challenge'
    
    def publish(self):
        self.save()


class challenge_user(models.Model):      
    challenge_id = models.ForeignKey('challenge', on_delete=CASCADE, db_column='challenge_id')
    user_id = models.CharField(max_length=200)
    start_date = models.DateField()
    num = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'Challenge_User'

class challenge_check(models.Model):
    challenge_id = models.ForeignKey('challenge', on_delete=CASCADE, db_column='challenge_id')
    user_id = models.CharField(max_length=200)
    check_date = models.DateField()
    num = models.AutoField(primary_key=True)


    class Meta:
        db_table = 'Challenge_Check'


