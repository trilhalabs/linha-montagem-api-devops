from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@tslabs.com', password='testpass'):
    """Cria um usuario simples"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Teste sucesso na criacao d eum usuario com email"""
        email = 'test@tslabs.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Teste se o e-mail foi convertido para minusculas"""
        email = 'test@TSLABS.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Teste se eh gerado erro para novo usuario"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Teste de criacao de um novo superuser"""
        user = get_user_model().objects.create_superuser(
            'test@tslabs.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Docker'
        )

        self.assertEqual(str(tag), tag.name)

    def test_atributos_str(self):
        """Test the attribute string respresentation"""
        atributo = models.Atributo.objects.create(
            user=sample_user(),
            name='Linguagens programacao'
        )

        self.assertEqual(str(atributo), atributo.name)

    def test_montagem_str(self):
        """Testa a reperesentacao da string de montagem"""
        montagem = models.Montagem.objects.create(
            user=sample_user(),
            titulo='Desenvolvendo uma solucao com Docker',
            tempo_execucao=5,
            preco=5.00
        )

        self.assertEqual(str(montagem), montagem.titulo)

    @patch('uuid.uuid4')
    def test_montagem_file_name_uuid(self, mock_uuid):
        """Teste se a imagem eh salva na localizacao correta"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.montagem_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/montagem/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
