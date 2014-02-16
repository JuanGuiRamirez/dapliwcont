from django import forms
from proveedor.models import cabeceraPro

import datetime



class cabeceraProForms( forms.ModelForm ):
    identificacion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
    fecha_tran = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class':'form-control'}),)     
    numero_fact = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), )
       
    class Meta:
        model = cabeceraPro
        exclude = ('created', 'createdby', 'isactive', 'updated', 'updatedby')
