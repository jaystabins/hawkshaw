from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from issues.forms import IssueForm
from issues.models import Issue


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/components/issue_list.html"
    context_object_name = "issues"

    class Meta:
        model = Issue

    def get_queryset(self):
        return Issue.objects.filter(user=self.request.user)


class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = "issues/components/issue_detail.html"

    class Meta:
        model = Issue

    def get_queryset(self):
        return Issue.objects.filter(pk=self.kwargs.get("pk"))


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    form_class = IssueForm
    template_name = "issues/components/update_issue.html"

    class Meta:
        model = Issue

    def get_queryset(self):
        return Issue.objects.filter(pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.save()
        response = HttpResponse()
        response["HX-Trigger"] = "issue_list_updated"
        return response


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "issues/components/delete_confirm.html"

    class Meta:
        model = Issue

    def get_queryset(self):
        return Issue.objects.filter(pk=self.kwargs.get("pk"))

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        response = HttpResponse()
        response["HX-Trigger"] = "issue_list_updated"
        return response


class IssueCreateView(LoginRequiredMixin, CreateView):
    form_class = IssueForm
    template_name = "issues/components/add_issue_form.html"

    class Meta:
        model = Issue

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        response = HttpResponse()
        response["HX-Trigger"] = "issue_list_updated"
        return response


def get_issue_count(request):
    count = Issue.objects.filter(user=request.user).count()
    return count
