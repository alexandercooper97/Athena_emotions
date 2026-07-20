# -*- coding: utf-8 -*-
"""
ATHENA — Santuario de las Emociones
Detección de emociones faciales multi-persona con IA (DeepFace, 7 emociones)
+ Dashboard emocional individual y grupal + Consejera de bienestar emocional
Estética: serenidad y majestuosidad del Monte Olimpo.

Para cambiar el nombre de la app, edita APP_NAME y APP_EPITHET más abajo
(por ejemplo: APP_NAME = "LUCIANA", APP_EPITHET = "La Portadora de Luz").
"""

import os
import time
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# ═══════════════════════════════════ IDENTIDAD ══════════════════════════════
APP_NAME = "ATHENA"                      # ← cámbialo a "LUCIANA" si prefieres
APP_EPITHET = "Diosa de la Sabiduría"    # ← p. ej. "La Portadora de Luz"
APP_TAGLINE = "Santuario de las Emociones · Inteligencia Artificial para el bienestar"

st.set_page_config(page_title=APP_NAME, page_icon="🦉", layout="wide")

# ══════════════════════════════════ EMOCIONES ═══════════════════════════════
EMO_ES = {
    "angry": "Enojo", "disgust": "Desagrado", "fear": "Miedo",
    "happy": "Alegría", "sad": "Tristeza", "surprise": "Sorpresa",
    "neutral": "Serenidad",
}
EMO_ICON = {
    "angry": "🔥", "disgust": "🌫️", "fear": "🌩️", "happy": "☀️",
    "sad": "🌧️", "surprise": "✨", "neutral": "🕊️",
}
EMO_COLOR = {
    "Enojo": "#b3543f", "Desagrado": "#7a8450", "Miedo": "#6b5b8e",
    "Alegría": "#d9a441", "Tristeza": "#5b7d99", "Sorpresa": "#c98bb1",
    "Serenidad": "#8fae9d",
}
BOX_COLOR = (163, 137, 76)  # dorado en BGR

# ═══════════════════════════════════ ESTILO ═════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

:root {
    --marble: #f6f3ec;
    --marble-2: #efeae0;
    --sky: #dfe8ee;
    --gold: #b08d3e;
    --gold-soft: #c9ae6e;
    --ink: #3c4148;
    --ink-soft: #6b7178;
    --laurel: #8fae9d;
}

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }
.stApp {
    background:
        radial-gradient(ellipse 1000px 400px at 50% -5%, rgba(223,232,238,.9), transparent 70%),
        radial-gradient(ellipse 700px 300px at 15% 110%, rgba(201,174,110,.12), transparent 60%),
        linear-gradient(180deg, #f8f6f0 0%, #f4f0e7 55%, #efe9dd 100%);
}
#MainMenu, footer { visibility: hidden; }

/* ── FRONTÓN DEL TEMPLO ── */
.pediment { text-align: center; padding: 2rem 1rem .8rem; position: relative; }
.pediment .owl { font-size: 2.4rem; display: block; margin-bottom: .3rem;
    filter: drop-shadow(0 4px 14px rgba(176,141,62,.4)); }
.pediment h1 {
    font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: .3em;
    color: var(--ink); font-size: 2.7rem; margin: 0;
}
.pediment h1 .au { color: var(--gold); }
.pediment .epithet {
    font-family: 'Cormorant Garamond', serif; font-style: italic;
    color: var(--ink-soft); font-size: 1.25rem; margin-top: .15rem;
}
.pediment .tagline {
    font-size: .74rem; letter-spacing: .28em; text-transform: uppercase;
    color: var(--gold); margin-top: .7rem; font-weight: 700;
}
/* laureles */
.laurel-line {
    display: flex; align-items: center; justify-content: center;
    gap: 1rem; margin: 1rem auto .2rem; max-width: 560px;
}
.laurel-line .stem { flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold-soft)); }
.laurel-line .stem:last-child {
    background: linear-gradient(90deg, var(--gold-soft), transparent); }
.laurel-line .leaf { color: var(--gold); font-size: 1.05rem; letter-spacing: .4em; }

