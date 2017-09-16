from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Interest, Subject, GRADE_CHOICES, Target, Course

class CourseSearchForm(forms.Form):
    ''' This defines the form used to receive user input to search for a course by keywords.
            keywords is a field defining the keywords to be searched for matches. '''
    keywords = forms.CharField(label='Search keywords',
                               max_length=50,)

class SignUpForm(UserCreationForm):
    ''' This defines the form used to receive user input to create an account and fill in details. 
            The form saves the data into the Django User model.
            username is a field defining the username of the user and is the primary key of the User model.
            first_name is a field defining the first name of the user.
            email is a field defining the email of the user.
            password1 and password2 are fields defining the password of the user. Both fields need to match. '''
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

class InterestForm(forms.Form):
    ''' This defines the form used to receive user input to select interests for a user.
            interests is a field used to select multiple Interest model instances. '''
    interests = forms.MultipleChoiceField(
        choices=Interest.objects.all().order_by('name').values_list('id', 'name'),
        widget=forms.CheckboxSelectMultiple
    )

class GradesForm(forms.Form):
    ''' This defines the form used to receive user input to enter subjects taken by a user and the respective
            grade scored.
            subject is a field used to select a Subject model instance.
            grade is a field used to select the grade scored, limited to the GRADE_CHOICES tuple. '''
    subject = forms.ModelChoiceField(queryset=Subject.objects.all().order_by('name'))
    grade = forms.ChoiceField(choices=GRADE_CHOICES)

class BaseGradesFormSet(BaseFormSet):
    ''' This defines the formset used to render multiple GradesForm forms.
            It ensures that both subject and grade fields must be selected for each GradesForm form and that the same
            Subject model instance cannot be selected across multiple GradesForm forms. '''
    def clean(self):
        if any(self.errors):
            return self.errors
        subjects = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                subject = form.cleaned_data['subject']
                grade = form.cleaned_data['grade']
                if subject and grade:
                    if subject in subjects:
                        duplicates = True
                    subjects.append(subject)
                if duplicates:
                    raise forms.ValidationError(
                        'The same subject cannot be entered twice.',
                        code='duplicate_subjects'
                    )
                if (subject and not grade) or (grade and not subject):
                    raise forms.ValidationError(
                        'Both fields must be entered.',
                        code='missing_field'
                    )


class TargetForm(forms.Form):
    ''' This defines the form used to receive user input to select target courses of a user.
            course is a field used to select a Course model instance.
            rank is a field used to select the rank of this course and is ranges from 1 to the current number of target
            courses the user has, plus one. '''
    course = forms.ModelChoiceField(queryset=Course.objects.all().order_by('name'))
    rank = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TargetForm, self).__init__(*args, **kwargs)
        self.fields['rank'].choices = [
            (i,i) for i in range(1, (Target.objects.filter(profile=self.request.user.profile).count())+2)
        ]

class BaseTargetFormSet(BaseFormSet):
    ''' This defines the formset used to render multiple TargetForm forms.
            It ensures that both course and rank fields must be selected for each GradesForm form and that across
            multiple GradesForm forms, course and rank must be unique. '''
    def clean(self):
        if any(self.errors):
            return self.errors
        courses = []
        ranks = []
        duplicate_course = False
        duplicate_rank = False
        for form in self.forms:
            if form.cleaned_data:
                course = form.cleaned_data['course']
                rank = form.cleaned_data['rank']
                if course and rank:
                    if course in courses:
                        duplicate_course = True
                    courses.append(course)
                    if rank in ranks:
                        duplicate_rank = True
                    ranks.append(rank)
                if duplicate_course:
                    raise forms.ValidationError(
                        'The same course cannot be selected twice.',
                        code='duplicate_course'
                    )
                if duplicate_rank:
                    raise forms.ValidationError(
                        'Target courses cannot have the same rank.',
                        code='duplicate_rank'
                    )
                if (course and not rank) or (rank and not course):
                    raise forms.ValidationError(
                        'Both fields must be entered.',
                        code='missing_field'
                    )