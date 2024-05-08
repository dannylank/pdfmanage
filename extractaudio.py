from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import VideoFileClip
from moviepy.config import change_settings
import speech_recognition as sr
import os

# Configurar manualmente la ruta de `ffmpeg`
ffmpeg_path = r'D:\\Files\\Personal\\Proyectos\\Phyton\\Leerpdf\\ffmpeg\\ffmpeg.exe'
change_settings({"FFMPEG_BINARY": ffmpeg_path})

# Ruta al archivo de video de entrada
video_path = r'D:\\Files\\Personal\\Ingenieria\\Computación Bioinspirada\\126649.mp4'

# Duración mínima de silencio para considerar un nuevo segmento (en milisegundos)
min_silence_duration = 2000

# Archivo de texto para guardar todas las transcripciones
transcription_file = r'D:\\Files\\Personal\\Ingenieria\\Computación Bioinspirada\\transcripciones.txt'

# Crear un objeto VideoFileClip
video_clip = VideoFileClip(video_path)

# Obtener la duración total del video
duration = int(video_clip.duration)

# Extraer el audio del video completo
audio_clip = video_clip.audio

# Exportar el audio a un archivo WAV temporal
temp_audio_wav = 'temp_audio.wav'
audio_clip.write_audiofile(temp_audio_wav)

# Cargar el archivo WAV en un objeto AudioSegment
audio_segment = AudioSegment.from_wav(temp_audio_wav)

# Crear un objeto recognizer para reconocer el audio
recognizer = sr.Recognizer()

# Verificar si el archivo de transcripción ya existe
if not os.path.exists(transcription_file):
    # Si el archivo no existe, crear el archivo y escribir el encabezado
    with open(transcription_file, 'w', encoding='utf-8') as output:
        output.write("Transcripciones por segmento\n")
        output.write("=" * 30 + "\n")

# Dividir el audio en segmentos basados en el silencio
segments = split_on_silence(audio_segment, min_silence_len=min_silence_duration, silence_thresh=-40)

# Calcular la duración total del audio en milisegundos
total_duration = len(audio_segment)

# Procesar cada segmento de audio
for i, segment in enumerate(segments):
    # Calcular los tiempos de inicio y fin del segmento en segundos
    start_time = sum(len(seg) for seg in segments[:i]) / 1000
    end_time = start_time + len(segment) / 1000
    
    # Exportar el segmento de audio a un archivo WAV temporal
    temp_segment_wav = f'temp_segment_{i}.wav'
    segment.export(temp_segment_wav, format='wav')
    
    # Usar SpeechRecognition para transcribir el archivo WAV temporal
    with sr.AudioFile(temp_segment_wav) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')
            transcripcion = f"Segmento {start_time:.2f}-{end_time:.2f} segundos: {text}"
        except sr.RequestError as e:
            transcripcion = f"Error en el reconocimiento del segmento {i}: {e}"
        except sr.UnknownValueError:
            transcripcion = f"No se pudo entender el audio en el segmento {i}."
    
    # Agregar la transcripción al archivo de texto
    with open(transcription_file, 'a', encoding='utf-8') as output:
        output.write(transcripcion + "\n")
    
    # Eliminar el archivo WAV temporal del segmento
    #os.remove(temp_segment_wav)

# Eliminar el archivo WAV temporal completo
#os.remove(temp_audio_wav)

# Cerrar el objeto VideoFileClip para liberar recursos
video_clip.close()