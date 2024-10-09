from django import forms

class SveikinimoForma(forms.Form):
    proga = forms.CharField(max_length=100, label='Proga')
    asmuo = forms.CharField(max_length=100, label='Asmuo')
    amzius = forms.IntegerField(min_value=0, required=False, label='Amžius')
    trukme = forms.IntegerField(min_value=10, max_value=120, label='Trukmė (sekundėmis)')
    papildomi_pageidavimai = forms.CharField(widget=forms.Textarea, required=False, label='Papildomi pageidavimai')
    balso_tipas = forms.ChoiceField(choices=[('vyras', 'Vyriškas'), ('moteris', 'Moteriškas')], label='Balso tipas')
    paveikslelio_stilius = forms.ChoiceField(choices=[
        ('natural', 'Realistinis'),
        ('vivid', 'Animacinis'),
        ('natural', 'Abstraktus')
    ], label='Paveikslėlio stilius')

class TekstoRedagavimoForma(forms.Form):
    tekstas = forms.CharField(widget=forms.Textarea, label='Redaguoti tekstą')