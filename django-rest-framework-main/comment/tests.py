from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from comment.models import Comment
from post.models import Post
import json

class CommentCreate(APITestCase):
    login_url = reverse("token_obtain_pair")
    def setUp(self):
        self.url = reverse("comment:create")
        self.url_list = reverse("comment:list")
        self.username = "sedattest"
        self.password = "testing963"
        self.post = Post.objects.create(title="xoxoxo title", content="xoxoxo content")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.parent_comment = Comment.objects.create(content="xoxoxo content", user=self.user, post=self.post)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.login_url, data={"username": "sedattest", "password": "testing963"})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # create comment
    def test_create_comment(self):
        data = {
            "content": "incoming comment",
            "user": self.user.id,
            "post": self.post.id,
            "parent": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    # create child comment
    def test_create_child_comment(self):
        data = {
            "content": "incoming comment",
            "user": self.user.id,
            "post": self.post.id,
            "parent": self.parent_comment.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    # test comment list
    def test_comment_list(self):
        self.test_create_comment()
        response = self.client.get(self.url_list, {'q': self.post.id})
        self.assertTrue(response.data["count"] == Comment.objects.filter(post=self.post).count())


class CommentUpdateDeleteTest(APITestCase):
    login_url = reverse("token_obtain_pair")
    def setUp(self):
        self.username = "sedattest"
        self.password = "testing963"
        self.post = Post.objects.create(title="xoxoxo title", content="xoxoxo content")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="sedattest2", password=self.password)
        self.comment = Comment.objects.create(content="xoxoxo content", user=self.user, post=self.post)
        self.url = reverse("comment:update", kwargs={'pk': self.comment.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="sedattest", password="testing963"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # yorum silme işlemi
    def test_delete_comment(self):
       response = self.client.delete(self.url)
       self.assertEqual(204, response.status_code)
       self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    # kendimizin olmayan bir değeri silmek
    def test_delete_other_user(self):
        self.test_jwt_authentication("sedattest2")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.objects.get(pk=self.comment.pk))

    #kendimizin kaydına update edelim
    def test_update_comment(self):
        response = self.client.put(self.url, data={"content": "xoxoxo"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Comment.objects.get(pk=self.comment.id).content, "xoxoxo")

    def test_update_comment_other_user(self):
        self.test_jwt_authentication("sedattest2")
        response = self.client.put(self.url, data={"content": "xoxoxo"})
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Comment.objects.get(pk=self.comment.id).content, "xoxoxo")

    def test_unauthorization(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
