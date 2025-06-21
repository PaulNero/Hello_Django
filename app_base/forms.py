from django.forms import forms, fields

class ContactForm(forms.Form):
    name = fields.CharField(
        label="Имя",
        widget=fields.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Введите ваше полное имя'
                })
            )
    message = fields.CharField(
        label="Сообщение",
        widget=fields.Textarea(attrs={
                'class': 'form-control',
                "placeholder": "Введите ваше сообщение",
                'rows': 5, # Устанавливаем количество строк
                'cols': 40 # Устанавливаем количество колонок
                })
            )
    agree = fields.BooleanField(
        label="Согласен с условиями",
        widget=fields.CheckboxInput(attrs={
                'class': 'form-check-input'
                })
            )
    sender = fields.EmailField(
        label="Email",
        widget=fields.EmailInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Введите ваш email"
                })
            )

    def clean_name(self):
        name = self.cleaned_data['name']
        if 'spam' in name:
            raise forms.ValidationError('Spam is not allowed')
        return name
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if 'spam' in message:
            raise forms.ValidationError('Spam is not allowed')
        return message

    def clean_sender(self):
        sender = self.cleaned_data['sender']
        if 'spam' in sender:
            raise forms.ValidationError('Spam is not allowed')
        return sender

    # def clean(self):
    #     cleaned_data = super().clean()
    #     message = cleaned_data["message"]
    #     if 'spam' in message:
    #         raise forms.ValidationError('Spam is not allowed')
    #     return cleaned_data
