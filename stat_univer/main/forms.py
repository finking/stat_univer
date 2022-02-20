from .models import Conference, Institute, FAQ
from django.forms import ModelForm, TextInput, Select, URLInput, EmailInput, Textarea, NumberInput, CheckboxInput, Form, EmailField


class ConferenceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Status'].empty_label = 'Выберите страну из списка.'

    class Meta:
        model = Conference
        fields = ['Name', 'Country', 'City', 'Month', 'Organizer', 'Student', 'Status', 'Total',
                  'Delegate', 'Url', 'Email', 'Comment']

        widgets = {
            'Name': TextInput(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название конферениции',
                'required': False
            }),
            'Country': Select(attrs={
                'class': 'form-select',
                'id': 'Status',
            }),
            'Status': Select(attrs={
                'class': 'form-select',
                'id': 'Status',
            }),
            'City': TextInput(attrs={
                'class': 'form-control',
                'id': 'City',
                'placeholder': 'Введите город проведения',
            }),
            'Month': Select(attrs={
                'class': 'form-select',
                'id': 'Month',
            }),
            'Organizer': CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'Organizer'
            }),
            'Student': CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'Student'
            }),
            'Total': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Total',
                'placeholder': 'Введите примерное количество участников',
            }),
            'Delegate': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Delegate',
                'placeholder': 'Введите количество представителей ГУУ',
            }),
            'Url': URLInput(attrs={
                'class': 'form-control',
                'id': 'url',
                'placeholder': 'https://',
                'required': False
            }),
            'Email': EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'you@example.com',
                'required': False
            }),
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'comment',
                'required': False
            }),

        }
    # use_required_attribute = False


class HistoryForm(Form):
    email = EmailField()


class InstituteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].error_messages = {
            'required': 'Введите значение'}
        # for k, field in self.fields.items():
        #     if 'required' in field.error_messages:
        #         field.error_messages['required'] = 'You have to field this.'

    class Meta:
        model = Institute
        fields = ['Name', 'ShortName', 'IdDirector', 'IdDeputeScience']

        widgets = {
            'Name': TextInput(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название Института',
            }),
            'ShortName': TextInput(attrs={
                'class': 'form-control ',
                'id': 'ShortName',
                'placeholder': 'Введите аббревиатуру Института',
            }),
            'IdDirector': Select(attrs={
                'class': 'form-select',
                'id': 'IdDirector',
            }),
            'IdDeputeScience': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeputeScience',
            }),
        }


class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ['Question', 'Answer', 'Link']

        widgets = {
            'Question': TextInput(attrs={
                'class': 'form-control ',
                'id': 'question',
                'placeholder': 'Введите вопрос',
            }),
            'Answer': Textarea(attrs={
                'class': 'form-control',
                'id': 'answer',
                'required': False
            }),
            'Link': URLInput(attrs={
                'class': 'form-control',
                'id': 'link',
                'placeholder': 'https://',
                'required': False
            }),
        }
