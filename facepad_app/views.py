from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from facepad_app import models
import datetime


# Create your views here.


def index(request):
    if request.method == "GET":
        if logged(request.COOKIES):
            return render(request, "portal.html", portal_context(request))
        else:
            return render(request, "login.html", {})
    else:
        raise Http404()


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {})
    elif request.method == "POST":
        try:
            user_name = request.POST["name"]
            user_password = request.POST["password"]
        except KeyError:
            return render(request, "login.html", {"error": "invalid user name or password"})
        try:
            user = models.SimpleUser.objects.get(name=user_name)
        except models.SimpleUser.DoesNotExist:
            return render(request, "login.html", {"error": "invalid user name or password"})

        if user.password == user_password:
            res = HttpResponseRedirect('/portal/')
            HttpResponse.set_cookie(res, "user_name", user_name)
            HttpResponse.set_cookie(res, "password", user_password)
            return res
        else:
            return render(request, "login.html", {"error": "invalid user name or password"})
    raise Http404()


def portal(request):
    if not logged(request.COOKIES):
        return render(request, "login.html", {})
    return render(request, "portal.html", portal_context(request))


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {})
    elif request.method == "POST":
        try:
            user_name = request.POST["name"]
            user_password = request.POST["password"]
            user_date = request.POST["date"]
        except KeyError:
            return render(request, "signup.html", {"error": "missing fields"})

        try:
            _ = models.SimpleUser.objects.get(name=user_name)
            return render(request, "signup.html", {"error": "this user already exists"})
        except models.SimpleUser.DoesNotExist:
            pass

        try:
            user_avatar = request.FILES["avatar"]
            try:
                user = models.SimpleUser.objects.create(name=user_name, password=user_password, date=user_date)
            except:
                return render(request, "signup.html", {"error": "Wrong date format"})
            user.avatar.save("avatar", user_avatar)
        except KeyError:
            try:
                user = models.SimpleUser.objects.create(name=user_name, password=user_password, date=user_date)
            except:
                return render(request, "signup.html", {"error": "Wrong date format"})
        user.save()
        res = HttpResponseRedirect('/portal/')
        HttpResponse.set_cookie(res, "user_name", user.name)
        HttpResponse.set_cookie(res, "password", user.password)
        return res


def like(request):
    if request.method == "POST":
        try:
            user_name = request.POST["name"]
            ltype = int(request.POST["type"])
            html = request.POST["html"]
            if ltype:
                post_id = request.POST["id"]
            else:
                comment_id = request.POST["id"]
        except KeyError:
            raise Http404()

        user = models.SimpleUser.objects.get(name=user_name)
        if ltype:
            liked_obj = models.Post.objects.get(id=post_id)
        else:
            liked_obj = models.Comment.objects.get(id=comment_id)

        for x in liked_obj.likes.all():
            if x.user.name == user_name:
                context = portal_context(request)
                context.update({"error": "already liked"})
                if 'portal' in html:
                    return HttpResponseRedirect('/portal/')
                elif 'section' in html:
                    return HttpResponseRedirect('/section/' + str(liked_obj.my_section()) + '/')
        if ltype:
            n_like = models.Likes.objects.create(user=user, post=liked_obj)
        else:
            n_like = models.Likes.objects.create(user=user, comment=liked_obj)

        liked_obj.likes.add(n_like)
        liked_obj.save()
        if 'portal' in html:
            return HttpResponseRedirect('/portal/')
        elif 'section' in html:
            return HttpResponseRedirect('/section/' + str(liked_obj.my_section()) + '/')


def comment(request):
    if request.method == 'POST':
        try:
            comm = request.POST['comment']
            post = request.POST['id']
            html = request.POST['html']
        except KeyError:
            raise Http404()
        post = models.Post.objects.get(id=post)
        user, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=user)
        comm = models.Comment.objects.create(content=comm, date=datetime.datetime.now(), user=user)
        comm.save()
        post.comments.add(comm)
        post.save()
        if 'portal' in html:
            return HttpResponseRedirect('/portal/')
        elif 'section' in html:
            return HttpResponseRedirect('/section/' + str(comm.my_section()) + '/')


