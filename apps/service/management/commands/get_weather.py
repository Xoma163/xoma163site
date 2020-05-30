import json

from django.core.management.base import BaseCommand

from apps.API_VK.APIs.yandex_weather import get_weather
from apps.service.models import City, Service


class Command(BaseCommand):

    def handle(self, *args, **options):
        city_name = options['city'][0]
        city = City.objects.get(name__icontains=city_name)
        weather_data = get_weather(city, False)
        weather_data_str = json.dumps(weather_data)

        entity_yesterday, _ = Service.objects.get_or_create(name=f'weatherchange_yesterday_{city.name}')
        entity_today, _ = Service.objects.get_or_create(name=f'weatherchange_today_{city.name}')
        entity_yesterday.value = entity_today.value
        entity_yesterday.save()
        entity_today.value = weather_data_str
        entity_today.save()

    def add_arguments(self, parser):
        parser.add_argument('city', nargs='+', type=str, help='city')
