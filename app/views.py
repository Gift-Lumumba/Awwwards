from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
  return render(request,'index.html')


def search_results(request):
  if 'project' in request.GET and request.GET["project"]:
    title = request.GET.get("project")
    searched_projects = Project.search_project(title)
    message = f"{title}"

    return render(request, 'search.html',{"message":message,"projects":searched_projects})

  else:
    message = "You haven't searched for anything"
    return render(request, 'search.html',{"message":message})