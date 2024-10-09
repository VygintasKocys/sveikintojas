from django.shortcuts import render, redirect
from django.conf import settings
from .forms import SveikinimoForma, TekstoRedagavimoForma
from .utils import generuoti_teksta, generuoti_garsa, generuoti_paveiksla, sujungti_failus
import os
from django.contrib import messages
import subprocess

def check_directories():
    directories = [
        os.path.join(settings.MEDIA_ROOT, 'garso_failai'),
        os.path.join(settings.MEDIA_ROOT, 'paveiksleliai'),
        os.path.join(settings.MEDIA_ROOT, 'galutiniai_failai'),
        os.path.join(settings.MEDIA_ROOT, 'temp')
    ]
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Sukurtas katalogas: {directory}")
            except Exception as e:
                print(f"Nepavyko sukurti katalogo {directory}: {str(e)}")
        else:
            print(f"Katalogas jau egzistuoja: {directory}")

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        print("FFmpeg rastas ir veikia")
    except subprocess.CalledProcessError:
        print("FFmpeg nerastas arba neveikia")
    except FileNotFoundError:
        print("FFmpeg neįdiegtas arba nepasiekiamas per PATH")

# Vykdome patikrinimus
check_directories()
check_ffmpeg()

def home(request):
    return render(request, 'generatorius/home.html')

def generate_text(request):
    if request.method == 'POST':
        forma = SveikinimoForma(request.POST)
        if forma.is_valid():
            tekstai = generuoti_teksta(forma.cleaned_data)
            request.session['tekstai'] = tekstai
            request.session['forma_duomenys'] = forma.cleaned_data
            return redirect('choose_text')
    else:
        forma = SveikinimoForma()
    return render(request, 'generatorius/generate_text.html', {'forma': forma})

def choose_text(request):
    tekstai = request.session.get('tekstai', [])
    if request.method == 'POST':
        pasirinktas_tekstas = request.POST.get('pasirinktas_tekstas')
        request.session['pasirinktas_tekstas'] = pasirinktas_tekstas
        return redirect('edit_text')
    return render(request, 'generatorius/choose_text.html', {'tekstai': tekstai})

def edit_text(request):
    pasirinktas_tekstas = request.session.get('pasirinktas_tekstas', '')
    if request.method == 'POST':
        forma = TekstoRedagavimoForma(request.POST)
        if forma.is_valid():
            redaguotas_tekstas = forma.cleaned_data['tekstas']
            request.session['galutinis_tekstas'] = redaguotas_tekstas
            return redirect('generate_audio')
    else:
        forma = TekstoRedagavimoForma(initial={'tekstas': pasirinktas_tekstas})
    return render(request, 'generatorius/edit_text.html', {'forma': forma})

def generate_audio(request):
    tekstas = request.session.get('galutinis_tekstas')
    forma_duomenys = request.session.get('forma_duomenys')
    if not tekstas or not forma_duomenys:
        return redirect('generate_text')

    if request.method == 'POST':
        balso_tipas = forma_duomenys.get('balso_tipas', 'moteris')
        try:
            garso_failas = generuoti_garsa(tekstas, balso_tipas)
            request.session['garso_failas'] = garso_failas
            return redirect('generate_image')
        except Exception as e:
            messages.error(request, f"Įvyko klaida generuojant garsą: {e}")
            return render(request, 'generatorius/generate_audio.html', {'tekstas': tekstas, 'error': str(e)})

    return render(request, 'generatorius/generate_audio.html', {'tekstas': tekstas})

def generate_image(request):
    tekstas = request.session.get('galutinis_tekstas')
    forma_duomenys = request.session.get('forma_duomenys')
    if not tekstas or not forma_duomenys:
        return redirect('generate_text')

    if request.method == 'POST':
        paveikslelio_stilius = forma_duomenys.get('paveikslelio_stilius', 'natural')
        try:
            paveikslai = generuoti_paveiksla(tekstas, paveikslelio_stilius)
            request.session['paveikslai'] = paveikslai
            return redirect('choose_image')
        except Exception as e:
            messages.error(request, f"Įvyko klaida generuojant paveikslėlį: {e}")
            return render(request, 'generatorius/generate_image.html', {'tekstas': tekstas, 'error': str(e)})

    return render(request, 'generatorius/generate_image.html', {'tekstas': tekstas})

