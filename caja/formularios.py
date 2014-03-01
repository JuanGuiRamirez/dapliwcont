from django import forms
from caja.models import ingreso, egreso


class ingresoForm ( forms.ModelForm ):   
    totalIngreso = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    fechaIngreso = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}),)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'cols':20, 'class':'form-control'}))
    
    class Meta:
        model = ingreso
        exclude = ('created', 'createdby', 'isactive', 'updated', 'updatedby', 'cajaId')
    

class egresoForm ( forms.ModelForm ):   
    totalEgreso = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}),)
    fechaEgreso = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}),)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'cols':20, 'class':'form-control'}))
    
    class Meta:
        model = egreso
        exclude = ('created', 'createdby', 'isactive', 'updated', 'updatedby', 'cajaId')
