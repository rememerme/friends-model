from cassa import CassaModel
from django.db import models
import pycassa
from django.conf import settings
import uuid
from rest_framework import serializers
import json

# User model faked to use Cassandra
POOL = pycassa.ConnectionPool('friends', server_list=settings.CASSANDRA_NODES)

class Friends(CassaModel):
    table = pycassa.ColumnFamily(POOL, 'friends')
    
    user_id = models.TextField(primary_key=True)
    friends_list = models.TextField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Friends object from a map object with the properties.
        '''
        friends = Friends(**mapRep)
        friends.friends_list = json.loads(friends.friends_list)
        return friends

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Friends object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['user_id'] = str(cassRep[0])
        
        return Friends.fromMap(mapRep)
    
    @staticmethod
    def get(user_id=None):
        '''
            Method for getting a user's friends list from cassandra given the user_id.
        '''
        if user_id:
            return Friends.getByID(user_id)
        
        return None
    
    @staticmethod
    def getByID(user_id):
        '''
            Gets the user's friends given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)
        return Friends.fromCassa((str(user_id), Friends.table.get(user_id)))
    
    @staticmethod
    def all(limit=settings.REST_FRAMEWORK['PAGINATE_BY'], page=None):
        '''
            Gets all of the users and uses an offset and limit if
            supplied.
        
            @param offset: Optional argument. Used to offset the query by so
                many entries.
            @param limit: Optional argument. Used to limit the number of entries
                returned by the query.
        '''
        if not page:
            return [Friends.fromCassa(cassRep) for cassRep in Friends.table.get_range(row_count=limit)]
        else:
            if not isinstance(page, uuid.UUID):
                page = uuid.UUID(page)
            gen = Friends.table.get_range(start=page, row_count=limit + 1)
            gen.next()
            return [Friends.fromCassa(cassRep) for cassRep in gen]
    
    def save(self):
        '''
            Saves a set of users given by the cassandra in/output, which is
            a dictionary of values.
        
            @param users: The set of users to save to the user store.
        '''
        user_id = uuid.uuid1() if not self.user_id else uuid.UUID(self.user_id)
        Friends.table.insert(user_id, CassaFriendsSerializer(self).data)
        self.user_id = str(user_id)
        
        
class CassaFriendsSerializer(serializers.ModelSerializer):
    '''
        The User serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Friends
        fields = ('friends')

    
    
    
