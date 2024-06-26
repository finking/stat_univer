from .models import Conference, Institute, FAQ, VAK, Thesis, Monograph, Income, RID
from django.forms import ModelForm, TextInput, Select, URLInput, EmailInput, Textarea, NumberInput, \
    CheckboxInput, Form, EmailField, FileInput, ChoiceField
from .utils import PARAMETERNAME


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
    
    
class DashboardForm(Form):
    feature = ChoiceField(choices=PARAMETERNAME,
                          label='Показатель',
                          widget=Select(attrs={"style": "width: 100%"}))


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
        fields = ['Name', 'Output', 'Tom', 'Pages', 'Year', 'DepartmentSame', 'DepartmentOther', 'Url',
                  'IdDeparture', 'Accepted', 'Points', 'Comment', 'Author']  # Порядок отображения полей

        widgets = {
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название публикации',
                'rows': 5
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
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5
            }),
            'DepartmentOther': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentOther',
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5
            }),
            'Url': URLInput(attrs={
                'class': 'form-control',
                'id': 'Url',
                'placeholder': 'https://elibrary.ru/',
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
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False,
                'rows': 5
            }),
            'Author': Select(attrs={
                'class': 'form-select',
                'id': 'Author',
                'hidden': True
            }),
        }


class ThesisForm(ModelForm):

    class Meta:
        model = Thesis
        fields = ['Type','Name', 'Output', 'Pages', 'Year', 'DepartmentSame', 'DepartmentOther', 'Url',
                  'IdDeparture', 'Accepted', 'Points', 'Comment', 'Author']

        widgets = {
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Type': Select(attrs={
                'class': 'form-select',
                'id': 'Type',
            }),
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название публикации',
                'rows': 5
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
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5
            }),
            'DepartmentOther': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentOther',
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5
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
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False,
                'rows': 5
            }),
            'Author': Select(attrs={
                'class': 'form-select',
                'id': 'Author',
                'hidden': True
            }),
        }


class MonographForm(ModelForm):

    class Meta:
        model = Monograph
        fields = ['Name', 'Output', 'Pages', 'Year', 'DepartmentSame', 'DepartmentOther', 'Url',
                  'IdDeparture', 'Accepted', 'Points', 'Comment', 'Author']

        widgets = {
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите название монографии',
                'rows': 5
            }),
            'Output': TextInput(attrs={
                'class': 'form-control',
                'id': 'Output',
                'placeholder': 'Введите ISBN'
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
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5
            }),
            'DepartmentOther': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentOther',
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5
            }),
            'Url': URLInput(attrs={
                'class': 'form-control',
                'id': 'Url',
                'placeholder': 'https://',
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
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False,
                'rows': 5
            }),
            'Author': Select(attrs={
                'class': 'form-select',
                'id': 'Author',
                'hidden': True
            }),
        }
        

class IncomeForm(ModelForm):

    class Meta:
        model = Income
        fields = ['IdDeparture', 'Name', 'Year', 'Accepted', 'Value', 'Points', 'Comment', 'Author']

        widgets = {
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите наименование НИР (работы, услуги)',
                'rows': 5
            }),
            'Year': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Year',
                'placeholder': 'Введите год, например: 2024',
            }),
            
            'Accepted': CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'Accepted',
                'required': False
            }),
    
            'Value': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Value',
                'required': False
            }),
            
            'Points': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Points',
                'required': False
            }),
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False,
                'rows': 5
            }),
            'Author': Select(attrs={
                'class': 'form-select',
                'id': 'Author',
                'hidden': True
            }),
        }


class RidForm(ModelForm):
    class Meta:
        model = RID
        fields = ['IdDeparture', 'Name', 'Year', 'Doc', 'Accepted', 'Points', 'Comment', 'Author']
        
        widgets = {
            'IdDeparture': Select(attrs={
                'class': 'form-select',
                'id': 'IdDeparture',
            }),
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите наименование РИД',
                'rows': 5
            }),
            'Year': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Year',
                'placeholder': 'Введите год, например: 2024',
            }),
            
            'Doc': FileInput(attrs={
                'class': 'form-control',
                'id': 'Doc',
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
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'required': False,
                'rows': 5
            }),
            'Author': Select(attrs={
                'class': 'form-select',
                'id': 'Author',
                'hidden': True
            }),
        }