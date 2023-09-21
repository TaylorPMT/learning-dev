from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import TopicListView


class TopicPostsTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        board = Board.objects.create(name='Django', description='Django board.')
        topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user, updated_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)
        self.url = url

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(self.url)
        self.assertEquals(view.func, TopicListView)