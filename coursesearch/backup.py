# class RankForm(forms.Form):
#     def __init__(self, request, *args, **kwargs):
#         super(RankForm, self).__init__(*args, **kwargs)
#     def clean(self):
#         rank = forms.ChoiceField(choices=[(i,i) for i in range(1,(Interest.objects.filter(profile=self.request.user.profile).count())+2)])
#
#
# def profile_add_target(request,code):
#     if request.method=='POST':
#         form = RankForm(request.POST,request)
#         if form.is_valid():
#             target = Course.objects.filter(code=code)
#             rank = form.cleaned_data.get('rank')
#             # new_target = Target(profile=request.user.profile,course=target,rank=rank)
#             # new_target.save()
#             return redirect('/profile/view')
#     else:
#         form = RankForm(request)
#         return render(request, 'coursesearch/add_target.html',{'form': form})
#
#
# url(r'^profile/add/course_(?P<code>[\w\-]+)/$', views.profile_add_target, name='profile_add_target'),
#
#
#
# {% extends 'coursesearch/base.html' %}
# {% block title %}Add Target Course{% endblock %}
# {% block content %}
#
# <div class="container">
#
# 	<div class="row" style="text-align: center;">
# 		<h3>Adding {{ course.code }} {{ course.name }} as Target Course</h3>
# 	</div>
#
# 	<form method="get">
# 		{% csrf_token %}
# 		{{ form.as_p }}
# 		<button type="submit"><span class="glyphicon glyphicon-plus"></span>Add</button>
# 	</form>
#
# </div>
#
# {% endblock %}