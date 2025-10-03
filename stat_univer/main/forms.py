from .models import Conference, Institute, FAQ, VAK, Thesis, Monograph, Income, RID
from django.forms import ModelForm, TextInput, Select, URLInput, EmailInput, Textarea, NumberInput, \
    CheckboxInput, Form, EmailField, FileInput, ChoiceField, DateField, DateInput
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


class ConferenceExportForm(Form):
    start_date = DateField(
        label='Дата с',
        widget=DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = DateField(
        label='Дата по',
        widget=DateInput(attrs={'type': 'date'}),
        required=False
    )


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
        fields = ['Name', 'ShortName', 'Director', 'DeputeScience']

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
            'Director': Select(attrs={
                'class': 'form-select',
                'id': 'Director',
            }),
            'DeputeScience': Select(attrs={
                'class': 'form-select',
                'id': 'DeputeScience',
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


class BaseForm(ModelForm):
    class Meta:
        widgets = {
            'Departure': Select(attrs={
                'class': 'form-select',
                'id': 'Departure',
            }),
            'Year': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Year',
                'placeholder': 'Введите год, например: 2024',
            }),
            'DepartmentSame': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentSame',
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5,
            }),
            'DepartmentOther': Textarea(attrs={
                'class': 'form-control',
                'id': 'DepartmentOther',
                'placeholder': '(по возможности с указанием кафедры)',
                'rows': 5,
            }),
            'Accepted': CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'Accepted',
                'required': False,
            }),
            'Points': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Points',
                'required': False,
            }),
            'Comment': Textarea(attrs={
                'class': 'form-control',
                'id': 'Comment',
                'rows': 5,
                'required': False,
            }),
            'Author': Select(attrs={
                'class': 'form-select',
                'id': 'Author',
                'hidden': True,
            }),
        }
                
                
class PublicationForm(BaseForm):
    class Meta(BaseForm.Meta):
        fields = ['Departure', 'Name', 'Output', 'Pages', 'Year', 'DepartmentSame', 'DepartmentOther', 'Url',
                  'Accepted', 'Points', 'Comment', 'Author']
    
        widgets = {
            **BaseForm.Meta.widgets,
            'Name': Textarea(attrs={
                'class': 'form-control',
                'id': 'Name',
                'placeholder': 'Введите название публикации',
                'rows': 5,
            }),
            'Output': TextInput(attrs={
                'class': 'form-control',
                'id': 'Output',
                'placeholder': 'Введите название журнала или конференции',
            }),
            'Pages': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например, 5-8',
                'id': 'Pages',
                'required': False,
            }),

            'Url': URLInput(attrs={
                'class': 'form-control',
                'id': 'Url',
                'placeholder': 'https://',
            }),
        }


class VAKForm(PublicationForm):

    class Meta(PublicationForm.Meta):
        model = VAK
        fields = PublicationForm.Meta.fields[:3] + ['Doi'] + ['Tom'] + PublicationForm.Meta.fields[3:]

        widgets = {
            **PublicationForm.Meta.widgets,
            'Doi': TextInput(attrs={
                'class': 'form-control',
                'id': 'Doi',
                'placeholder': 'Введите DOI публикации',
                'required': False,
            }),
            'Tom': TextInput(attrs={
                'class': 'form-control',
                'id': 'Tom',
                'placeholder': 'Введите том издания (при наличии)',
                'required': False,
            }),
        }


class ThesisForm(ModelForm):

    class Meta:
        model = Thesis
        fields = PublicationForm.Meta.fields[:1] + ['Type'] + PublicationForm.Meta.fields[1:]

        widgets = {
            **PublicationForm.Meta.widgets,
            'Type': Select(attrs={
                'class': 'form-select',
                'id': 'Type',
            }),
        }


class MonographForm(ModelForm):

    class Meta:
        model = Monograph
        fields = PublicationForm.Meta.fields

        widgets = {
            **PublicationForm.Meta.widgets,
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
        }
        

class IncomeForm(BaseForm):

    class Meta(BaseForm.Meta):
        model = Income
        fields = ['Departure', 'Name', 'Year', 'DepartmentSame', 'DepartmentOther', 'Accepted', 'Value',
                  'Points', 'Comment', 'Author']

        widgets = {
            **BaseForm.Meta.widgets,
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите наименование НИР (работы, услуги)',
                'rows': 5
            }),
            'Value': NumberInput(attrs={
                'class': 'form-control',
                'id': 'Value',
            }),
        }


class RidForm(ModelForm):
    class Meta:
        model = RID
        fields = ['Departure', 'Name', 'Year', 'DepartmentSame', 'DepartmentOther', 'Doc', 'Accepted',
                  'Points', 'Comment', 'Author']
        
        widgets = {
            **BaseForm.Meta.widgets,
            'Name': Textarea(attrs={
                'class': 'form-control ',
                'id': 'Name',
                'placeholder': 'Введите наименование РИД',
                'rows': 5
            }),
            'Doc': FileInput(attrs={
                'class': 'form-control',
                'id': 'Doc',
            }),

        }