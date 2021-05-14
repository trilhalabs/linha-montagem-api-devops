import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Montagem, Tag, Atributo

from montagem.serializers import MontagemSerializer, MontagemDetailSerializer


MONTAGENS_URL = reverse('montagem:montagem-list')


def image_upload_url(montagem_id):
    """URL de retorno para upload de imagem de linha de montagem"""
    return reverse('montagem:montagem-upload-image', args=[montagem_id])


def detail_url(montagem_id):
    """Retorna detalhes da URL da linha demontagemL"""
    return reverse('montagem:montagem-detail', args=[montagem_id])


def sample_tag(user, name='Main course'):
    """Cria e retorna uma tag simples"""
    return Tag.objects.create(user=user, name=name)


def sample_atributo(user, name='Docker'):
    """Criae retorna um atributo simples"""
    return Atributo.objects.create(user=user, name=name)


def sample_montagem(user, **params):
    """Cria e retorna uma linha demontagem simples"""
    defaults = {
        'titulo': 'Exemplo linha de montagem',
        'tempo_execucao': 10,
        'preco': 5.00
    }
    defaults.update(params)

    return Montagem.objects.create(user=user, **defaults)


class PublicMontagemApiTests(TestCase):
    """Teste o acesso nao autenticado a linha de montagem da API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(MONTAGENS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMontagemApiTests(TestCase):
    """Teste o acesso nao autenticado a linha de montagem da API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@tslabs.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_montagem(self):
        """Teste recuperando uma lista de linhas de montagem"""
        sample_montagem(user=self.user)
        sample_montagem(user=self.user)

        res = self.client.get(MONTAGENS_URL)

        montagens = Montagem.objects.all().order_by('-id')
        serializer = MontagemSerializer(montagens, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_montagens_limited_to_user(self):
        """Teste de recuperacao de linhas de montagem para o usuario"""
        user2 = get_user_model().objects.create_user(
            'other@tslabs.com',
            'password123'
        )
        sample_montagem(user=user2)
        sample_montagem(user=self.user)

        res = self.client.get(MONTAGENS_URL)

        montagens = Montagem.objects.filter(user=self.user)
        serializer = MontagemSerializer(montagens, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_montagem_detail(self):
        """Teste a visualizacao de um detalhe da linha de montagem"""
        montagem = sample_montagem(user=self.user)
        montagem.tags.add(sample_tag(user=self.user))
        montagem.atributos.add(sample_atributo(user=self.user))

        url = detail_url(montagem.id)
        res = self.client.get(url)

        serializer = MontagemDetailSerializer(montagem)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_montagem(self):
        """Testa a criacao d euma linha demontagem simples"""
        payload = {
            'titulo': 'Docker vs Vagrant',
            'tempo_execucao': 30,
            'preco': 5.00
        }
        res = self.client.post(MONTAGENS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        montagem = Montagem.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(montagem, key))

    def test_create_montagem_with_tags(self):
        """Teste de criacao de uma linha d emontagem com tags"""
        tag1 = sample_tag(user=self.user, name='Docker')
        tag2 = sample_tag(user=self.user, name='Vagrant')
        payload = {
            'titulo': 'Docker vs Vagrant',
            'tags': [tag1.id, tag2.id],
            'tempo_execucao': 60,
            'preco': 20.00
        }
        res = self.client.post(MONTAGENS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        montagem = Montagem.objects.get(id=res.data['id'])
        tags = montagem.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_montagem_with_atributos(self):
        """Teste de criacao de uma linha de montagem com atributos"""
        atributo1 = sample_atributo(user=self.user, name='Pipeline')
        atributo2 = sample_atributo(user=self.user, name='Cloud')
        payload = {
            'titulo': 'Devops e cloud',
            'atributos': [atributo1.id, atributo2.id],
            'tempo_execucao': 20,
            'preco': 70.00
        }
        res = self.client.post(MONTAGENS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        montagem = Montagem.objects.get(id=res.data['id'])
        atributos = montagem.atributos.all()
        self.assertEqual(atributos.count(), 2)
        self.assertIn(atributo1, atributos)
        self.assertIn(atributo2, atributos)

    def test_partial_update_montagem(self):
        """Teste a atualizacao de uma linha de montagem com patch"""
        montagem = sample_montagem(user=self.user)
        montagem.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Python')

        payload = {'titulo': 'Python com Django', 'tags': [new_tag.id]}
        url = detail_url(montagem.id)
        self.client.patch(url, payload)

        montagem.refresh_from_db()
        self.assertEqual(montagem.titulo, payload['titulo'])
        tags = montagem.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_montagem(self):
        """Teste a atualizacao de uma linha demontagem com put"""
        montagem = sample_montagem(user=self.user)
        montagem.tags.add(sample_tag(user=self.user))
        payload = {
            'titulo': 'Integracao continua',
            'tempo_execucao': 25,
            'preco': 5.00
        }
        url = detail_url(montagem.id)
        self.client.put(url, payload)

        montagem.refresh_from_db()
        self.assertEqual(montagem.titulo, payload['titulo'])
        self.assertEqual(montagem.tempo_execucao, payload['tempo_execucao'])
        self.assertEqual(montagem.preco, payload['preco'])
        tags = montagem.tags.all()
        self.assertEqual(len(tags), 0)


class MontagemImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@tslabs.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.montagem = sample_montagem(user=self.user)

    def tearDown(self):
        self.montagem.image.delete()

    def test_upload_image_to_montagem(self):
        """Teste o upload de um e-mail para a linha demontagem"""
        url = image_upload_url(self.montagem.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.montagem.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.montagem.image.path))

    def test_upload_image_bad_request(self):
        """Teste o upload de uma imagem invalida"""
        url = image_upload_url(self.montagem.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_montagens_by_tags(self):
        """Teste de montagemcom com tags especificas"""
        montagem1 = sample_montagem(user=self.user, titulo='Gitlab')
        montagem2 = sample_montagem(user=self.user, titulo='Github')
        tag1 = sample_tag(user=self.user, name='Repositorio')
        tag2 = sample_tag(user=self.user, name='CICD')
        montagem1.tags.add(tag1)
        montagem2.tags.add(tag2)
        montagem3 = sample_montagem(user=self.user, titulo='Mirroring Github')

        res = self.client.get(
            MONTAGENS_URL,
            {'tags': f'{tag1.id},{tag2.id}'}
        )

        serializer1 = MontagemSerializer(montagem1)
        serializer2 = MontagemSerializer(montagem2)
        serializer3 = MontagemSerializer(montagem3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_montagens_by_atributos(self):
        """Teste linhas de montagem de devolução com atributos especificos"""
        montagem1 = sample_montagem(user=self.user, titulo='API com java ')
        montagem2 = sample_montagem(user=self.user, titulo='Api com python')
        atributo1 = sample_atributo(user=self.user, name='Programacao')
        atributo2 = sample_atributo(user=self.user, name='Codigo')
        montagem1.atributos.add(atributo1)
        montagem2.atributos.add(atributo2)
        montagem3 = sample_montagem(user=self.user, titulo='Kubernets e pods')

        res = self.client.get(
            MONTAGENS_URL,
            {'atributos': f'{atributo1.id},{atributo2.id}'}
        )

        serializer1 = MontagemSerializer(montagem1)
        serializer2 = MontagemSerializer(montagem2)
        serializer3 = MontagemSerializer(montagem3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
