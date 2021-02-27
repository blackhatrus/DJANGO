from rest_framework.test import APITestCase, force_authenticate
from records_api.serializers import RecordListSerializer, RecordHistorySerializer
from records.models import Record, Category, Comment, RecordHistory
from rest_framework import status
import json
from django.utils import timezone, dateformat
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import Client
# Create your tests here.


class RecordsListApiTest(APITestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(title="тестовая категория",
                                                description="очень крутая категория")
        self.record = Record.objects.create(
            title="Cool shop",
            category=self.category,
            record_status='published',
            body="Очень крутой лабаз в даркнете",
            url="http://duytqwtduuq.onion",
            online_status="online",
            stars=3,
            added_to_cat='год назад',
            meta_desc='чумовой магаз',
        )
        self.user = User.objects.create(
            username = "test_test",
            password= "test"
        )
        self.token = Token.objects.get(user=self.user).key
        self.c = Client()      
        

    def test_get_RecordsListAPI_with_Token(self):
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        url =  'http://127.0.0.1:8000/api/records/'
        response = self.client.get(url, format='json',**header)
        a = response.json()
        serializer_data = RecordListSerializer(self.record).data
        self.assertEquals(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEquals(serializer_data['title'], a['results'][0]['title'])

    def test_RecordHistorySerializer(self):
        record_1 = RecordHistory.objects.create(response=200, record=self.record)
        data = RecordHistorySerializer(record_1).data
        expected_data = {
         "created": dateformat.format(timezone.now(), 'Y-m-d H:i:s'),   
         "response": '200',
        } 
        self.assertEquals(expected_data, data)

    def test_get_RecordsListAPI_without_Token(self):
        url =  'http://127.0.0.1:8000/api/records/'
        response = self.client.get(url, format='json')
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

           
        
        



