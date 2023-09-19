from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import NewTopicForm
from .models import Board, Topic, Post
from django.views.generic import ListView, DetailView
from django.template import loader
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def home(request):
    boards = Board.objects.all()
    template = loader.get_template('home.html')
    
    return HttpResponse(template.render({
        'boards': boards
    }, request))

def board_topics(request, pk):
    try:
        board = Board.objects.get(id=pk)
    except Board.DoesNotExist:
        raise Http404
    template = loader.get_template('board_topics.html')
    context = {
        'board': board,
    }
    return HttpResponse(template.render(context, request))


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
                updated_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
