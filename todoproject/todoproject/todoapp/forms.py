from django import forms
from .models import ToDo, Category


class ToDoForm(forms.ModelForm):
    
    due_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}), 
        required=False )

    
    new_category = forms.CharField(
        required=False, 
        help_text="Enter a new category if not listed", 
        label="New Category")

    
    
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'completed', 'due_date',  'category']
    widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,       # Adjust the number of rows
                'cols': 40,      # Adjust the number of columns
                'style': 'resize: none;',  # Disable resizing
            }), 
}
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        
        new_category_name = self.cleaned_data.get('new_category')
        
        if new_category_name:
            
            category, created = Category.objects.get_or_create(name=new_category_name)
            instance.category = category

        
        if commit:
            instance.save()

        return instance
