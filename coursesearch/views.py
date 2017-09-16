from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from functools import reduce
from . import l1r4_calculator, recommend_system
from .forms import CourseSearchForm, SignUpForm, InterestForm, GradesForm, BaseGradesFormSet, TargetForm, BaseTargetFormSet
from .models import Course, Grade, Target, Interest

def course_search(request):
    ''' This function defines the main html page rendered, which depends on whether the user is logged in or not. '''
    form = CourseSearchForm()
    if request.user.is_authenticated:
        return render(request, 'coursesearch/search_base.html',{'form':form})
    else:
        return render(request, 'coursesearch/main_public.html')

def keyword_search(request):
    ''' This function defines the html page for search results after searching for courses by keywords.
            It checks that each search keyword, separated by space, has at least 3 characters.
            It searches for all Course model objects whose name, description, or category matches every keyword and
            returns the search results. '''
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        if not search_query or search_query.isspace():
            return redirect("/")
        search_keyword = search_query.split()
        for kw in search_keyword:
            if (len(kw)<3):
                messages.info(request, 'Each keyword should have at least 3 characters.')
                return redirect("/")
        import operator
        courses = Course.objects.filter(reduce(operator.and_, [Q(name__icontains=kw) | Q(description__icontains=kw) | Q(category__icontains=kw) for kw in search_keyword]))
        if courses.exists():
            messages.info(request, 'Search results for "' + search_query + '"')
            return render(request, 'coursesearch/search_results.html', {'courses': courses})
        else:
            messages.info(request, 'Zero search results found.')
            return redirect("/")
    

def cat_search(request,cat):
    ''' This function defines the html page for search results after searching for courses by category.
            It searches for all Course model objects that match the category and returns the search results. '''
    courses = Course.objects.filter(category=cat)
    if courses.exists():
        messages.info(request, 'Search results for ' + courses[0].get_category_display() + ' category')
        return render(request, 'coursesearch/search_results.html', {'courses': courses})
    else:
        messages.info(request, 'Zero search results found.')
        return redirect("/")

def school_search(request,sch):
    ''' This function defines the html page for search results after searching for courses by school.
            It searches for all Course model objects that match the school and returns the search results. '''
    courses = Course.objects.filter(school=sch)
    if courses.exists():
        messages.info(request, 'Search results for ' + courses[0].get_school_display())
        return render(request, 'coursesearch/search_results.html', {'courses': courses})
    else:
        messages.info(request, 'Zero search results found.')
        return redirect("/")

def logout_view(request):
    ''' This function log outs the user and redirects the user to the main page. '''
    logout(request)
    return redirect("/")

def signup(request):
    ''' This function renders the html page to allow a user to sign up and create a new account by rendering a
            SignUpForm form.
            After checking that the form is valid, the data retrieved from the form is used to create
            a new User model instance. '''
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile/edit')
    else:
            form = SignUpForm()
    return render(request, 'coursesearch/signup.html',{'form': form})

def profile_edit(request):
    ''' This function renders the html page to allow a user to edit their profile by rendering the
            BaseGradesFormSet formset and InterestForm form.
            After checking that the forms are valid, the data retrieved is used to create new Grade and Interest model
            instances, which are linked to the Profile of the user. '''
    user = request.user
    GradesFormSet = formset_factory(GradesForm, formset=BaseGradesFormSet)
    grades = Grade.objects.filter(profile=user.profile).order_by('subject__name')
    grades_dict = [{'subject': g.subject, 'grade':g.grade} for g in grades]
    if request.method == 'POST':
        interest_form = InterestForm(request.POST)
        grades_formset = GradesFormSet(request.POST)
        try:
            if interest_form.is_valid() and grades_formset.is_valid():
                user.profile.interests = interest_form.cleaned_data.get('interests')
                user.profile.save()
                new_grades = []
                for grades_form in grades_formset:
                    subject = grades_form.cleaned_data.get('subject')
                    grade = grades_form.cleaned_data.get('grade')
                    if subject and grade:
                        new_grades.append(Grade(subject=subject, grade=grade, profile=user.profile))
                try:
                    with transaction.atomic():
                        Grade.objects.filter(profile=user.profile).delete()
                        Grade.objects.bulk_create(new_grades)
                        user.profile.l1r4_A = l1r4_calculator.calcL1R4(user.profile, 'a')
                        user.profile.l1r4_B = l1r4_calculator.calcL1R4(user.profile, 'b')
                        user.profile.l1r4_C = l1r4_calculator.calcL1R4(user.profile, 'c')
                        user.profile.l1r4_D = l1r4_calculator.calcL1R4(user.profile, 'd')
                        user.profile.save()
                        messages.success(request,'Your user profile has been successfully updated.')
                        return redirect("/profile/view/")
                except IntegrityError:
                    messages.error(request,'An error occurred while saving your user profile.')
                    return redirect(reverse('profile_view'))
        except ValidationError as e:
            messages.error(request, e.message)
            pass

    else:
        interest_form = InterestForm()
        grades_formset = GradesFormSet(initial=grades_dict)
    return render(request,'coursesearch/profile_edit.html',{
        'interest_form': interest_form, 'grades_formset': grades_formset
    })

