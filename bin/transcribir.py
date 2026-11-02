# transcribir.py
# Transcripción de audio a SRT + Markdown usando faster-whisper.
# Uso: python bin/transcribir.py [audio]   (por defecto: 1.opus)
#      python bin/transcribir.py 1.opus
# Requiere: faster-whisper, y (opcional) CUDA para GPU.
# Para descargar audio de una URL, usar yt-dlp antes:
#   yt-dlp -x --audio-format opus -o "1.opus" "URL"

import sys

AUDIO = sys.argv[1] if len(sys.argv) > 1 else "1.opus"

from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")

initial_prompt = (
    "Vocabulario TAI: Constitución Española de 1978, Cortes Generales, "
    "Congreso de los Diputados, Senado, Tribunal Constitucional, "
    "Estado autonómico, artículo 14, artículo 23, recurso de amparo, "
    "Ley Orgánica, real decreto, BOE, Título I, Título VIII."
)

segments, info = model.transcribe(
    AUDIO,
    language="es",
    beam_size=5,
    # batch_size=8,
    vad_filter=True,
    initial_prompt=initial_prompt,
)

with open("transcripcion.srt", "w", encoding="utf-8") as srt, \
     open("transcripcion.md", "w", encoding="utf-8") as md:
    for i, seg in enumerate(segments, 1):
        h, rem = divmod(int(seg.start), 3600)
        m, s = divmod(rem, 60)
        start = f"{h:02d}:{m:02d}:{s:02d}"
        h, rem = divmod(int(seg.end), 3600)
        m, s = divmod(rem, 60)
        end = f"{h:02d}:{m:02d}:{s:02d}"
        srt.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n\n")
        md.write(f"{seg.text.strip()}\n")
