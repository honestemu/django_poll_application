#Create your views here.
from django.shortcuts import render, get_object_or_404
from polls.models import Poll, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

#def index(request):
#  latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#  context = {'latest_poll_list':latest_poll_list}
#  return render(request, 'polls/index.html',context)
#
#def detail(request, poll_id):
#  poll = get_object_or_404(Poll, pk=poll_id)
#  return render(request, 'polls/details.html', {'poll': poll})
#
#def results(request, poll_id):
#  poll = get_object_or_404(Poll, pk=poll_id)
#  return render(request, 'polls/results.html', {'poll': poll})
class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_poll_list'

  def get_queryset(self):
    """
    Return the last five published polls (not including those
    set to be published in the future).
    """
    return Poll.objects.filter(
      pub_date__lte=timezone.now()#less than or equal to(lte) now.
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Poll
  template_name = 'polls/details.html'
  def get_queryset(self):
    """
    Excludes any polls that aren't published yet.
    """
    return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Poll
  template_name = "polls/results.html"

def vote(request, poll_id):
  p =  get_object_or_404(Poll, pk=poll_id)#pk=primarykey
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    #Redisplay the poll voting form
    return render(request,
                  'polls/detail.html',
		  {'poll':p, 'error_message': "You didn't select a choice."})
  else:
    selected_choice.votes += 1
    selected_choice.save()
    #Always Return an HttpResponseRedirect after successfully dealing with
    #POST data. This prevents data from being posted twice if the user hits
    #the back button.
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
