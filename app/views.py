from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm,ProjectForm,UpdateProfileForm,DesignForm,UsabilityForm,ContentForm
from .models import Profile,Project,UsabilityRating,DesignRating,ContentRating
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer,ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .email import send_welcome_email



# Create your views here.
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your Awwwards account.'
#             message = render_to_string('registration/activate_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'registration/signup.html', {'form': form})


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponse('Thank you for your email confirmation. Now you can <a href="/accounts/login/">Login</a>  to your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')



@login_required(login_url='/accounts/login/')
def index(request):
  '''
  view function that renders the homepage
  '''
  form=DesignForm()
  projects = Project.get_posted_projects().order_by('-posted_on')
  
  return render(request,'index.html',locals())

@login_required(login_url='/accounts/login/')
def search_results(request):
  if 'project' in request.GET and request.GET["project"]:
    form=DesignForm()
    title = request.GET.get("project")
    searched_projects = Project.search_project(title)
    message = f"{title}"

    return render(request, 'search.html',{"message":message,"projects":searched_projects,"form":form})

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
    form=DesignForm()
    title = "Profile"
    projects = Project.get_project_by_id(id= user_id).order_by('-posted_on')
    profiles = Profile.objects.get(user_id=user_id)
    users = User.objects.get(id=user_id)

    return render(request, 'profile/profile.html',locals())

    
@login_required(login_url='/accounts/login/')
def update_profile(request):
    '''
    Function that enables one to update their profile details
    '''
    current_user = request.user
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
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

@login_required(login_url='/login')
def add_usability(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = UsabilityForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.project = project
            rate.user_name = request.user
            rate.profile = request.user.profile

            rate.save()
        return redirect('index')

    return render(request, 'index.html')

@login_required(login_url='/login')
def add_design(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.project = project
            rate.user_name = request.user
            rate.profile = request.user.profile

            rate.save()
        return redirect('index')
    else:
        form = DesignForm()

    return render(request, 'index.html',{'form': form})


@login_required(login_url='/login')
def add_content(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.project = project
            rate.user_name = request.user
            rate.profile = request.user.profile

            rate.save()
        return redirect('index')

    return render(request, 'index.html')