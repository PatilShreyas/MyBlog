from django.test import TestCase

from MyBlog.forms import SignInForm, SignUpForm, PostForm


class SignInFormTest(TestCase):
    def test_signin_form_label(self):
        form = SignInForm(data={'username': 'testuser', 'password': 'test#1234'})
        self.assertEqual(form.fields['username'].label, "Username")
        self.assertEqual(form.fields['password'].label, "Password")


class SignUpFormTest(TestCase):
    def test_signup_form_valid(self):
        form = SignUpForm(data={'first_name': 'First Name',
                                'last_name': 'Last Name',
                                'username': 'testuser',
                                'email': 'mail@email.com',
                                'password1': 'test#1234',
                                'password2': 'test#1234'})

        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form = SignUpForm(data={'first_name': 'First Name',
                                'last_name': 'Last Name',
                                'username': 'testuser',
                                'email': 'mail',
                                'password1': 'test',
                                'password2': 'test'})

        self.assertFalse(form.is_valid())


class PostFormTest(TestCase):
    def test_post_form_valid(self):
        form = PostForm(data={'title': 'Hi there',
                              'content': 'This is content',
                              'tags': 'tag1, tag2',
                              'category': 1})

        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form = PostForm(data={'title': '',
                              'content': '',
                              'tags': '',
                              'category': 0})

        self.assertFalse(form.is_valid())
