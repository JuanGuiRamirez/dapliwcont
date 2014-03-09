from cxc.models import abono
from django import forms
import datetime


class abonoForm ( forms.ModelForm ):   
    montoAbono = forms.FloatField(initial=0, widget=forms.TextInput(attrs={'class':'form-control'}), label='Monto Abono')
    fechaAbono = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}), 
                                 initial=datetime.date.today, input_formats=['%Y-%m-%d'], label='Fecha Abono')
        
    class Meta:
        model = abono
        exclude = ('created', 'createdby', 'isactive', 'updated', 'updatedby', 'cuentaId', 'saldoInicial', 'saldoFinal')