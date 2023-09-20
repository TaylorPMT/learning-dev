from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import NewTopicForm
from django.db.models import Count
from .models import Board, Topic, Post
from django.views.generic import ListView, DetailView
from django.template import loader
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.views.generic import View

#

from django.utils import timezone
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator

# Create your views here.
# def home(request):
#     boards = Board.objects.all()
#     template = loader.get_template('home.html')
    
#     return HttpResponse(template.render({
#         'boards': boards
#     }, request))
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name='home.html'

def board_topics(request, pk):
    try:
        board = Board.objects.get(id=pk)
    except Board.DoesNotExist:
        raise Http404
    template = loader.get_template('board_topics.html')
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))
    context = {
        'board': board,
        'topics': topics,
    }
    return HttpResponse(template.render(context, request))

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user # User.objects.first()  # TODO: get the currently logged in user
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


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.updated_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})    


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
