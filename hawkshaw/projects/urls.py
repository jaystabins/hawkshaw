from django.urls import path
from projects.views import (
    IssueCardView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectTableView,
    project_dashboard,
)

app_name = "projects"

urlpatterns = [
    path("", project_dashboard, name="dashboard"),
    path("add_project/", ProjectCreateView.as_view(), name="project-add"),
    path("project_table/", ProjectTableView.as_view(), name="project-table"),
    path("<pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
    path("<pk>/issueCardView", IssueCardView.as_view(), name="issue-card"),
]
