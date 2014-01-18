from models import Friends, ReceivedRequests, SentRequests
from rest_framework import serializers

class FriendsSerializer(serializers.ModelSerializer):
    '''
        The Friends serializer used to display a model to the web through json serialization.
    '''
    class Meta:
        model = Friends 
        fields = ('user_id', 'friends_list')
        
class ReceivedRequestsSerializer(serializers.ModelSerializer):
    '''
        The Requests serializer used to display a model to the web through json serialization.
    '''
    class Meta:
        model = ReceivedRequests 
        fields = ('requests', )
        
class SentRequestsSerializer(serializers.ModelSerializer):
    '''
        The Requests serializer used to display a model to the web through json serialization.
    '''
    class Meta:
        model = SentRequests 
        fields = ('requests', )
