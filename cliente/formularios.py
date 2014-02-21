from django import forms
from cliente.models import cliente



class clienteForms( forms.ModelForm ):
    identificacion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    celular = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    saldodeuda = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    saldofavor = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    limitecredito = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),) 
        
    class Meta:
        model = cliente
        exclude = ('created', 'createdby', 'isactive', 'updated', 'updatedby')
