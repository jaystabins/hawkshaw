from django import forms
from issues.models import Issue


class IssueForm(forms.ModelForm):
    priority = forms.ChoiceField(choices=Issue.PRIORITY_CHOICES, initial=1)
    type = forms.ChoiceField(choices=Issue.TYPE_CHOICES, initial=1)
    status = forms.ChoiceField(choices=Issue.STATUS_CHOICES, initial=1)

    class Meta:
        model = Issue
        fields = ("title", "description", "priority", "type", "status")
