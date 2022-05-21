from rest_framework import serializers
from .models import challenge, challenge_check, challenge_user

class challengeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = challenge
        fields = '__all__'
        #fields = fields = ('challenge_id','name','start_date','start_date','end_date','image','goal','contents','creator_id')



class challengeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = challenge_user
        fields = '__all__'

        # fields = ('challenge_id','user_id','start_date')


class challengeCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = challenge_check
        fields = '__all__'

        # fields = ('challenge_id','user_id','check_date')
