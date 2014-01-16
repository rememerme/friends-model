from models import Friends
from rest_framework import serializers

class FriendsSerializer(serializers.ModelSerializer):
    '''
        The Friends serializer used to display a model to the web through json serialization.
    '''
    class Meta:
        model = Friends 
        fields = ('user_id', 'friends_list')
