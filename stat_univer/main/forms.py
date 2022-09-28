from .models import Conference, Institute, FAQ, VAK, Thesis
from django.forms import ModelForm, TextInput, Select, URLInput, EmailInput, Textarea, NumberInput, CheckboxInput, Form, EmailField, FloatField


class ConferenceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Status'].empty_label = 'Выберите страну из списка.'

    class Meta:
        model = Conference
        fields = ['Name', 'Country', 'City', 'Month', 'Organizer', 'Student', 'Status', 'Total', 'Delegate',
                  'Total_student', 'Delegate_student', 'Url', 'Email', 'Invite']

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
            'Total_student': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Total_student',
                'placeholder': 'Введите количество студентов, принявших участие.',
                'required': False
            }),
            'Delegate_student': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Delegate_student',
                'placeholder': 'Введите количество студентов ГУУ, участвующих в конференции.',
                'required': False
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
            'Invite': Textarea(attrs={
                'class': 'form-control',
                'id': 'Invite',
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


class VAKForm(ModelForm):

    class Meta:
        model = VAK
        fields = ['Name', 'Output', 'Tom', 'Pages', 'Year', 'DepartmentSame', 'DepartmentOther', 'Url', 'IdInstitute',
                  'IdDeparture', 'Accepted', 'Comment', 'Points']

        widgets = {
            'IdInstitute': Select(attrs={
                'class': 'form-select',
                'id': 'IdInstitute',
            }),
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Name': TextInput(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название публикации'
            }),
            'Output': TextInput(attrs={
                'class': 'form-control',
                'id': 'Output',
                'placeholder': 'Введите название журнала'
            }),
            'Tom': TextInput(attrs={
                'class': 'form-control',
                'id': 'Tom',
                'placeholder': 'Введите том издания (при налиичии)',
                'required': False
            }),
            'Year': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Year',
                'placeholder': 'Введите год издания, например: 2021',
            }),
            'Pages': TextInput(attrs={
                'class': 'form-control',
                'id': 'Pages',
                'placeholder': 'Например, 5-8',
                'required': False
            }),
            'DepartmentSame': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentSame',
                'placeholder': '(по возможности с указанием кафедры)'
            }),
            'DepartmentOther': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentOther',
                'placeholder': '(по возможности с указанием кафедры)'
            }),
            'Url': URLInput(attrs={
                'class': 'form-control',
                'id': 'Url',
                'placeholder': 'https://',
                # 'required': False
            }),
            'Accepted': CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'Accepted',
                'required': False
            }),
            'Points': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Points',
                'required': False
            }),
            'Comment': TextInput(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False
            }),
        }


class ThesisForm(ModelForm):

    class Meta:
        model = Thesis
        fields = ['Type','Name', 'Output', 'Pages', 'Year', 'DepartmentSame', 'DepartmentOther', 'Url', 'IdInstitute',
                  'IdDeparture', 'Accepted', 'Points', 'Comment']

        widgets = {
            'IdInstitute': Select(attrs={
                'class': 'form-select',
                'id': 'IdInstitute',
            }),
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Type': Select(attrs={
                'class': 'form-select',
                'id': 'Type',
            }),
            'Name': TextInput(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название публикации'
            }),
            'Output': TextInput(attrs={
                'class': 'form-control',
                'id': 'Output',
                'placeholder': 'Введите полное название конференции'
            }),
            'Year': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Year',
                'placeholder': 'Введите год издания, например: 2021',
            }),
            'Pages': TextInput(attrs={
                'class': 'form-control',
                'id': 'Pages',
                'placeholder': 'Например, 5-8',
                'required': False
            }),
            'DepartmentSame': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentSame',
                'placeholder': '(по возможности с указанием кафедры)'
            }),
            'DepartmentOther': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentOther',
                'placeholder': '(по возможности с указанием кафедры)'
            }),
            'Url': URLInput(attrs={
                'class': 'form-control',
                'id': 'Url',
                'placeholder': 'https://',
                # 'required': False
            }),
            'Accepted': CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'Accepted',
                'required': False
            }),
            'Points': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Points',
                'required': False
            }),
            'Comment': TextInput(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False
            }),
        }
