from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'www', settings.ROOT_URLCONF, name='www'),
                         host(r'birds', 'apps.birds.urls', name='birds'),
                         host(r'api', 'apps.API_VK.urls', name='API_VK'),
                         )