# Create your views here.
from django.http import HttpResponse
from pprint import pprint
import logging
import hello.settings

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def index(request):
    log = logging.getLogger('debug')
    log.debug(__file__)
    user = getattr(request, 'user', None)
    io = StringIO()
    if user:
        pprint(user.is_authenticated(), io)
        io.write('\n date_joined={}, username={}, passwd={} \n'.format(user.date_joined, user.username, user.password))
    pprint(user, io)
    pprint(vars(hello.settings), io)
    return HttpResponse('<pre>' + io.getvalue() + '</pre>')

