from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Post
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
        response = {}
        if is_ajax(request=request) and form.is_valid():
            print("form images", form.cleaned_data.get('images'))
            title = form.cleaned_data.get("title", "")
            print("Title ", title)
            print(form)
            post_instance = form.save(commit=False)
            post_instance.author = request.user

            response["title"] = title
            response["success"] = True
            return JsonResponse(response)
        response["success"] = False
        cxt_csrf = {}
        cxt_csrf.update(csrf(request))
        formErrors = render_crispy_form(form, context=cxt_csrf)
        response["formErrors"] = formErrors
        return JsonResponse(response)


class PostEditView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None, request.FILES or None)
        if is_ajax(request=request) and form.is_valid():
            pass


def UserProfile(request):
    return render(request, "landing/profile.html")


def JobsView(request):
    return render(request, 'landing/jobs.html')
