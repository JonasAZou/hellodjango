from django.core.management.base import BaseCommand, CommandError
from polls.models import Poll
from optparse import make_option

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Close the specified polls for vote'
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it'),
    )

    def handle(self, *args, **options):
        for poll_id in args:
            try:
                poll = Poll.objects.get(pk=int(poll_id))
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)
            if options['delete']:
                poll.delete()
                self.stdout.write('Successfully deleted poll "%s"' % poll_id)
            else:
                poll.opened = False
                poll.save()
                self.stdout.write('Successfully closed poll "%s"' % poll_id)
