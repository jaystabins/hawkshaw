from django.shortcuts import render
from projects.models import Project
from projects.forms import ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin
from hawkshaw.utils.helpers import htmx_message_response
from issues.models import Issue
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)


def project_dashboard(request):
    project_list = Project.objects.filter(pk=request.user.id)
    context = {"project_list": project_list}
    return render(request, "pages/projects.html", context)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/components/add_project.html"

    class Meta:
        model = Project

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return htmx_message_response(
            204,
            f"{form.cleaned_data.get('title')} Created!",
            "success",
            project_list_updated=None,
            close_modal=None,
        )


class ProjectTableView(LoginRequiredMixin, ListView):
    template_name = "projects/components/project_table.html"
    context_object_name = "project_list"

    class Meta:
        model = Project

    def get_queryset(self):
        return Project.objects.filter(user_id=self.request.user.id)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    class Meta:
        model = Project

    def get_queryset(self):
        return Project.objects.filter(pk=self.kwargs.get("pk"))


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "projects/components/project_delete.html"

    class Meta:
        model = Project

    def get_queryset(self):
        return Project.objects.filter(pk=self.kwargs.get("pk"))

    def delete(self, request, *args, **kwargs):
        name = Project.objects.get(pk=self.kwargs.get("pk")).title
        self.get_object().delete()
        return htmx_message_response(
            204,
            f"{name} has been deleted",
            "success",
            project_list_updated=None,
            close_modal=None,
        )


class IssueCardView(LoginRequiredMixin, DetailView):
    template_name = "issues/components/issue_project_cards.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context["issue_count"] = project.issues.count()
        context["bug_count"] = project.issues.filter(type=1).count()
        context["feature_count"] = project.issues.filter(type=2).count()
        return context
