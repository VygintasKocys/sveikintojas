from django.db import models

class Sveikinimas(models.Model):
    tekstas = models.TextField()
    garso_failas = models.FileField(upload_to='garso_failai/')
    paveikslelis = models.ImageField(upload_to='paveiksleliai/')
    galutinis_failas = models.FileField(upload_to='galutiniai_failai/')
    sukurimo_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sveikinimas {self.id}"

class FonoMuzika(models.Model):
    pavadinimas = models.CharField(max_length=100)
    failas = models.FileField(upload_to='fono_muzika/')

    def __str__(self):
        return self.pavadinimas
