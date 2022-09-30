from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile, Feedback
    
class UserRegisterForm(UserCreationForm):

	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['password1'].help_text = "Passwords must be of minimun 8 charectors"
		self.fields['username'].help_text = ""

	def clean(self):
		cleaned_data = self.cleaned_data

		# checking Email unique

		try:
		    User.objects.get(email=cleaned_data['email'])
		except User.DoesNotExist:
		    pass
		else:
		    raise ValidationError('This Email address already exists! Try different one!')

		# checking User unique

		try:
		    User.objects.get(username=cleaned_data['username'])
		except User.DoesNotExist:
		    pass
		else:
		    raise forms.ValidationError('User already exists! Try different one!')

		return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'profile_pic']

class FeedbackForm(forms.ModelForm):
    class Meta:
    	model = Feedback
    	fields = ['feedback']
  