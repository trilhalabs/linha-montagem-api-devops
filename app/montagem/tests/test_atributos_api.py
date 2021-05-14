from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Atributo, Montagem

from montagem.serializers import AtributoSerializer


ATRIBUTOS_URL = reverse('montagem:atributo-list')


class PublicAtributosApiTests(TestCase):
    """Teste a API de atributos publicamente disponível"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Teste se o login eh necessario para acessar o endpoint"""
        res = self.client.get(ATRIBUTOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAtributosApiTests(TestCase):
    """Teste a API de atributos privados"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@tslabs.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_atributo_list(self):
        """Teste recuperando uma lista de atributos"""
        Atributo.objects.create(user=self.user, name='Alex')
        Atributo.objects.create(user=self.user, name='Xande')

        res = self.client.get(ATRIBUTOS_URL)

        atributos = Atributo.objects.all().order_by('-name')
        serializer = AtributoSerializer(atributos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_atributos_limited_to_user(self):
        """Teste se os atributos para o usuario autenticado sao retornados"""
        user2 = get_user_model().objects.create_user(
            'other@tslabs.com',
            'testpass'
        )
        Atributo.objects.create(user=user2, name='AWS')
        atributo = Atributo.objects.create(user=self.user, name='Bucket')

        res = self.client.get(ATRIBUTOS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], atributo.name)

    def test_create_atributo_successful(self):
        """Teste a criacao de um novo atributo"""
        payload = {'name': 'Terraform'}
        self.client.post(ATRIBUTOS_URL, payload)

        exists = Atributo.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_atributo_invalid(self):
        """Teste de falha de criacao de atributo invalido"""
        payload = {'name': ''}
        res = self.client.post(ATRIBUTOS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_atributos_assigned_to_montagens(self):
        """Testa os atributos de filtragem"""
        atributo1 = Atributo.objects.create(
            user=self.user, name='API'
        )
        atributo2 = Atributo.objects.create(
            user=self.user, name='Pipeline'
        )
        montagem = Montagem.objects.create(
            titulo='Solucao Devops',
            tempo_execucao=500,
            preco=10,
            user=self.user
        )
        montagem.atributos.add(atributo1)

        res = self.client.get(ATRIBUTOS_URL, {'assigned_only': 1})

        serializer1 = AtributoSerializer(atributo1)
        serializer2 = AtributoSerializer(atributo2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_atributos_assigned_unique(self):
        """Testar atributos de filtragem"""
        atributo = Atributo.objects.create(user=self.user, name='Docker')
        Atributo.objects.create(user=self.user, name='AWS')
        montagem1 = Montagem.objects.create(
            titulo='Devops e cloud publica',
            tempo_execucao=300,
            preco=29.00,
            user=self.user
        )
        montagem1.atributos.add(atributo)
        montagem2 = Montagem.objects.create(
            titulo='Django framework iniciante',
            tempo_execucao=20,
            preco=5.00,
            user=self.user
        )
        montagem2.atributos.add(atributo)

        res = self.client.get(ATRIBUTOS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
