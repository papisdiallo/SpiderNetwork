from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import edit
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from .models import Post, Files, UserProfile, Comment
from django.template.loader import render_to_string
from .forms import PostForm, CommentPostForm, UserProfileForm
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.core import serializers
import json


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        commentForm = CommentPostForm()
        posts = Post.objects.all().order_by("-date_posted")
        context = {"posts": posts, "form": form, "commentForm": commentForm}
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


class PostDeleteView(View):
    def post(self, request, post_slug, *args, **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
        if is_ajax(request=request):
            print("the request is ajax and the post should be deleted")
            post.delete()
            return JsonResponse({"success": True})


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
        files = request.FILES.getlist("images")

        if is_ajax(request=request) and form.is_valid():

            post_obj = form.save()
            Files.objects.filter(post=post).delete()
            post.images.clear()  # clearing all the old instances
            for img in files:
                img = Files(image=img)
                img.save()
                post.images.add(img)
            post_obj.save()

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


class DetailPostView(View):
    def get(self, request, post_slug, *args, **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
        context = {"post": post, }
        return render(request, "social/post-detail.html", context)

    def post(self, request, post_slug, *args, **kwargs):
        pass
        # the post will be about the comment on this post or images
        # of the post itself


class UserProfileView(View):
    def get(self, request, user_slug, *args, **kwargs):
        form = UserProfileForm()
        profile = get_object_or_404(UserProfile, profile_slug=user_slug)
        current_user = request.user
        posts = Post.objects.filter(author__profile__profile_slug=user_slug)
        # We have different state depending on who is looking to the profile and the
        # relationship that they do have with the owner of the profile
        # first case the user is looking to his own profile
        is_profile_owner = True  # just a default value
        if profile.user == current_user:
            is_profile_owner = True
        else:  # that means the user is looking to another user profile
            pass
        context = {"profile": profile, "posts": posts, "form": form}
        return render(request, "landing/profile.html", context)


def JobsView(request):
    return render(request, 'landing/jobs.html')


class CreateCommentPostView(View):
    def post(self, request, post_slug, *args, **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
        form = CommentPostForm(request.POST or None)
        if is_ajax(request=request) and form.is_valid():
            comment_post = form.save(commit=False)
            comment_post.author = request.user
            comment_post.post = post
            # comment_post.save()
            jsonInstance = serializers.serialize(
                "json",
                [
                    comment_post,
                ],
                use_natural_foreign_keys=True,  # I don't use one for now
            )
            result = {}
            result["success"] = True
            result["comment_obj"] = jsonInstance
            result["imageUrl"] = comment_post.author.profile.avatar.url
            result["comment_pk"] = comment_post.pk
            return JsonResponse(result)
        result = {"success": False}
        return JsonResponse(result)


class DeleteCommentPostView(View):
    def post(self, request, comment_id, *args, **kwargs):
        if is_ajax(request=request):
            print("the request is ajax and this post should be deleted")
            comment = get_object_or_404(Comment, id=comment_id)
            post_slug = comment.post.post_slug
            comment.delete()
        return JsonResponse({"success": True, "post_slug": post_slug, })


class AddRemovePostLikes(View):
    def post(self, request, post_or_comment_slug, *args, **kwargs):
        if is_ajax(request=request):
            liked_a = request.POST.get("liked_a")
            print(liked_a)
            is_liked = None
            if liked_a == "comment":
                comment = get_object_or_404(
                    Comment, comment_slug=post_or_comment_slug)
                is_liked = comment.likes.filter(
                    username=request.user.username).exists()
                if not is_liked:
                    comment.likes.add(request.user)
                    comment.save()  # do not thing this step is necessary though
                else:
                    comment.likes.remove(request.user)
                    comment.save()
            else:
                post = get_object_or_404(Post, post_slug=post_or_comment_slug)
                is_liked = post.likes.filter(
                    username=request.user.username).exists()
                if not is_liked:
                    post.likes.add(request.user)
                    post.save()
                else:
                    post.likes.remove(request.user)
                    post.save()
            if request.user == post.author:
                return JsonResponse({"is_liked": "Not accepted"})
            return JsonResponse({"is_liked": is_liked})
