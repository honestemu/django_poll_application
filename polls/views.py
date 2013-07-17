#Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

def index(request):
  latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
  return render_to_response('polls/index.html', {'latest_poll_list':latest_poll_list})

def detail(request, poll_id):
  p = get_object_or_404(Poll, pk=poll_id)
  return render_to_response('polls/details.html', {'poll': p},
                            context_instance=RequestContext(request))

def results(request, poll_id):
  p = get_object_or_404(Poll, pk=poll_id)
  return render_to_response('polls/results.html', {'poll': p})

def vote(request, poll_id):
  p =  get_object_or_404(Poll, pk=poll_id)#pk=primarykey
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    #Redisplay the poll voting form
    return render_to_response('polls/detail.html', 
                              {'poll':p, 'error_message': "You didn't select a choice,",},
			      context_instance=RequestContext(request))
  else:
    selected_choice.votes += 1
    select_choice.save()
    #Always Return an HttpResponseRedirect after successfully dealing with
    #POST data. This prevents data from being posted twice if the user hits
    #the back button.
    return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))