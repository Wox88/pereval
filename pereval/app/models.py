from django.db import models
import os


def image_upload_path(instance, filename):
    return os.path.join('images', f'pereval_{instance.pereval.id}', filename)

class Added(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    height = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'Новый'),
            ('pending', 'В работе'),
            ('accepted', 'Принят'),
            ('rejected', 'Отклонён'),
        ],
        default='new'
    )

    class Meta:
        db_table = 'pereval_added'


    @classmethod
    def create_pereval(cls, raw_data, images=None):
        if images is None:
            images = []

        pereval = cls.objects.create(
            latitude=raw_data.get('latitude'),
            longitude=raw_data.get('longitude'),
            height=raw_data.get('height'),
            name=raw_data.get('name'),
            user_name=raw_data.get('user_name'),
            user_email=raw_data.get('user_email'),
            user_phone=raw_data.get('user_phone'),
            status='new'
        )

        for img_data in images:
            Images.objects.create(pereval=pereval, img=img_data)

        return pereval


    @classmethod
    def update_pereval(cls, pereval_id, new_status):
        choices = ['pending', 'accepted', 'rejected']
        if new_status not in choices:
            raise ValueError('Неверный статус')
        cls.objects.filter(id=pereval_id).update(status=new_status)
        return 'Статус обновлен'


    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

class Areas(models.Model):
    title = models.CharField(max_length=100)
    id_parent = models.BigIntegerField()

    class Meta:
        db_table = 'pereval_areas'


class Images(models.Model):
    pereval = models.ForeignKey(Added, on_delete=models.CASCADE, related_name='images')
    date_added = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    class Meta:
        db_table = 'pereval_images'


class ActivitiesTypes(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'spr_activities_types'