def view_post(request, id):
    if request.method == 'GET':
        post = models.Section.objects.get(pk=id)
        context = portal_context(request)
        context.update({
            "section": post
        })
        return render(request, 'section.html', context)
    elif request.method == 'POST':
        sect = models.Section.objects.get(pk=id)
        name, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=name)
        try:
            content = request.POST['message']
        except KeyError:
            raise Http404()

        post = models.Post.objects.create(user=user, section=sect, content=content)
        post.save()

        return HttpResponseRedirect('/section/' + str(id) + '/')


def create_post(request):
    if request.method == 'GET':
        return render(request, 'post.html', {
        })
    elif request.method == 'POST':
        try:
            content = request.POST['content']
            section = request.POST['section']
            date = datetime.datetime.now()
        except KeyError:
            raise Http404()

        user, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=user)
        section = models.Section.objects.get(name=section)
        post = models.Post.objects.create(user=user, content=content, date=date, section=section)
        post.save()
        return HttpResponseRedirect('/view_post/' + str(post.id) + '/')


def add_friend(request):
    if request.method == 'GET':
        name, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=name)
        no_friends = []
        for u in models.SimpleUser.objects.all():
            if u not in user.friend.all() and u.id != user.id:
                no_friends.append(u)

        context = portal_context(request)
        context.update({
            'no_friends': no_friends
        })

        return render(request, 'addfriends.html', context)
    elif request.method == 'POST':
        name, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=name)
        try:
            u = request.POST['user']
        except KeyError:
            raise Http404()
        friend = models.SimpleUser.objects.get(pk=int(u))
        user.friend.add(friend)
        user.save()
        return HttpResponseRedirect('/add_friend/')


def message(request, id):
    if request.method == 'GET':
        user, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=user)
        rec_user = models.SimpleUser.objects.get(pk=id)
        sent = models.Message.objects.filter(senderUser__in=[user, rec_user], receiverUser__in=[user, rec_user])
        # rec = models.Message.object.filter(senderUser=rec_user, receiverUser=user)
        # res = list(sent) + list(rec)
        # res.sort(key=lambda x: x.date, reverse=True)
        context = portal_context(request)
        context.update({
            'message': sent,
            'friend': rec_user
        })
        return render(request, 'send_message.html', context)
    elif request.method == "POST":
        user, _ = logged(request.COOKIES)
        user = models.SimpleUser.objects.get(name=user)

        rec_user = models.SimpleUser.objects.get(pk=int(id))
        content = request.POST['message']
        mess = models.Message.objects.create(senderUser=user, receiverUser=rec_user, content=content,
                                             date=datetime.datetime.now())
        mess.save()
        return HttpResponseRedirect('/send_message/' + str(id) + '/')


def logged(cookies):
    try:
        user_name = cookies["user_name"]
        password = cookies["password"]
        return user_name, password
    except KeyError:
        return None


def portal_context(request, user_name=None):
    if not user_name:
        user_name, _ = logged(request.COOKIES)
    user = models.SimpleUser.objects.get(name=user_name)
    sections = models.Section.objects.all()
    posts = [x for x in models.Post.objects.filter(user=user)]
    for f in user.friend.all():
        posts += [x for x in models.Post.objects.filter(user=f)]
    posts.sort(key=lambda x: x.date, reverse=True)
    return {"user": user, "post": posts, "sections": sections}


def logout(request):
    if request.method == 'GET':
        user = logged(request.COOKIES)
        res = HttpResponseRedirect('/')
        if user:
            HttpResponse.delete_cookie(res, 'user_name')
            HttpResponse.delete_cookie(res, 'password')
        return res
