from django.core.management.base import BaseCommand, CommandError
from polls.models import Poll, Choice
from optparse import make_option
from django.utils import timezone

data = (
    {'poll': {'question': 'what is 1+1?', 'pub_date': timezone.now()},
     'choices': ({'choice_text': 'zero', 'votes': 1}, {'choice_text': 'one', 'votes': 2},
         {'choice_text': 'three', 'votes': 1}, {'choice_text': 'four', 'votes': 2},
     )
    },

    {'poll': {'question': 'which is the best cloud computing service provider?', 'pub_date': timezone.now()},
     'choices': ({'choice_text': 'Amozon', 'votes': 1}, {'choice_text': 'Google', 'votes': 2},
         {'choice_text': 'Sina', 'votes': 1}, {'choice_text': 'meituan', 'votes': 2},
     )
    },
)

class Command(BaseCommand):
    args = ''
    help = 'stuff some test data'

    def handle(self, *args, **options):
        for pc in data:
            p = Poll(**pc['poll'])
            p.save()
            self.stdout.write('saved Poll: {}'.format(p))
            for c in pc['choices']:
                c = Choice(**c)
                c.poll = p
                c.save()
                self.stdout.write('saved Choice: {}'.format(c), ending=',')
            self.stdout.write('')
        self.stdout.write('DONE')

