
from vnexpressAPI.methods import update_news, big_update_news
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Updates news data from VNExpress'

    def add_arguments(self, parser):
        parser.add_argument('type_update', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            if options['type_update'][0] == 'big':
                big_update_news()
                self.stdout.write(self.style.SUCCESS('Successfully updated news data from VNExpress'))
            elif options['type_update'][0] == 'small':
                update_news()
                self.stdout.write(self.style.SUCCESS('Successfully updated news data from VNExpress'))
            else:
                self.stdout.write(self.style.ERROR('Type update not supported'))
        except:
            raise CommandError('Update news data failed')
            
            