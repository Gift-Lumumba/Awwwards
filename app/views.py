from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from . models import Profile,Project


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
  '''
  view function that renders the homepage
  '''
  projects = Project.get_posted_projects().order_by('-posted_on')
  
  return render(request,'index.html',locals())

@login_required(login_url='/accounts/login/')
def search_results(request):
  if 'project' in request.GET and request.GET["project"]:
    title = request.GET.get("project")
    searched_projects = Project.search_project(title)
    message = f"{title}"

    return render(request, 'search.html',{"message":message,"projects":searched_projects})

  else:
    message = "You haven't searched for anything"
    return render(request, 'search.html',{"message":message})

@login_required(login_url='accounts/login/')
def upload_project(request):
    profile = Profile.objects.all()
    for profile in profile:
      if request.method == 'POST':
          form = ProjectForm(request.POST, request.FILES)
          if form.is_valid():
              add=form.save(commit=False)
              add.profile = profile
              add.user = request.user
              add.save()
              return redirect('index')
      else:
          form = ProjectForm()


      return render(request,'upload.html',locals())

@login_required(login_url='/accounts/login/')
def profile(request, user_id):
    '''
    View function that enables users see their profile
    '''
    title = "Profile"
    profiles = Profile.objects.all()

    return render(request,'profile.html',locals())