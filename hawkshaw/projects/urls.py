from django.urls import path
from projects.views import (
    project_dashboard,
    ProjectCreateView,
    ProjectTableView,
    ProjectDetailView,
    ProjectDeleteView,
    IssueCardView,
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
