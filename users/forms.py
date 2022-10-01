from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile, Feedback
from django.core.validators import MaxLengthValidator, MinLengthValidator
    
class UserRegisterForm(UserCreationForm):
	username = forms.CharField(
		validators=[MinLengthValidator(5), MaxLengthValidator(15)],
		help_text='Username should be Alphanumeric of length 5 to 15'
	    )
	email = forms.EmailField()

	class Meta:
		model = User
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['password1'].help_text = "Passwords must be of minimun 8 charectors"
		self.fields['username'].help_text = "Passwords must be of minimun 8 charectors"

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
		fields = "__all__"

class FeedbackForm(forms.ModelForm):
    class Meta:
    	model = Feedback
    	fields = "__all__"
  
