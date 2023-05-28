from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice, Voter
from django.utils import timezone
from .forms import RequestForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User

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
    
def request_poll(request):
    if request.method == 'POST':
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        form = RequestForm(request.POST)
        if form.is_valid():
            #enter what you want the form to do
            subject = "requested poll"
            from_email = "champloosixsix@gmail.com"
            message = '''
            From:\t{}\n
            Question:\t{}\n
            Option1:\t{}\n
            Option2:\t{}\n
            Option3:\t{}\n
            '''.format(username,form.cleaned_data['request_question'], form.cleaned_data['answer_option1'], form.cleaned_data['answer_option2'], form.cleaned_data['answer_option3'])
            try:
                send_mail(subject, message, from_email, ["champloosixsix@gmail.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return HttpResponseRedirect('/')
    else:
        form = RequestForm()

    return render(request, 'polls/request.html', {'form': form})
    
    

