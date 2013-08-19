# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from .models import Poll, Choice


def index(request):
    ''' long version
    polls = Poll.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {'latest_poll_list': polls})
    return HttpResponse(template.render(context))
    '''
    polls = Poll.objects.order_by('-pub_date')[:5]
    context = {'latest_poll_list': polls}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll': poll})

def result(requst, poll_id):
    return HttpResponse('result of poll {}'.format(poll_id))

def vote(request, poll_id):
    return HttpResponse('voted for poll {}'.format(poll_id))

