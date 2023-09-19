from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)