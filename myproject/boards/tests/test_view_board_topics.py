from django.test import TestCase, Client
from django.urls import reverse
from django.urls import resolve
from ..views import home, board_topics, new_topic
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from ..forms import NewTopicForm
from ..views import TopicListView

class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    """
    The resolve function is a part of Django's URL routing system. 
    It is used to match a given URL path to a corresponding view function or class-based view in your Django project.

    When a user makes a request to a specific URL, 
    Django's URL dispatcher attempts to find a matching pattern and then calls the associated view function or class with the matched parameters.

    The resolve function takes a URL path as its argument, 
    and returns a ResolverMatch object that contains information about the matched URL pattern, such as the view function or class and any captured parameters.
    """
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1') 
        self.assertEquals(view.func, TopicListView)
    
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))