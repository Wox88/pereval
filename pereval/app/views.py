from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Added, Images


class Interaction(APIView):
    model = Added

    def post(self, request, *args, **kwargs):
        return self.submitData(request)

    def submitData(self, request):
        data = request.data
        images = data.get('images', [])
        required_fields = [
            'latitude', 'longitude', 'height', 'name',
            'user_name', 'user_email', 'user_phone'
        ]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return Response(
                {
                    'status': 400,
                    'message': f'Не хватает обязательных полей: {", ".join(missing_fields)}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval = Added.create_pereval(data, images)
            return Response(
                {
                    'status': 200,
                    'message': 'Отправлено успешно',
                    'id': pereval.id
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': 500,
                    'message': f'Ошибка при выполнении операции: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update_pereval_id(self, request, pk):
        field = request.data.get('field')
        new_field = request.data.get('new_field')

        if not field or new_field is None:
            return Response(
                {'state': 0, 'message': 'Необходимо указать поля "field" и "new_field"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            added = Added.objects.get(id=pk)
            status_added = added.status
            prohibited = ['user_name', 'user_phone', 'user_email']

            if status_added == 'new':
                if field not in prohibited:
                    setattr(added, field, new_field)
                    added.save()
                    return Response({'state': 1}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'state': 0, 'message': 'Данное поле изменить невозможно'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'state': 0, 'message': f'Статус объекта {pk} должен быть "new"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Added.DoesNotExist:
            return Response(
                {'state': 0, 'message': f'Объект {pk} не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'status': 500, 'message': f'Ошибка получения данных: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def get_date_email(self, email):
        added_objects = Added.objects.filter(user_email=email)
        if not added_objects.exists():
            return Response(
                {'status': 404, 'message': 'Пользователь с таким email не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        result = []
        for added in added_objects:
            list_of_images = [
                {'id': img.id, 'date_added': img.date_added, 'url': img.img.url if img.img else None}
                for img in added.images.all()
            ]
            result.append({
                'user_name': added.user_name,
                'latitude': added.latitude,
                'longitude': added.longitude,
                'height': added.height,
                'status': added.status,
                'images': list_of_images
            })

        first_added = added_objects.first()
        return Response({
            'user': first_added.user_name,
            'result': result
        }, status=status.HTTP_200_OK)