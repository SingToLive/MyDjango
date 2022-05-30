from django.shortcuts import render, redirect
from .models import Tweet, TweetComment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

# Create your views here.
def home(request):
    user = request.user.is_authenticated #사용자가 로그인 되어있는지 확인
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = Tweet.objects.all().order_by('created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')
        if content == '':
            all_tweet = Tweet.objects.all().order_by('created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet, 'error':'글은 공백일 수 없습니다.'})
        else:
            my_tweet = Tweet.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':  # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
        return redirect('/tweet')

@login_required
def delete_tweet(request, id):
    my_tweet = Tweet.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def tweet_detail(request, id):
    if request.method == 'GET':
        my_tweet = Tweet.objects.get(id=id)
        comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
        return render(request, 'tweet/tweet_detail.html', {'comment':comment, 'tweet': my_tweet})

@login_required
def tweet_comment_write(request, id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        tweet_id = Tweet.objects.get(id=id)
        tc = TweetComment()
        tc.tweet = tweet_id
        tc.author = request.user
        tc.comment = comment
        tc.save()

        return redirect('/tweet/'+str(id))

@login_required
def tweet_comment_delete(request, id):
    comment_id = TweetComment.objects.get(id=id)
    print(comment_id)
    current_tweet = comment_id.tweet.id
    comment_id.delete()
    return redirect('/tweet/'+str(current_tweet))

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = Tweet

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context