from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if not user:
            return render(request, 'user/signup.html')
        else:
            return redirect('/')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            #패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다.'})
            old_user = auth.get_user_model().objects.filter(username=username)
            if old_user:
                return render(request, 'user/signup.html', {'error': '이미 존재하는 사용자 이름입니다.'})
            else:
                UserModel.objects.create_user(
                    username=username,
                    password=password,
                    bio=bio
                )
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password) #authenticate 암호화된 비빌번호와 입력된 비밀번호가 맞는지 그리고 사용자와 맞는지 확인을 해준다.
        if me is not None:
            auth.login(request, me) #login은 Django가 user id를 session에 저장하게 해준다
            # return HttpResponse(f'{me.username} 로그인에 성공하셨습니다!')
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저이름 혹은 패스워드를 확인 해 주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if not user:
            return render(request, 'user/signin.html')
        else:
            return redirect('/')

@login_required #사용자가 로그인이 되어있어야만 작동할 수 있게끔 해준다.
def logout(request):
    auth.logout(request)
    #원래는 세션에서 확인을 하고 제거를 하는 복잡한 과정이 필요로 하지만 장고에서는
    #한번에 처리를 해준다.
    return redirect('/')

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')