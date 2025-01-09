import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import webbrowser  # Web tarayıcısını kullanmak için
import keyboard  # Klavye olaylarını yakalamak için
import subprocess  # Uygulamaları çalıştırmak için
import sys  # Programı tamamen kapatmak için
import requests  # Web scraping için
from datetime import datetime  # Tarih ve saat bilgisi almak için

# Pydub için geçici dosya dizinini ayarlayın
os.environ["TMPDIR"] = "Bu dosya nerede olacaksa o klasörün adresini buraya girin"

# Günlerin Türkçe karşılıkları
days_in_turkish = {
    "Monday": "Pazartesi",
    "Tuesday": "Salı",
    "Wednesday": "Çarşamba",
    "Thursday": "Perşembe",
    "Friday": "Cuma",
    "Saturday": "Cumartesi",
    "Sunday": "Pazar"
}

def speak(text):
    """Sesli cevap verir."""
    tts = gTTS(text=text, lang='tr')
    output_file = os.path.join(os.path.expanduser("~"), "response.mp3")  # Kullanıcı ana dizinine kaydet
    tts.save(output_file)
    audio = AudioSegment.from_mp3(output_file)
    play(audio)
    os.remove(output_file)

def listen():
    """Sesli komut dinler."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis, seni dinliyorum...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="tr-TR")
            print(f"Dinlenen komut: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Üzgünüm, komutunu anlayamadım.")
            return None
        except sr.RequestError:
            speak("Ses tanıma servisine bağlanırken bir sorun oluştu.")
            return None

notes = []

def save_note(note):
    """Notları kaydeder."""
    notes.append(note)
    try:
        with open("notes.txt", "a", encoding="utf-8") as file:
            file.write(note + "\n")
        speak("Notunuz kaydedildi.")
    except Exception as e:
        speak(f"Not kaydedilirken bir hata oluştu: {e}")

def run_app(app_name):
    """Belirtilen uygulamayı çalıştırır"""
    apps = {
        "not defteri": "notepad.exe",
        "hesap makinesi": "calc.exe",
        "tarayıcı": r"Tarayıcınızın özellikler kısmında yazan adresini giriniz",
        "valorant": r"C:\Riot Games\Riot Client\RiotClientServices.exe",  # Valorant uygulamasının dosya yolu
        "cs go": "steam://rungameid/730",  # Counter Strike: Global Offensive
        "marvel": "steam://rungameid/2767030",  # Marvel Rivals
        "specter": "steam://rungameid/2507950",  # Specter Divide
        # Bu listeye diğer uygulamaları ve oyunları ekleyebilirsiniz
    }
    app_path = apps.get(app_name.lower())
    if app_path:
        try:
            if app_path.startswith("steam://") or app_path.startswith("com.epicgames.launcher://"):
                webbrowser.open(app_path)
            else:
                subprocess.Popen(app_path)
            speak(f"{app_name} açılıyor.")
        except Exception as e:
            speak(f"{app_name} açılırken bir hata oluştu: {e}")
    else:
        speak(f"{app_name} adlı uygulama veya oyun bulunamadı. Lütfen başka bir uygulama veya oyun deneyin.")

def get_weather():
    """Antalya'nın hava durumunu alır"""
    url = "https://wttr.in/Antalya?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        weather = response.text.strip()
        speak(f"Antalya'da hava durumu: {weather}")
    else:
        speak("Hava durumu bilgisi alınamadı.")

def process_command(command):
    """Komutları işler."""
    if "not al" in command:
        speak("Ne not almak istersiniz?")
        note = listen()
        if note:
            save_note(note)
    elif "soru sor" in command:
        speak("Bu işlev şu anda aktif değil.")
    elif "internette ara" in command:
        speak("Ne arayayım?")
        query = listen()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"{query} için internette arama yapılıyor.")
    elif "uygulama aç" in command:
        speak("Hangi uygulamayı açmak istersiniz?")
        app_name = listen()
        if app_name:
            run_app(app_name)
    elif "hangi gündeyiz" in command:
        day = datetime.now().strftime("%A")
        speak(f"Bugün günlerden {days_in_turkish[day]}.")
    elif "saat kaç" in command:
        time = datetime.now().strftime("%H:%M")
        speak(f"Şu an saat {time}.")
    elif "hava nasıl" in command:
        get_weather()
    elif "jarvis uyu" in command:
        speak("Jarvis uyuyor. Hoşçakalın.")
        sys.exit()  # Programı tamamen kapat
    elif "teşekkürler" in command:
        speak("Rica ederim. Bekliyorum...")
        return False  # Dinlemeyi durdur ve 0 tuşuna basana kadar bekle
    elif "neler yapabilirsin" in command:
        speak("Şu komutları verebilirsiniz: not al, soru sor, internette ara, uygulama aç, hangi gündeyiz, saat kaç, hava nasıl, jarvis uyu, teşekkürler.")
    return True

def main():
    """Ana döngü."""
    while True:
        # 0 tuşuna basılmayı bekle
        keyboard.wait('0')
        speak("Jarvis başlatıldı, seni dinliyorum.")
        
        command = listen()
        if command and "jarvis uyan" in command:
            speak("Efendim, uyandım. Komut almaya hazırım.")
            is_awake = True

            while is_awake:
                command = listen()
                if command:
                    is_awake = process_command(command)
                    if is_awake:
                        speak("Başka bir isteğiniz var mı?")
        elif command and "jarvis uyu" in command:
            speak("Jarvis uyuyor. Hoşçakalın.")
            sys.exit()

if __name__ == "__main__":
    main()
