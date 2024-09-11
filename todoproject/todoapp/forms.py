from django import forms
from .models import ToDo, Category
import datetime

class ToDoForm(forms.ModelForm):
    
    due_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}), 
        required=False
    )
    
    new_category = forms.CharField(
        required=False, 
        help_text="Enter a new category if not listed", 
        label="New Category"
    )

    class Meta:
        model = ToDo
        fields = ['title', 'description', 'completed', 'due_date', 'category']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,       
                'cols': 40,      
                'style': 'resize: none;',  
            }), 
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title is required.')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 10:
            raise forms.ValidationError('Description must be at least 10 characters long.')
        return description

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < datetime.date.today():
            raise forms.ValidationError('Due date cannot be in the past.')
        return due_date
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        new_category_name = self.cleaned_data.get('new_category')
        
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            instance.category = category

        if commit:
            instance.save()

        return instance

   
 