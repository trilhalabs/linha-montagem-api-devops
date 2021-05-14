from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Montagem

from montagem.serializers import TagSerializer


TAGS_URL = reverse('montagem:tag-list')


class PublicTagsApiTests(TestCase):
    """Teste a API de tags disponiveis publicamente"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Teste se o login eh necessario para recuperar tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Teste a API de tags de usuario autorizado"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@tslabs.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Teste de recuperacao de tags"""
        Tag.objects.create(user=self.user, name='Docker')
        Tag.objects.create(user=self.user, name='Container')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Teste se as tags retornadas sao para o usuario autenticado"""
        user2 = get_user_model().objects.create_user(
            'other@tslabs.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Programacao')
        tag = Tag.objects.create(user=self.user, name='Pipelina')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Teste de criacao de uma nova tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Teste a criacao de uma nova tag com carga util invalida"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_montagens(self):
        """Teste as tags filtradas"""
        tag1 = Tag.objects.create(user=self.user, name='Docker')
        tag2 = Tag.objects.create(user=self.user, name='CICD')
        montagem = Montagem.objects.create(
            titulo='Integracao continua',
            tempo_execucao=10,
            preco=5.00,
            user=self.user
        )
        montagem.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Teste as tags filtradas"""
        tag = Tag.objects.create(user=self.user, name='CICD')
        Tag.objects.create(user=self.user, name='Pipeline')
        montagem1 = Montagem.objects.create(
            titulo='Deploy continuo',
            tempo_execucao=5,
            preco=3.00,
            user=self.user
        )
        montagem1.tags.add(tag)
        montagem2 = Montagem.objects.create(
            titulo='Devops e integracao continua',
            tempo_execucao=3,
            preco=2.00,
            user=self.user
        )
        montagem2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
