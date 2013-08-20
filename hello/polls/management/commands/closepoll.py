from django.core.management.base import BaseCommand, CommandError
from polls.models import Poll

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Close the specified polls for vote'

    def handle(self, *args, **kwargs):
        for poll_id in *args:
            try:
                poll = Poll.objects.get(pk=int(poll_id))
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)
            poll.opened = False
            poll.save()
            self.stdout.write('Successfully closed poll "%s"' % poll_id)
