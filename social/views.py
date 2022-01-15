from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from .models import Post, Files, UserProfile
from django.template.loader import render_to_string
from .forms import PostForm
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        posts = Post.objects.all().order_by("-date_posted")
        context = {"posts": posts, "form": form}
        return render(request, 'social/post-list.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None, request.FILES or None)
        result = {}
        files = request.FILES.getlist('images')
        if is_ajax(request=request) and form.is_valid():
            post_obj = form.save(commit=False)
            post_obj.author = request.user
            post_obj.save()
            for file in files:
                new_img = Files(image=file)
                new_img.save()
                post_obj.images.add(new_img)
            post_obj.save()

            result['success'] = True

            return JsonResponse(result)
        else:
            result['success'] = False
            csrf_cxt = {}
            csrf_cxt.update(csrf(request))
            print("the form is not valid")
            formErrors = render_crispy_form(form, context=csrf_cxt)
            result['formErrors'] = formErrors
            return JsonResponse(result)
        context = {"form": form, }

        return render(request, 'social/post-create.html', context)


class PostCreateView(View):
    def get(self, request, post_identity, *args, **kwargs):
        form = PostForm()
        posts = Post.objects.all().order_by("-date_posted")
        context = {"posts": posts, "form": form}
        return render(request, 'social/post-create.html', context)

    def post(self, request, *args, **kwargs):
        result = dict()
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("form valid")
            print(request.FILES)
            result["success"] = True
            return JsonResponse(result)
        posts = Post.objects.all().order_by("-date_posted")
        context = {"posts": posts, "form": form}
        return render(request, 'social/post-create.html', context)


class UpdatePostView(LoginRequiredMixin, View):
    def get(self, request, post_slug, *args, **kwargs):
        if is_ajax(request=request):
            post = Post.objects.get(post_slug=post_slug)
            form = PostForm(instance=post)
            context = {"form": form, "post": post, }
            template = render_to_string(
                "social/getEditForm.html", context, request=request)
            return JsonResponse({"template": template, })

    def post(self, request, post_slug, *args, **kwargs):
        post = Post.objects.get(post_slug=post_slug)
        form = PostForm(request.POST or None,
                        request.FILES or None, instance=post)
        result = {}
        if is_ajax(request=request) and form.is_valid():
            form.save()
            print("the request is ajax and the form is valid")
            result["success"] = True
            return JsonResponse(result)
        else:
            print("the form is not valid at all")
            result['success'] = False
            csrf_cxt = {}
            csrf_cxt.update(csrf(request))
            print("the form is not valid")
            formErrors = render_crispy_form(form, context=csrf_cxt)
            result['formErrors'] = formErrors
            return JsonResponse(result)


class UserProfileView(View):
    def get(self, request, user_slug, *args, **kwargs):
        profile = get_object_or_404(UserProfile, profile_slug=user_slug)
        context = {"profile": profile, }
        return render(request, "landing/profile.html", context)


def JobsView(request):
    return render(request, 'landing/jobs.html')
