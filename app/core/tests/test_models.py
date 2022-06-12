
"""
Test for Models
"""

from multiprocessing.sharedctypes import Value
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class ModelTest(TestCase):
    
    def test_create_user_with_email_succesful(self):
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test normalized email for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_failure(self):
        """Test creating user with an email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", 'sample123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email = "test@example.com",
            password='test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)