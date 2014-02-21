from django import forms
from producto.models import producto



class productoForms( forms.ModelForm ):
    codigo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    cantidad = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    preciocompra = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    precioventa = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    descuento_max = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)   
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'cols':20, 'class':'form-control'}))
    
    class Meta:
        model = producto
        exclude = ('created', 'createdby', 'isactive', 'updated', 'updatedby', 'imagen')
