from django.forms import inlineformset_factory
import django.forms
from django import forms
from django.forms import DateInput
from .models import *
from django.core.exceptions import ValidationError


class MenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].label = 'Kuupäev'
        self.fields['theme'].label = 'Teema'
        self.fields['recommends'].label = 'Soovitab'
        self.fields['prepared'].label = 'Valmistas'

    class Meta:
        model = Menu
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%d.%m.%Y'),
            'theme': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                            'placeholder': 'Teema jaoks on vaja sisestada ka soovitaja'}),
            'recommends': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                                 'placeholder': 'Soovitaja jaoks on vaja sisestada teema'}),
            'prepared': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }
        fields = ('date', 'theme', 'recommends', 'prepared')


class FoodMenuUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuUpdateForm, self).__init__(*args, **kwargs)
        self.fields['food'].label = 'Söögi nimi'
        self.fields['full_price'].label = 'Täishind'
        self.fields['half_price'].label = 'Soodushind'
        self.fields['show_in_menu'].label = 'Näita menüüs'

    class Meta:
        model = FoodItem
        fields = ['food', 'full_price', 'half_price', 'show_in_menu']
        widgets = {
            'food': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'full_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'step': 0.01}),
            'half_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'step': 0.01}),
            'show_in_menu': django.forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'DELETE': 'Kustuta:',
        }


class FoodMenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuCreateForm, self).__init__(*args, **kwargs)

        self.fields['date'].label = 'Kuupäev'
        self.fields['category'].label = 'Kategooria'

    class Meta:
        model = FoodMenu
        fields = ['date', 'category']
        widgets = {
            'date': django.forms.Select(attrs={'type': 'date', 'class': 'form-control mb-2 form-select'}),
            'category': django.forms.Select(attrs={'class': 'form-control form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        category = cleaned_data.get('category')

        if FoodMenu.objects.filter(date=date, category=category).exists():
            raise ValidationError(
                f"Uut '{category}' kategooriat ei saa sellele kuupäevale sisestada, kuna see on juba olemas. "
                f"Et lisada veel toite kategooriasse vali Menüü Koostamine -> Muuda")

        return cleaned_data


class CategoryCreateForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


FoodMenuFormset = inlineformset_factory(
    FoodMenu,
    FoodItem,
    extra=5,
    form=FoodMenuUpdateForm,
    fields=('food', 'full_price', 'half_price', 'show_in_menu'))