/* ── COLUMNATA (tarjetas) ── */
.stele {
    background: linear-gradient(180deg, #fffdf8, var(--marble));
    border: 1px solid rgba(176,141,62,.28);
    border-top: 3px solid var(--gold-soft);
    border-radius: 3px 3px 10px 10px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 14px 34px rgba(60,65,72,.09);
    margin: .6rem 0;
}
.stele h3 {
    font-family: 'Cinzel', serif; color: var(--ink); font-size: 1.05rem;
    letter-spacing: .1em; margin: 0 0 .5rem; font-weight: 600;
}
.stele p, .stele li { color: var(--ink-soft); font-size: .95rem; line-height: 1.7; margin: 0; }
.stele .gold { color: var(--gold); font-weight: 700; }

/* ── ORÁCULO / CONSEJOS ── */
.oracle {
    background: linear-gradient(180deg, #fffdf6, #f8f3e6);
    border: 1px solid rgba(176,141,62,.35);
    border-left: 4px solid var(--gold);
    border-radius: 6px; padding: 1.2rem 1.4rem; margin: .7rem 0;
}
.oracle h4 {
    font-family: 'Cormorant Garamond', serif; font-weight: 600;
    color: var(--ink); font-size: 1.25rem; margin: 0 0 .4rem;
}
.oracle p { color: var(--ink-soft); font-size: .94rem; line-height: 1.75; margin: .3rem 0; }
.oracle .verse { font-family: 'Cormorant Garamond', serif; font-style: italic;
    color: var(--gold); font-size: 1.02rem; }

/* ── BOTONES ── */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: linear-gradient(180deg, #c3a15c, var(--gold)) !important;
    color: #fffdf6 !important; border: 1px solid #9a7a33 !important;
    border-radius: 6px !important; padding: .7rem 2rem !important;
    font-family: 'Cinzel', serif !important; font-weight: 600 !important;
    letter-spacing: .12em; font-size: .95rem !important; width: 100%;
    box-shadow: 0 8px 22px rgba(176,141,62,.35);
    transition: box-shadow .2s ease, transform .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 30px rgba(176,141,62,.5);
}

/* ── RELOJ DE ARENA DE MNEMÓSINE ── */
.hourglass-scene { text-align: center; padding: 2.2rem 0 1.4rem; }
.hg {
    display: inline-block; position: relative; width: 64px; height: 88px;
    animation: hgflip 3s ease-in-out infinite;
}
.hg .frame-t, .hg .frame-b {
    position: absolute; left: 0; right: 0; height: 6px;
    background: var(--gold); border-radius: 3px;
}
.hg .frame-t { top: 0; } .hg .frame-b { bottom: 0; }
.hg .bulb-t, .hg .bulb-b {
    position: absolute; left: 8px; right: 8px; height: 36px;
    border: 2.5px solid var(--gold-soft); background: rgba(255,253,246,.85);
}
.hg .bulb-t { top: 6px; border-bottom: none; border-radius: 6px 6px 0 0;
    clip-path: polygon(0 0, 100% 0, 58% 100%, 42% 100%); }
.hg .bulb-b { bottom: 6px; border-top: none; border-radius: 0 0 6px 6px;
    clip-path: polygon(42% 0, 58% 0, 100% 100%, 0 100%); }
.hg .sand-t {
    position: absolute; top: 12px; left: 14px; right: 14px; height: 22px;
    background: var(--gold-soft);
    clip-path: polygon(0 0, 100% 0, 55% 100%, 45% 100%);
    animation: drain 3s linear infinite;
}
.hg .sand-b {
    position: absolute; bottom: 10px; left: 20px; right: 20px; height: 16px;
    background: var(--gold-soft);
    clip-path: polygon(46% 0, 54% 0, 100% 100%, 0 100%);
    animation: fill 3s linear infinite;
}
.hg .stream {
    position: absolute; top: 42px; bottom: 24px; left: 50%; width: 2px;
    margin-left: -1px; background: var(--gold);
    animation: stream 3s linear infinite;
}
@keyframes drain  { 0% {transform: scaleY(1);} 88% {transform: scaleY(.06);} 100% {transform: scaleY(.06);} }
@keyframes fill   { 0% {transform: scaleY(.1);} 88% {transform: scaleY(1);} 100% {transform: scaleY(1);} }
@keyframes stream { 0%,84% {opacity: 1;} 90%,100% {opacity: 0;} }
@keyframes hgflip { 0%,86% {transform: rotate(0);} 96%,100% {transform: rotate(180deg);} }
.hg-caption {
    font-family: 'Cormorant Garamond', serif; font-style: italic;
    color: var(--ink-soft); margin-top: 1rem; font-size: 1.08rem;
}
@media (prefers-reduced-motion: reduce) {
    .hg, .hg .sand-t, .hg .sand-b, .hg .stream { animation: none; }
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f2eee4, #ece6d8);
    border-right: 1px solid rgba(176,141,62,.25);
}
section[data-testid="stSidebar"] .stRadio label { font-family: 'Lato', sans-serif; }

/* ── MÉTRICAS ── */
[data-testid="stMetric"] {
    background: #fffdf8; border: 1px solid rgba(176,141,62,.25);
    border-radius: 8px; padding: .8rem 1rem;
}
h2, h3 { font-family: 'Cinzel', serif !important; color: var(--ink) !important; }

.disclaimer-box {
    background: #f4efe2; border: 1px solid rgba(176,141,62,.3);
    border-radius: 8px; padding: 1rem 1.3rem; margin-top: 1.6rem;
    color: var(--ink-soft); font-size: .84rem; line-height: 1.65; text-align: center;
}

@media (max-width: 640px) {
    .pediment h1 { font-size: 1.6rem; letter-spacing: .18em; }
    .pediment .epithet { font-size: 1rem; }
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════ IA (DeepFace) ═════════════════════════════
@st.cache_resource(show_spinner=False)
def get_deepface():
    from deepface import DeepFace
    return DeepFace


def analizar_imagen(img_bgr, detector="opencv"):
    """Devuelve lista de rostros: [{'persona', 'region', 'emociones', 'dominante'}]"""
    DeepFace = get_deepface()
    try:
        resultados = DeepFace.analyze(
            img_bgr, actions=["emotion"],
            detector_backend=detector, enforce_detection=True, silent=True,
        )
    except ValueError:
        return []
    rostros = []
    for r in resultados:
        reg = r.get("region", {})
        if not reg or reg.get("w", 0) <= 1:
            continue
        rostros.append({
            "region": (reg["x"], reg["y"], reg["w"], reg["h"]),
            "emociones": {EMO_ES[k]: float(v) for k, v in r["emotion"].items()},
            "dominante": EMO_ES[r["dominant_emotion"]],
            "icono": EMO_ICON[r["dominant_emotion"]],
        })
    # Persona 1..N ordenadas de izquierda a derecha (estable entre capturas similares)
    rostros.sort(key=lambda f: f["region"][0])
    for i, f in enumerate(rostros, 1):
        f["persona"] = f"Persona {i}"
    return rostros


def anotar(img_bgr, rostros):
    img = img_bgr.copy()
    for f in rostros:
        x, y, w, h = f["region"]
        cv2.rectangle(img, (x, y), (x + w, y + h), BOX_COLOR, 2)
        etiqueta = f"{f['persona']}: {f['dominante']}"
        (tw, th), _ = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.62, 2)
        cv2.rectangle(img, (x, y - th - 12), (x + tw + 8, y), BOX_COLOR, -1)
        cv2.putText(img, etiqueta, (x + 4, y - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 253, 246), 2)
    return img


def leer_imagen(archivo):
    data = np.frombuffer(archivo.getvalue(), np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


# ═════════════════════════ CONSEJERA DE BIENESTAR ═══════════════════════════
CONSEJOS = {
    "Alegría": {
        "verso": "«La alegría compartida es un templo con las puertas abiertas.»",
        "texto": "Se percibe un estado emocional luminoso. Para cultivarlo: comparte este momento con alguien cercano, anota en un diario qué lo provocó (la gratitud escrita consolida el bienestar) y aprovecha esta energía para actividades creativas o sociales. La alegría se fortalece cuando se reconoce conscientemente.",
    },
    "Serenidad": {
        "verso": "«La calma no es ausencia de tormenta, sino paz en medio de ella.»",
        "texto": "Un estado sereno y equilibrado es terreno fértil para la claridad mental. Es un buen momento para tomar decisiones, planificar o practicar mindfulness. Para sostenerlo: respiración consciente 4-7-8 (inhala 4 s, retén 7 s, exhala 8 s), pausas breves sin pantallas y contacto con la naturaleza.",
    },
    "Tristeza": {
        "verso": "«Hasta los ríos más profundos buscan siempre el mar.»",
        "texto": "Se detectan señales de tristeza. La tristeza es una emoción válida que merece espacio, no supresión. Sugerencias: permítete sentirla sin juicio, busca conversación con una persona de confianza, movimiento suave (caminar 20 minutos eleva el ánimo de forma medible), luz natural y rutinas de sueño estables. Si la tristeza persiste más de dos semanas, afecta el apetito, el sueño o el interés por las cosas, es importante conversar con un profesional de salud mental — pedir ayuda es un acto de sabiduría, no de debilidad.",
    },
    "Enojo": {
        "verso": "«Domina tu ira, o ella hablará por ti.»",
        "texto": "Se perciben señales de enojo o tensión. El enojo suele proteger algo importante: un límite, una necesidad no atendida. Técnicas útiles: pausa de 90 segundos antes de responder (el pico fisiológico del enojo dura ~90 s), respiración prolongada con exhalación lenta, descarga física saludable (caminar rápido, ejercicio), y luego nombrar en palabras qué necesidad fue vulnerada. Expresarlo con asertividad — «me sentí… cuando… y necesito…» — transforma la ira en comunicación.",
    },
    "Miedo": {
        "verso": "«El valor no es la ausencia de miedo, sino avanzar con él de la mano.»",
        "texto": "Se detectan señales de miedo o ansiedad. Para regular el sistema nervioso: técnica de anclaje 5-4-3-2-1 (nombra 5 cosas que ves, 4 que sientes, 3 que oyes, 2 que hueles, 1 que saboreas), respiración diafragmática lenta y reducir cafeína. Pregúntate: ¿este miedo señala un peligro real o una posibilidad imaginada? Escribir el peor escenario y su plan de respuesta reduce su poder. Si la ansiedad interfiere con tu vida diaria, un profesional puede ofrecerte herramientas muy efectivas.",
    },
    "Sorpresa": {
        "verso": "«El asombro es el principio de la sabiduría.»",
        "texto": "La sorpresa indica que algo rompió lo esperado: es la emoción más breve y suele transformarse en otra. Es un buen momento para la curiosidad: pregúntate qué te sorprendió y qué puedes aprender de ello. Si la sorpresa vino de una noticia difícil, date tiempo antes de reaccionar y busca información completa antes de sacar conclusiones.",
    },
    "Desagrado": {
        "verso": "«Escucha lo que rechazas: también habla de ti.»",
        "texto": "El desagrado señala que algo contradice tus valores o bienestar. Es información valiosa sobre tus límites. Sugerencias: identifica con precisión qué lo provocó, evalúa si puedes modificar la situación o tu exposición a ella, y comunica tus límites con respeto. Si es hacia uno mismo, trabaja la autocompasión: háblate como le hablarías a un buen amigo.",
    },
}

CLIMA_GRUPAL = {
    "positivo": "El clima emocional del grupo es predominantemente positivo. Es un momento ideal para colaboración, decisiones conjuntas y celebrar logros. Para sostenerlo: reconocimiento explícito entre los miembros y espacios de escucha.",
    "neutro": "El grupo muestra un clima emocional equilibrado y sereno. Buen terreno para el trabajo concentrado y la planificación. Considera iniciar con una dinámica breve de conexión para elevar la energía si la tarea lo requiere.",
    "tenso": "Se detectan señales de tensión emocional en el grupo (enojo, miedo o desagrado presentes). Recomendaciones: hacer una pausa consciente, validar las preocupaciones antes de resolver («entiendo que esto genera inquietud»), establecer turnos de palabra y, si el conflicto es persistente, considerar un facilitador o mediador. Un grupo que nombra sus tensiones las transforma.",
    "melancolico": "El grupo presenta señales compartidas de tristeza o desánimo. Sugerencias: reconocer colectivamente el momento (evitar el «positivismo forzado»), reducir la carga si es posible, fomentar apoyo entre pares y actividades restauradoras. Si el desánimo es sostenido, el acompañamiento profesional grupal (talleres de bienestar) tiene gran impacto.",
}


def consejo_individual(emociones: dict):
    dominante = max(emociones, key=emociones.get)
    return dominante, CONSEJOS[dominante]


def clima_grupo(promedios: dict):
    pos = promedios.get("Alegría", 0) + promedios.get("Sorpresa", 0) * 0.5
    neg_tension = promedios.get("Enojo", 0) + promedios.get("Miedo", 0) + promedios.get("Desagrado", 0)
    tristeza = promedios.get("Tristeza", 0)
    if neg_tension > 35:
        return "tenso"
    if tristeza > 35:
        return "melancolico"
    if pos > 40:
        return "positivo"
    return "neutro"


# ══════════════════════════════ ESTADO DE SESIÓN ════════════════════════════
if "registros" not in st.session_state:
    st.session_state.registros = []   # [{captura, hora, persona, emociones{}, dominante}]
if "capturas" not in st.session_state:
    st.session_state.capturas = 0


def guardar(rostros):
    st.session_state.capturas += 1
    hora = datetime.now().strftime("%H:%M:%S")
    for f in rostros:
        st.session_state.registros.append({
            "captura": st.session_state.capturas, "hora": hora,
            "persona": f["persona"], "dominante": f["dominante"],
            **f["emociones"],
        })


# ═══════════════════════════════════ SIDEBAR ════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:.6rem 0 .2rem">
        <div style="font-size:1.9rem">🦉</div>
        <div style="font-family:Cinzel,serif;font-weight:700;letter-spacing:.25em;
                    color:#3c4148;font-size:1.25rem">{APP_NAME}</div>
        <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
                    color:#6b7178;font-size:.95rem">{APP_EPITHET}</div>
    </div><hr style="border-color:rgba(176,141,62,.3)">
    """, unsafe_allow_html=True)

    pagina = st.radio("Salas del templo", [
        "🏛️ El Templo",
        "👁️ El Oráculo — Análisis",
        "📜 El Ágora — Dashboard",
        "🌿 El Consejo — Bienestar",
        "ℹ️ Acerca de",
    ], label_visibility="collapsed")

    st.markdown("---")
    detector = st.selectbox("Detector de rostros", ["opencv", "retinaface"],
                            help="opencv: rápido · retinaface: más preciso (descarga ~120 MB la primera vez)")
    st.caption(f"Capturas en esta sesión: **{st.session_state.capturas}** · "
               f"Detecciones: **{len(st.session_state.registros)}**")
    if st.button("🗑️ Limpiar sesión"):
        st.session_state.registros = []
        st.session_state.capturas = 0
        st.rerun()

# ═══════════════════════════════════ FRONTÓN ════════════════════════════════
st.markdown(f"""
<div class="pediment">
    <span class="owl">🦉</span>
    <h1>{APP_NAME[:-1] if len(APP_NAME) > 1 else APP_NAME}<span class="au">{APP_NAME[-1]}</span></h1>
    <div class="epithet">{APP_EPITHET}</div>
    <div class="laurel-line"><span class="stem"></span><span class="leaf">🌿 ⚭ 🌿</span><span class="stem"></span></div>
    <div class="tagline">{APP_TAGLINE}</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════ PÁG. 1: TEMPLO ═════════════════════════════
if pagina.startswith("🏛️"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="stele"><h3>👁️ El Oráculo</h3>
        <p>Captura una foto con tu cámara o sube una imagen. La IA detecta <span class="gold">todos los rostros presentes</span>
        y reconoce <span class="gold">7 emociones</span> en cada uno: alegría, tristeza, enojo, miedo, sorpresa, desagrado y serenidad.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="stele"><h3>📜 El Ágora</h3>
        <p>Un <span class="gold">dashboard emocional</span> con la historia de la sesión: perfil de cada persona,
        clima del grupo, evolución en el tiempo y la emoción que reina en el conjunto.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="stele"><h3>🌿 El Consejo</h3>
        <p>Recomendaciones de <span class="gold">bienestar emocional</span> personalizadas para cada persona
        y para el grupo, con técnicas respaldadas por la psicología: respiración, anclaje, gratitud y más.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="stele"><h3>Cómo usar el santuario</h3>
    <p><b>1.</b> Entra a <b>El Oráculo</b> y captura una o varias fotos (individuales o grupales).
    <b>2.</b> Cada análisis se guarda en la sesión. <b>3.</b> Visita <b>El Ágora</b> para ver el dashboard
    y <b>El Consejo</b> para recibir las recomendaciones. Cuantas más capturas hagas, más rica será la lectura emocional.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="disclaimer-box">🌿 <b>Aviso:</b> esta herramienta es educativa y de apoyo al bienestar.
    La expresión facial es solo una ventana parcial a la emoción real. No constituye evaluación psicológica ni diagnóstico.
    Si atraviesas un momento difícil, busca a un profesional de salud mental.</div>""", unsafe_allow_html=True)

# ═══════════════════════════════ PÁG. 2: ORÁCULO ════════════════════════════
elif pagina.startswith("👁️"):
    st.markdown("## 👁️ El Oráculo")
    st.markdown("""<div class="stele"><p>Presenta tu rostro —o los de tu grupo— ante el oráculo.
    Puedes <span class="gold">capturar con la cámara</span> o <span class="gold">subir una imagen</span>.
    Cada lectura queda registrada en la sesión para el Ágora y el Consejo.</p></div>""", unsafe_allow_html=True)

    tab_cam, tab_up = st.tabs(["📷 Cámara", "🖼️ Subir imagen"])
    imagen = None
    with tab_cam:
        foto = st.camera_input("Captura una foto", label_visibility="collapsed")
        if foto:
            imagen = leer_imagen(foto)
    with tab_up:
        archivo = st.file_uploader("Sube una imagen (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if archivo:
            imagen = leer_imagen(archivo)

    if imagen is not None:
        with st.spinner("El oráculo contempla los rostros…"):
            rostros = analizar_imagen(imagen, detector)
        if not rostros:
            st.warning("El oráculo no encontró rostros claros en la imagen. Intenta con mejor luz y de frente.")
        else:
            guardar(rostros)
            anotada = anotar(imagen, rostros)
            st.image(cv2.cvtColor(anotada, cv2.COLOR_BGR2RGB),
                     caption=f"Lectura n.º {st.session_state.capturas} · {len(rostros)} rostro(s) detectado(s)",
                     use_container_width=True)

            cols = st.columns(min(len(rostros), 4))
            for i, f in enumerate(rostros):
                with cols[i % len(cols)]:
                    st.markdown(f"""<div class="oracle">
                        <h4>{f['icono']} {f['persona']} — {f['dominante']}</h4>
                        <p>{' · '.join(f"{e}: {v:.0f}%" for e, v in
                            sorted(f['emociones'].items(), key=lambda kv: -kv[1])[:3])}</p>
                    </div>""", unsafe_allow_html=True)
            st.success("Lectura guardada. Visita **El Ágora** para el dashboard y **El Consejo** para las recomendaciones.")

# ═══════════════════════════════ PÁG. 3: ÁGORA ══════════════════════════════
elif pagina.startswith("📜"):
    st.markdown("## 📜 El Ágora — Dashboard emocional")

    if not st.session_state.registros:
        st.info("Aún no hay lecturas en esta sesión. Visita primero **El Oráculo** y captura algunas fotos.")
    else:
        # ── Reloj de arena de Mnemósine mientras se calculan los datos ──
        escena = st.empty()
        escena.markdown("""
        <div class="hourglass-scene">
            <div class="hg">
                <div class="frame-t"></div><div class="bulb-t"></div><div class="sand-t"></div>
                <div class="stream"></div><div class="bulb-b"></div><div class="sand-b"></div>
                <div class="frame-b"></div>
            </div>
            <div class="hg-caption">Mnemósine, madre de las musas, ordena los recuerdos de la sesión…</div>
        </div>""", unsafe_allow_html=True)

        df = pd.DataFrame(st.session_state.registros)
        emo_cols = list(EMO_COLOR.keys())
        time.sleep(2.2)  # el reloj de arena honra el proceso
        escena.empty()

        # ── Métricas del grupo ──
        prom_grupo = df[emo_cols].mean().to_dict()
        emocion_reina = max(prom_grupo, key=prom_grupo.get)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Lecturas", st.session_state.capturas)
        c2.metric("Personas por lectura (máx.)", df.groupby("captura")["persona"].count().max())
        c3.metric("Emoción reinante", emocion_reina)
        c4.metric("Intensidad media", f"{prom_grupo[emocion_reina]:.0f}%")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### El alma del grupo")
            pie = px.pie(values=list(prom_grupo.values()), names=list(prom_grupo.keys()),
                         color=list(prom_grupo.keys()), color_discrete_map=EMO_COLOR, hole=.45)
            pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(family="Lato"), margin=dict(t=10, b=10, l=10, r=10), height=340)
            st.plotly_chart(pie, use_container_width=True)

        with col_b:
            st.markdown("### Perfil por persona")
            perfil = df.groupby("persona")[emo_cols].mean().reset_index()
            barras = go.Figure()
            for emo in emo_cols:
                barras.add_bar(name=emo, x=perfil["persona"], y=perfil[emo],
                               marker_color=EMO_COLOR[emo])
            barras.update_layout(barmode="stack", paper_bgcolor="rgba(0,0,0,0)",
                                 plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Lato"),
                                 margin=dict(t=10, b=10, l=10, r=10), height=340,
                                 yaxis_title="%", legend=dict(orientation="h", y=-0.25))
            st.plotly_chart(barras, use_container_width=True)

        # ── Radar individual ──
        st.markdown("### El espejo de cada alma")
        personas = sorted(df["persona"].unique())
        sel = st.selectbox("Elige una persona", personas)
        pd_sel = df[df["persona"] == sel][emo_cols].mean()
        radar = go.Figure(go.Scatterpolar(
            r=list(pd_sel.values) + [pd_sel.values[0]],
            theta=emo_cols + [emo_cols[0]],
            fill="toself", line=dict(color="#b08d3e", width=2),
            fillcolor="rgba(176,141,62,.22)"))
        radar.update_layout(polar=dict(radialaxis=dict(range=[0, 100], showticklabels=True)),
                            paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Lato"),
                            margin=dict(t=30, b=30), height=380, showlegend=False)
        st.plotly_chart(radar, use_container_width=True)

        # ── Evolución temporal ──
        if st.session_state.capturas > 1:
            st.markdown("### El río del tiempo")
            evol = df.groupby("captura")[emo_cols].mean().reset_index()
            linea = go.Figure()
            for emo in emo_cols:
                linea.add_scatter(x=evol["captura"], y=evol[emo], name=emo,
                                  mode="lines+markers", line=dict(color=EMO_COLOR[emo], width=2))
            linea.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(family="Lato"), height=340,
                                xaxis_title="Lectura", yaxis_title="%",
                                margin=dict(t=10, b=10), legend=dict(orientation="h", y=-0.3))
            st.plotly_chart(linea, use_container_width=True)

        # ── Exportar ──
        st.download_button("⬇️ Descargar registros (CSV)",
                           df.to_csv(index=False).encode("utf-8"),
                           "registros_emocionales.csv", "text/csv")

# ═══════════════════════════════ PÁG. 4: CONSEJO ════════════════════════════
elif pagina.startswith("🌿"):
    st.markdown("## 🌿 El Consejo — Bienestar emocional")

    if not st.session_state.registros:
        st.info("Aún no hay lecturas en esta sesión. Visita primero **El Oráculo**.")
    else:
        df = pd.DataFrame(st.session_state.registros)
        emo_cols = list(EMO_COLOR.keys())

        # ── Consejo grupal ──
        prom_grupo = df[emo_cols].mean().to_dict()
        clima = clima_grupo(prom_grupo)
        titulos_clima = {"positivo": "☀️ Clima luminoso", "neutro": "🕊️ Clima sereno",
                         "tenso": "🌩️ Clima en tensión", "melancolico": "🌧️ Clima melancólico"}
        if df["persona"].nunique() > 1 or st.session_state.capturas > 1:
            st.markdown("### Para el grupo")
            st.markdown(f"""<div class="oracle"><h4>{titulos_clima[clima]}</h4>
            <p>{CLIMA_GRUPAL[clima]}</p></div>""", unsafe_allow_html=True)

        # ── Consejo por persona ──
        st.markdown("### Para cada persona")
        for persona in sorted(df["persona"].unique()):
            prom = df[df["persona"] == persona][emo_cols].mean().to_dict()
            dominante, consejo = consejo_individual(prom)
            icono = [ic for k, ic in EMO_ICON.items() if EMO_ES[k] == dominante][0]
            secundaria = sorted(prom.items(), key=lambda kv: -kv[1])[1]
            st.markdown(f"""<div class="oracle">
                <h4>{icono} {persona} — predomina la {dominante.lower()}
                    <span style="font-size:.85rem;color:#6b7178">(acompañada de {secundaria[0].lower()}, {secundaria[1]:.0f}%)</span></h4>
                <p class="verse">{consejo['verso']}</p>
                <p>{consejo['texto']}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="disclaimer-box">🌿 Estas recomendaciones son de carácter general y educativo,
        inspiradas en técnicas de psicología del bienestar. No reemplazan la atención de un psicólogo o psiquiatra.
        Si tú o alguien de tu grupo atraviesa un momento emocional difícil o persistente, buscar ayuda profesional
        es el acto más sabio. En Perú puedes llamar gratuitamente a la <b>Línea 113, opción 5</b> (salud mental, MINSA).</div>""",
                    unsafe_allow_html=True)

# ═══════════════════════════════ PÁG. 5: ACERCA ═════════════════════════════
else:
    st.markdown("## ℹ️ Acerca de")
    st.markdown(f"""<div class="stele">
    <h3>{APP_NAME} — {APP_EPITHET}</h3>
    <p>Aplicación de reconocimiento de emociones faciales multi-persona construida con
    <span class="gold">DeepFace</span> (análisis de 7 emociones con redes neuronales profundas),
    <span class="gold">OpenCV</span> para el procesamiento de imagen,
    <span class="gold">Plotly</span> para el dashboard y <span class="gold">Streamlit</span> como interfaz.
    Sucesora del proyecto ARTEMISA (CNN propia de 5 emociones), esta versión detecta
    múltiples rostros por imagen, amplía el espectro emocional, añade el dashboard del Ágora
    y la consejería de bienestar de El Consejo.</p>
    </div>
    <div class="stele"><h3>Privacidad</h3>
    <p>Las imágenes se procesan en memoria durante la sesión y no se almacenan de forma permanente.
    Los registros emocionales viven solo en tu sesión del navegador y desaparecen al cerrarla
    (o con el botón «Limpiar sesión»). El uso de análisis emocional con terceros requiere siempre
    su consentimiento informado.</p></div>
    <div class="stele"><h3>Créditos</h3>
    <p>Proyecto original: Luciana de los Ángeles Herrera Cooper · Desarrollo: Miguel Alexander Herrera Cooper.
    Modelos: DeepFace (Sefik Ilkin Serengil, MIT License).</p></div>
    """, unsafe_allow_html=True)
