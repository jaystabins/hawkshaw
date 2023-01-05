from django.urls import path
from issues.views import (
    IssueCreateView,
    IssueDeleteView,
    IssueDetailView,
    IssueListView,
    IssueUpdateView,
)

app_name = "issues"

urlpatterns = [
    path("list/", IssueListView.as_view(), name="issue-list"),
    path("create/", IssueCreateView.as_view(), name="issue-create"),
    path("<pk>/delete/", IssueDeleteView.as_view(), name="issue-delete"),
    path("<pk>/edit/", IssueUpdateView.as_view(), name="issue-update"),
    path("<pk>/", IssueDetailView.as_view(), name="issue-detail"),
]
