from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from issues.forms import IssueForm
from issues.models import Issue
from projects.models import Project

from hawkshaw.utils.helpers import htmx_message_response


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/components/issue_table.html"
    context_object_name = "issues"

    class Meta:
        model = Issue

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get("projectPK"))


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
        return htmx_message_response(
            204,
            f"{form.cleaned_data.get('title')} Has Been Updated",
            "success",
            issue_list_updated=None,
            close_modal=None,
        )


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "issues/components/delete_confirm.html"

    class Meta:
        model = Issue

    def get_queryset(self):
        return Issue.objects.filter(pk=self.kwargs.get("pk"))

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return htmx_message_response(
            204,
            "Issue successfully deleted",
            "danger",
            issue_list_updated=None,
            close_modal=None,
        )


class IssueCreateView(LoginRequiredMixin, CreateView):
    form_class = IssueForm
    template_name = "issues/components/add_issue_form.html"

    class Meta:
        model = Issue

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs.get("projectPK"))
        form.save()
        return htmx_message_response(
            204, "Issue Created!", "success", close_modal=None, issue_list_updated=None
        )

    def get_context_data(self, **kwargs):
        context = {"project_id": self.kwargs.get("projectPK")}
        context["form"] = self.form_class()
        return context


def get_issue_count(request):
    count = Issue.objects.filter(user=request.user).count()
    return count
