from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice, Voter
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(open_poll=True, pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
class ClosedView(generic.ListView):
    template_name = 'polls/closed.html'
    context_object_name = 'latest_closed_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(open_poll=False, pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#@login_required
def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Voter.objects.filter(poll_id=question_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "Sorry, but you've already voted."})
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        v = Voter(user=request.user, poll=question)
        v.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    

