from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )
    username = forms.CharField(
        error_messages={"required": "유저이름을 입력해주세요."},
        label="유저명",
    )
    password1 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호",
    )
    password2 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호 확인",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    username=forms.CharField(
        error_messages={"required": "유저이름을 입력해주세요."},
        label="유저명"
    )
    password=forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput, label="비밀번호" 
    )
    def clean(self):                                       
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password :
            try:
                user = User.objects.get(username=username)
                if not check_password(password, user.password):
                    self.add_error('password', '비밀번호를 틀렸습니다.') 
                else:
                    self.user_id = user.id
            except Exception:
                self.add_error('username', '존재하지 않는 아이디 입니다.')