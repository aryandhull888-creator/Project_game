# game/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re 

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',) 

    # game/forms.py

# ... (keep your other imports and the UserRegisterForm class definition)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        
        # This first check for matching passwords is fine
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")

        # --- This is the corrected part ---
        # We add "if password:" to ensure these checks only run if a password was provided.
        if password:
            if len(password) < 5:
                raise forms.ValidationError("Password must be at least 5 characters long.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("Password must contain at least one number.")
            if not re.search(r'[$%*@]', password):
                raise forms.ValidationError("Password must contain one of $, %, *, or @.")
        
        return password2