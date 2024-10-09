import os
from openai import OpenAI
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import requests
from django.conf import settings
from moviepy.editor import *
from gtts.lang import tts_langs

media_root = settings.MEDIA_ROOT
garso_failai_dir = os.path.join(media_root, 'garso_failai')

if not os.path.exists(garso_failai_dir):
    os.makedirs(garso_failai_dir)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


ensure_dir(os.path.join(settings.MEDIA_ROOT, 'paveiksleliai'))
ensure_dir(os.path.join(settings.MEDIA_ROOT, 'garso_failai'))


def generuoti_teksta(duomenys, variantu_skaicius=3):
    prompt = f"Sukurkite sveikinimą {duomenys['proga']} proga {duomenys['asmuo']}. "
    if duomenys['amzius']:
        prompt += f"Asmeniui {duomenys['amzius']} metų. "
    prompt += f"Sveikinimo trukmė turėtų būti apie {duomenys['trukme']} sekundžių. "
    if duomenys['papildomi_pageidavimai']:
        prompt += f"Papildomi pageidavimai: {duomenys['papildomi_pageidavimai']}"

    tekstai = []
    for _ in range(variantu_skaicius):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        tekstai.append(response.choices[0].message.content.strip())

    return tekstai


def generuoti_garsa(tekstas, balso_tipas):
    try:
        if balso_tipas == 'vyras':
            tts = gTTS(text=tekstas, lang='lt', tld='lt')
        else:  # moteris
            tts = gTTS(text=tekstas, lang='lt')

        garso_failas = os.path.join(settings.MEDIA_ROOT, 'garso_failai', 'sveikinimas.mp3')
        tts.save(garso_failas)
        return garso_failas
    except ValueError as e:
        print(f"Klaida generuojant garsą: {e}")
        print(f"Palaikomos kalbos: {tts_langs()}")
        raise

def generuoti_prompta(tekstas):
    prompt = f"Sukurkite aprašyma (prompt) fotorealistinaim paveiksliukui generuoti, kuris iliustuotų ši teksta:{tekstas}.  Prompt'a sukurkite anglu kalba"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    print(response)
    return response

def generuoti_paveiksla(tekstas, stilius, variantu_skaicius=1):
    prompt = str(generuoti_prompta(tekstas))

    paveikslai = []
    for i in range(variantu_skaicius):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                style=stilius,
                size="1024x1024",
                quality="standard",
                n=1
            )

            image_url = response.data[0].url
            image_content = requests.get(image_url).content

            paveikslo_failas = os.path.join(settings.MEDIA_ROOT, 'paveiksleliai', f'sveikinimas_{i}.png')
            ensure_dir(paveikslo_failas)

            with open(paveikslo_failas, 'wb') as f:
                f.write(image_content)

            paveikslai.append(paveikslo_failas)
        except Exception as e:
            print(f"Klaida generuojant paveikslėlį {i}: {e}")

    return paveikslai


def sujungti_failus(garso_failas, paveikslo_failas, fono_muzikos_failas):
    try:
        print("Pradedamas failų sujungimas")

        print(f"Bandoma atidaryti garso failą: {garso_failas}")
        garsas = AudioSegment.from_mp3(garso_failas)

        print(f"Bandoma atidaryti fono muzikos failą: {fono_muzikos_failas}")
        fono_muzika = AudioSegment.from_mp3(fono_muzikos_failas)

        if len(fono_muzika) < len(garsas):
            fono_muzika = fono_muzika * (len(garsas) // len(fono_muzika) + 1)
        fono_muzika = fono_muzika[:len(garsas)]

        galutinis_garsas = garsas.overlay(fono_muzika)

        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_garso_failas = os.path.join(temp_dir, 'galutinis_garsas.mp3')
        print(f"Bandoma išsaugoti galutinį garsą: {temp_garso_failas}")
        galutinis_garsas.export(temp_garso_failas, format="mp3")

        print(f"Bandoma sukurti vaizdo klipą: {paveikslo_failas}")
        vaizdo_klipas = ImageClip(paveikslo_failas).set_duration(len(galutinis_garsas) / 1000)
        garso_klipas = AudioFileClip(temp_garso_failas)

        galutinis_klipas = vaizdo_klipas.set_audio(garso_klipas)

        galutiniai_failai_dir = os.path.join(settings.MEDIA_ROOT, 'galutiniai_failai')
        if not os.path.exists(galutiniai_failai_dir):
            os.makedirs(galutiniai_failai_dir)

        galutinis_failas = os.path.join(galutiniai_failai_dir, 'sveikinimas.mp4')
        print(f"Bandoma sukurti galutinį failą: {galutinis_failas}")
        galutinis_klipas.write_videofile(galutinis_failas, fps=1)

        # Valome laikinus failus
        os.remove(temp_garso_failas)

        print(f"Galutinis failas sukurtas: {galutinis_failas}")
        return galutinis_failas
    except Exception as e:
        print(f"Klaida sujungiant failus: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise