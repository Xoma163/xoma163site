from django.core.management import BaseCommand

from apps.service.models import Meme, Horoscope

MEMES_COUNT = 12


class Command(BaseCommand):

    def handle(self, *args, **options):
        random_memes = Meme.objects.order_by('?')[:MEMES_COUNT]
        Horoscope.objects.all().delete()
        horoscope = Horoscope()
        horoscope.save()
        horoscope.memes.add(*random_memes)
        horoscope.save()
