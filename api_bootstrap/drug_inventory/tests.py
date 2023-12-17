from rest_framework.test import APITestCase
from rest_framework import status
from .models import Drug, Category, Transaction
from django.urls import reverse

class DrugTests(APITestCase):
    def setUp(self):
        Category.objects.create(name='Analgesics')
        self.valid_payload = {
            'name': 'Paracetamol',
            'category': 1,
            'price': 50.0,
            'quantity': 100
        }
        self.invalid_payload = {
            'name': '',
            'category': 1,
            'price': 50.0,
            'quantity': 100
        }

    def test_create_drug(self):
        """
        Ensure we can create a new drug object.
        """
        url = reverse('drug-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drug.objects.count(), 1)
        self.assertEqual(Drug.objects.get().name, 'Paracetamol')

    def test_create_invalid_drug(self):
        """
        Ensure we cannot create a new drug object with invalid payload.
        """
        url = reverse('drug-list')
        response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)