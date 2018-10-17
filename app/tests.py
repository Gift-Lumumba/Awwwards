from django.test import TestCase
from .models import Profile, Project
from django.contrib.auth.models import User

# TESTING PROFILE CLASS
class ProfileTestClass(TestCase):
    '''
    Tests profile methods and functions
    '''
    def setUp(self):

        self.user = User.objects.create(id =1,username='user1')
        self.profile = Profile(profile_pic='test.jpg', bio='Test bio', contact="987654321",user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_method(self):
        '''
        Function that tests whether a user's profile is being saved
        '''
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_method(self):
        '''
        Function that tests whether a user's profile can be deleted
        '''
        self.profile.save_profile()
        self.profile.delete_profile()

    
    def test_get_profile_by_id(self):
        '''
        Function that tests whether a user's profile can be found by its id
        '''
        self.profile.save_profile()
        profile= self.profile.get_profile_by_id(self.profile.user_id)
        profiles = Profile.objects.get(user_id=self.profile.user_id)
        self.assertTrue(profile, profiles)


# TESTING PROJECT CLASS
class ProjectTestClass(TestCase):
    '''
    Tests project class methods and functions
    '''
    def setUp(self):

        self.user = User.objects.create(id =2,username='Another user')

        self.profile = Profile(profile_pic='test2.jpg', bio='Biooo', contact="123456789",user=self.user)
        self.profile.save_profile()
        self.project = Project(title='title',image='image.jpg', description='Description', link='https://www.testingapplication.com', profile=self.profile, user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_method(self):
        '''
        Function that checks whether a project is being saved
        '''
        self.project.save_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)

    def test_delete_method(self):
        '''
        Function that tests whether a project can be deleted
        '''
        self.project.save_project()
        self.project.delete_project()

    def test_update_method(self):
        '''
        Function that tests whether a project's details can be updated
        '''
        self.project.save_project()
        updated_project = Project.objects.filter(title='title').update(title='title2')
        projects = Project.objects.get(title='title2')
        self.assertTrue(projects.title, 'title2')

    
