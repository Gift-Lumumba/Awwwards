from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from .forms import ProjectForm,UpdateProfileForm
from .models import Profile,Project
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer,ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly


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
    """
    Function that enables one to see their profile
    """
    title = "Profile"
    projects = Project.get_project_by_id(id= user_id).order_by('-posted_on')
    # profiles = User.objects.get(id=user_id)
    users = User.objects.get(id=user_id)

    return render(request, 'profile/profile.html',locals())

    
@login_required(login_url='/accounts/login/')
def update_profile(request):
   if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
        return redirect('index')
   else:
        form = UpdateProfileForm()
   return render(request, 'profile/update_profile.html', locals())

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    permission_classes = (IsAdminOrReadOnly,)
    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    permission_classes = (IsAdminOrReadOnly,)
    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_profile(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
