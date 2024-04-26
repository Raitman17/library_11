from django.forms import Form, CharField, DecimalField, ChoiceField, EmailField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

class AddFundsForm(Form):
    money = DecimalField(label='money', decimal_places=2, max_digits=11)

    def is_valid(self) -> bool:
        def add_error(error):
            if self.errors:
                self.errors['money'] += [error]
            else:
                self.errors['money'] = [error]

        if not super().is_valid():
            return False
        money = self.cleaned_data.get('money', None)
        if not money:
            add_error(ValidationError('an error occured, money field was not specified!'))
            return False
        if money < 0:
            add_error(ValidationError('you can only add positive amount of money!'))
            return False
        return True
