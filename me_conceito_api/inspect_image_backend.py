import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
import django
django.setup()
from backend import settings
from api.models import CardNovidade
from api.serializers import CardNovidadeSerializer
field = CardNovidade._meta.get_field('imagem')
serializer_field = CardNovidadeSerializer().fields['imagem']
print('MEDIA_URL=', settings.MEDIA_URL)
print('MEDIA_ROOT=', settings.MEDIA_ROOT)
print('CardNovidade.imagem=', type(field).__name__, 'upload_to=', getattr(field, 'upload_to', None), 'blank=', field.blank, 'null=', field.null)
print('Serializer imagem=', type(serializer_field).__name__, 'use_url=', getattr(serializer_field, 'use_url', None), 'read_only=', serializer_field.read_only)
