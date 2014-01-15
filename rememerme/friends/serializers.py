from models import Friends
from rest_framework import serializers

'''
    The User serializer used to display a model to the web through json serialization.
'''
class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends 
        fields = ('user_id', 'friends')