def choose_image(request):
    paveikslai = request.session.get('paveikslai', [])
    paveikslai_urls = [os.path.join(settings.MEDIA_URL, 'paveiksleliai', os.path.basename(p)) for p in paveikslai]

    if request.method == 'POST':
        pasirinktas_paveikslas = request.POST.get('pasirinktas_paveikslas')
        if pasirinktas_paveikslas:
            pilnas_paveikslo_kelias = os.path.join(settings.MEDIA_ROOT, 'paveiksleliai', os.path.basename(pasirinktas_paveikslas))
            request.session['pasirinktas_paveikslas'] = pilnas_paveikslo_kelias
        return redirect('result')

    return render(request, 'generatorius/choose_image.html', {'paveikslai': paveikslai_urls})


def result(request):
    tekstas = request.session.get('galutinis_tekstas')
    garso_failas = request.session.get('garso_failas')
    pasirinktas_paveikslas = request.session.get('pasirinktas_paveikslas')

    print(f"Tekstas: {tekstas}")
    print(f"Garso failas: {garso_failas}")
    print(f"Pasirinktas paveikslas: {pasirinktas_paveikslas}")

    if not all([tekstas, garso_failas, pasirinktas_paveikslas]):
        messages.error(request, "Trūksta reikalingų duomenų. Pradėkite nuo pradžių.")
        return redirect('home')

    fono_muzikos_dir = os.path.join(settings.BASE_DIR, 'static', 'music')
    fono_muzikos_failai = [f for f in os.listdir(fono_muzikos_dir) if f.endswith('.mp3')]

    # Pataisytas paveikslėlio kelias
    pilnas_paveikslo_kelias = os.path.join(settings.MEDIA_ROOT, 'paveiksleliai', os.path.basename(pasirinktas_paveikslas))

    context = {
        'tekstas': tekstas,
        'garso_failas': os.path.join(settings.MEDIA_URL, 'garso_failai', os.path.basename(garso_failas)),
        'paveikslas': os.path.join(settings.MEDIA_URL, 'paveiksleliai', os.path.basename(pasirinktas_paveikslas)),
        'fono_muzikos_failai': fono_muzikos_failai
    }

    if request.method == 'POST':
        fono_muzika = request.POST.get('fono_muzika')
        print(f"Pasirinkta fono muzika: {fono_muzika}")

        if not fono_muzika:
            messages.error(request, "Prašome pasirinkti fono muziką.")
            return render(request, 'generatorius/result.html', context)

        fono_muzikos_failas = os.path.join(fono_muzikos_dir, fono_muzika)

        print(f"Fono muzikos failas: {fono_muzikos_failas}")
        print(f"Ar fono muzikos failas egzistuoja: {os.path.exists(fono_muzikos_failas)}")
        print(f"Ar garso failas egzistuoja: {os.path.exists(garso_failas)}")
        print(f"Ar paveikslėlio failas egzistuoja: {os.path.exists(pilnas_paveikslo_kelias)}")

        if not os.path.exists(fono_muzikos_failas):
            messages.error(request, f"Fono muzikos failas '{fono_muzika}' nerastas.")
            return render(request, 'generatorius/result.html', context)

        if not os.path.exists(garso_failas):
            messages.error(request, "Garso failas nerastas.")
            return render(request, 'generatorius/result.html', context)

        if not os.path.exists(pilnas_paveikslo_kelias):
            messages.error(request, "Paveikslėlio failas nerastas.")
            return render(request, 'generatorius/result.html', context)

        try:
            print(f"Bandoma sujungti failus:")
            print(f"Garso failas: {garso_failas}")
            print(f"Paveikslėlio failas: {pilnas_paveikslo_kelias}")
            print(f"Fono muzikos failas: {fono_muzikos_failas}")
            galutinis_failas = sujungti_failus(garso_failas, pilnas_paveikslo_kelias, fono_muzikos_failas)
            print(f"Galutinis failas: {galutinis_failas}")
            if os.path.exists(galutinis_failas):
                context['galutinis_failas'] = os.path.join(settings.MEDIA_URL, 'galutiniai_failai', os.path.basename(galutinis_failas))
                print(f"Galutinis failas sukurtas: {context['galutinis_failas']}")
            else:
                raise FileNotFoundError("Galutinis failas nebuvo sukurtas")
        except Exception as e:
            messages.error(request, f"Įvyko klaida sujungiant failus: {str(e)}")
            print(f"Klaida sujungiant failus: {str(e)}")
            print(f"Pilnas klaidos aprašymas:")
            import traceback
            print(traceback.format_exc())

    return render(request, 'generatorius/result.html', context)