from django import forms
from store.models import Product
from category.models import Category 


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['product_name','slug','description','price','image','category','stock','is_available']
        

        def __init__(self, *args,**kwargs):
            super(ProductForm,self).__init__(*args, **kwargs)
    
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'

            self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'



class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['category_name','slug', 'desciption']

    def __init__(self, *args,**kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


           