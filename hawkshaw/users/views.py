from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.http import HttpResponse
import json
from django.shortcuts import render
from users.forms import UserUploadImageForm
from hawkshaw.utils.helpers import htmx_message_response

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = [
        "name",
        "bio",
        "company",
        "location",
        "show_primary_email",
        "website",
    ]
    success_message = _("Information successfully updated")
    template_name = "users/components/update_profile.html"

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return htmx_message_response(
            204,
            "Information successfully updated.",
            "success",
            profile_updated=None,
            close_modal=None,
        )


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def get_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, "users/components/profile_card.html", {"object": user})


def get_profile_image(request):
    avatar = User.objects.get(pk=request.user.id).avatar
    context = {"avatar": avatar}
    return render(request, "users/components/small_profile_image.html", context)


class UserUpdateImageView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserUploadImageForm
    template_name = "users/components/update_profile_image.html"

    class Meta:
        model = User

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        old_avatar = User.objects.get(pk=self.get_object().pk).avatar
        old_cover = User.objects.get(pk=self.get_object().pk).cover_img
        if old_avatar and old_avatar != form.cleaned_data["avatar"]:
            old_avatar.delete(save=False)
        if old_cover and old_cover != form.cleaned_data["cover_img"]:
            old_cover.delete(save=False)
        print(old_avatar)
        form.save()
        return htmx_message_response(
            204,
            "Images successfully updated.",
            "success",
            profile_updated=None,
            close_modal=None,
        )


user_update_image_view = UserUpdateImageView.as_view()
