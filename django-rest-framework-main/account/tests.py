from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.utils import json


class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")
    def test_user_registration(self):
    #Doğru veriler ile kayıt işlemi.
        data = {
            "username": "sedattest",
            "password": "testing963"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
    #invalid password verisi ile kayıt işlemi.
        data = {
            "username": "sedattest",
            "password": "1"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
    #unique isim testi.
        self.test_user_registration()
        data = {
            "username": "sedattest",
            "password": "xoxoxoxoxoxo"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
    #session ile giris yapmıs kullanıcı sayfayi gorememeli.
        self.test_user_registration()
        self.client.login(username='sedattest', password='testing963')
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)


    def test_user_authenticated_token_registration(self):
    #token ile giriş yapmış kullanıcı sayfayı görememeli.
        self.test_user_registration()
        data = {
            "username": "sedattest",
            "password": "testing963"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)
#***************************************************************************
class UserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")
    #burada setup'i yaptik
    def setUp(self):
        self.username = "sedattest"
        self.password = "testing963"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
         response = self.client.post(self.url_login, {"username": "sedattest", "password": "testing963"})
         self.assertEqual(200, response.status_code)
         self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
         response = self.client.post(self.url_login, {"username": "xoxoxoxoxo", "password": "xoxoxoxo963"})
         self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
         response = self.client.post(self.url_login, {"username": "", "password": ""})
         self.assertEqual(400, response.status_code)
#****************************************************************************
class UserPasswordChange(APITestCase):
    url = reverse("account:change-password")
    url_login = reverse("token_obtain_pair")
    def setUp(self):
        self.username = "sedattest"
        self.password = "testing963"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": "sedattest",
            "password": "testing963"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # oturum açılmadan girildiğinde hata
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "old_password": "testing963",
            "new_password": "testing369"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)

    def test_with_wrong_informations(self):
        self.login_with_token()
        data = {
            "old_password": "xoxoxoxo",
            "new_password": "testing369"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_with_empty_informations(self):
        self.login_with_token()
        data = {
            "old_password": "",
            "new_password": ""
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)
#******************************************************
class UserProfileUpdate(APITestCase):
    url = reverse("account:me")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "sedattest"
        self.password = "testing963"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": "sedattest",
            "password": "testing963"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

    # oturum acilmadan girildiginde hata
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "id": 1,
            "first_name": "",
            "last_name": "",
            "profile": {
                "id": 1,
                "about": "xoxoxo",
                "address": "xoxoxo"
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), data)

    def test_with_empty_informations(self):
        self.login_with_token()
        data = {
            "id": 1,
            "first_name": "",
            "last_name": "",
            "profile": {
                "id": 1,
                "about": "",
                "address": ""
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(400, response.status_code)