def profile_view(request):
    ''' This function renders the html page to allow the user to view their profile.
            It displays the interests, target courses, and grades of the user. '''
    interests = Interest.objects.filter(profile=request.user.profile).order_by('name')
    targets = Target.objects.filter(profile=request.user.profile).order_by('rank')
    grades = Grade.objects.filter(profile=request.user.profile).order_by('subject__name')
    return render(request,'coursesearch/profile_view.html', {'interests': interests, 'targets': targets, 'grades': grades})

def profile_recommend(request):
    ''' This function renders the html page to display the courses recommended to the user.
            It calls the recommend_system module and displays a list of recommended courses based on the user's profile. '''
    reclist = recommend_system.recommend(request.user.profile, 5, 0.5)
    if reclist:
        recs = Course.objects.filter(code__in=reclist).order_by('cutoff')
        return render(request,'coursesearch/profile_recommend.html', {'recs': recs, 'reclist':reclist})
    else:
        messages.info(request, 'Sorry, no courses could be recommended at this point. :(')
        return redirect('/')

def profile_add_target(request,code):
    ''' This function renders the html page to allow the user to add a new target course to their profile by
            rendering a BaseTargetFormSet formset.
            After checking that the form is valid, the data retrieved is used to create new Target model instances,
            which are linked to the Profile of the user. '''
    user = request.user
    TargetFormSet = formset_factory(TargetForm, formset=BaseTargetFormSet)
    targets = Target.objects.filter(profile=user.profile).order_by('rank')
    targets_dict = [{'course': t.course, 'rank': t.rank} for t in targets]
    new_target = Course.objects.get(code=code)
    targets_dict.append({'course': new_target, 'rank': (len(targets_dict) + 1)})
    if request.method == 'POST':
        target_formset = TargetFormSet(request.POST, form_kwargs={'request': request})
        if target_formset.is_valid():
            new_targets = []
            for target_form in target_formset:
                course = target_form.cleaned_data.get('course')
                rank = target_form.cleaned_data.get('rank')
                if course and rank:
                    new_targets.append(Target(course=course, rank=rank, profile=user.profile))
            try:
                with transaction.atomic():
                    Target.objects.filter(profile=user.profile).delete()
                    Target.objects.bulk_create(new_targets)
                    messages.success(request, 'Your target courses has been successfully updated.')
                    return redirect("/profile/view/")
            except IntegrityError:
                messages.error(request, 'An error occurred while saving your target courses.')
                return redirect(reverse('profile_view'))
    else:
        target_formset = TargetFormSet(initial=targets_dict, form_kwargs={'request': request})
    return render(request, 'coursesearch/profile_target.html', {'target_formset': target_formset})

def profile_edit_target(request):
    ''' This function renders the html page to allow the user to edit their target courses, such as changing the
            subject and rank, and adding or removing a target course, by rendering a BaseTargetFormSet formset.
            After checking that the form is valid, new Target model instances are created which are linked to the
            Profile of the user. '''
    user = request.user
    TargetFormSet = formset_factory(TargetForm, formset=BaseTargetFormSet)
    targets = Target.objects.filter(profile=user.profile).order_by('rank')
    targets_dict = [{'course': t.course, 'rank':t.rank} for t in targets]
    if request.method == 'POST':
        target_formset = TargetFormSet(request.POST, form_kwargs={'request': request})
        if target_formset.is_valid():
            new_targets = []
            for target_form in target_formset:
                course = target_form.cleaned_data.get('course')
                rank = target_form.cleaned_data.get('rank')
                if course and rank:
                    new_targets.append(Target(course=course, rank=rank, profile=user.profile))
            try:
                with transaction.atomic():
                    Target.objects.filter(profile=user.profile).delete()
                    Target.objects.bulk_create(new_targets)
                    messages.success(request,'Your target courses has been successfully updated.')
                    return redirect("/profile/view/")
            except IntegrityError:
                messages.error(request,'An error occurred while saving your target courses.')
                return redirect(reverse('profile_view'))
    else:
        target_formset = TargetFormSet(initial=targets_dict, form_kwargs={'request': request})
    return render(request,'coursesearch/profile_target.html',{'target_formset': target_formset})
