from django.test import TestCase
from unittest.mock import Mock, patch
from rest_framework.request import Request
from .views import Interaction
from .models import Added, Images


class InteractionTestCase(TestCase):
    def setUp(self):
        self.pereval = Added.objects.create(
            name="Test Pass",
            latitude=43.0,
            longitude=42.0,
            height=3000,
            user_name="Ivan",
            user_email="ivan@test.com",
            user_phone="+79990000000",
            status='new'
        )

        Images.objects.create(pereval=self.pereval, img="image1.jpg")  # Исправлено здесь
        Images.objects.create(pereval=self.pereval, img="image2.jpg")  # Исправлено здесь

        self.pereval_closed = Added.objects.create(
            name="Closed Pass",
            latitude=44.0,
            longitude=43.0,
            height=2500,
            user_name="Petr",
            user_email="petr@test.com",
            user_phone="+79991111111",
            status='approved'
        )

    def test_update_pereval_id_success(self):
        request = Mock(spec=Request)
        request.data = {'field': 'name', 'new_field': 'New Name Updated'}

        view = Interaction()
        response = view.update_pereval_id(request, pk=self.pereval.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['state'], 1)

        self.pereval.refresh_from_db()
        self.assertEqual(self.pereval.name, 'New Name Updated')

    def test_update_pereval_id_forbidden_field(self):
        request = Mock(spec=Request)
        request.data = {'field': 'user_name', 'new_field': 'Hacker'}

        view = Interaction()
        response = view.update_pereval_id(request, pk=self.pereval.id)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['state'], 0)
        self.assertIn('невозможно', response.data['message'])

    def test_update_pereval_id_wrong_status(self):
        request = Mock(spec=Request)
        request.data = {'field': 'name', 'new_field': 'Should not update'}

        view = Interaction()
        response = view.update_pereval_id(request, pk=self.pereval_closed.id)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['state'], 0)
        self.assertIn('должен быть "new"', response.data['message'])

    def test_update_pereval_id_not_found(self):
        request = Mock(spec=Request)
        request.data = {'field': 'name', 'new_field': 'Test'}

        view = Interaction()
        response = view.update_pereval_id(request, pk=9999)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['state'], 0)

    def test_get_date_email_found(self):
        view = Interaction()
        response = view.get_date_email('ivan@test.com')

        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user'], 'Ivan')

        result_list = response.data['result']
        self.assertTrue(len(result_list) >= 1)

        first_item = result_list[0]
        self.assertEqual(first_item['user_name'], 'Ivan')
        self.assertEqual(len(first_item['images']), 2)

    def test_get_date_email_not_found(self):
        view = Interaction()
        response = view.get_date_email('nonexistent@test.com')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['status'], 404)

    @patch('app.views.Added')
    def test_submit_data(self, mock_added_class):
        request = Mock(spec=Request)
        request.data = {
            "latitude": 43.3521,
            "longitude": 42.4789,
            "height": 2850,
            "name": "Перевал Северный",
            "user_name": "Иван Петров",
            "user_email": "ivan.petrov@example.com",
            "user_phone": "+79991234567",
            "images": []
        }

        view = Interaction()

        mock_instance = Mock()
        mock_instance.id = 123
        mock_added_class.create_pereval.return_value = mock_instance

        result = view.post(request)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data['id'], 123)
        mock_added_class.create_pereval.assert_called_once()