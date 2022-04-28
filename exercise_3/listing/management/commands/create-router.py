from django.core.management.base import BaseCommand, CommandError
from listing.models import Router
import string, random
class Command(BaseCommand):
    help = 'creates router for specified number'

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='+', type=int)

    def handle(self, *args, **options):
        for i in range(options['n'][0]):
            mac_address = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))
            loopback = "127.%s.%s.%s" % (random.randint(0, 255), random.randint(0, 255),random.randint(1, 254))
            hostname = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 14)))
            sap_id = "%s/%s/%s:1" % (random.randint(1, 9), random.randint(1, 9),random.randint(1, 12))
            Router.objects.create(sap_id=sap_id,hostname=hostname,loopback=loopback,mac_address=mac_address)

        self.stdout.write(self.style.SUCCESS('Successfully created %s samples"' % options['n'][0]))