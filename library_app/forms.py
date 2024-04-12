from django.forms import Form, CharField, DecimalField, ChoiceField, EmailField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

choices = (
    ('first', 'first'),
    ('second', 'second'),
)

class TestForm(Form):
    choice = ChoiceField(label='choice', choices=choices)
    number = DecimalField(label='number')
    text = CharField(label='text')

class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']