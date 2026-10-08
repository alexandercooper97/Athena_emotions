# 🦉 ATHENA — Santuario de las Emociones

Detección de emociones faciales **multi-persona** con IA (7 emociones), dashboard emocional individual y grupal, y consejera de bienestar emocional. Estética inspirada en la serenidad y majestuosidad del Monte Olimpo.

> Sucesora del proyecto ARTEMISA. Motor de IA: **DeepFace** (redes neuronales profundas, MIT License) — detecta todos los rostros de una imagen y clasifica 7 emociones: alegría, tristeza, enojo, miedo, sorpresa, desagrado y serenidad.

> 🌿 Herramienta educativa y de apoyo al bienestar. No constituye evaluación psicológica ni diagnóstico.

## ✏️ ATHENA

Abre `app.py` y edita las dos primeras constantes:

```python
APP_NAME = "LUCIANA"
APP_EPITHET = "La Portadora de Luz"
```

## 🏛️ Salas del templo

- **🏛️ El Templo** — bienvenida y guía de uso.
- **👁️ El Oráculo** — captura con cámara o sube una imagen; detecta todos los rostros y sus emociones.
- **📜 El Ágora** — dashboard con reloj de arena animado ("Mnemósine ordena los recuerdos"): emoción reinante, alma del grupo (dona), perfil por persona (barras apiladas), espejo de cada alma (radar) y río del tiempo (evolución). Exporta CSV.
- **🌿 El Consejo** — recomendaciones de bienestar por persona y clima grupal, con técnicas de psicología (respiración 4-7-8, anclaje 5-4-3-2-1, pausa de 90 segundos, etc.).

## ▶️ Ejecutar en tu computadora

1. Instala **Python 3.10 u 3.11** ([python.org](https://www.python.org/downloads/), en Windows marca "Add Python to PATH").
2. Abre una terminal en esta carpeta e instala dependencias (la primera vez tarda varios minutos, TensorFlow es grande):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta:
   ```bash
   streamlit run app.py
   ```
4. Se abre en http://localhost:8501. El navegador pedirá **permiso para usar la cámara** — acéptalo.

**Nota:** la primera vez que analices una imagen, DeepFace descargará automáticamente los pesos del modelo (~6 MB; ~120 MB si eliges el detector retinaface). Requiere internet solo esa primera vez.

## 🌐 Publicarla gratis en internet (Streamlit Community Cloud)

1. Sube esta carpeta a un repositorio de [GitHub](https://github.com).
2. En [share.streamlit.io](https://share.streamlit.io): **New app** → tu repositorio → `app.py` → **Deploy**.
3. Comparte el enlace `https://tu-usuario-athena.streamlit.app`. La cámara funciona desde el navegador del celular también (el sitio usa HTTPS, requisito para el permiso de cámara).

**Consejo de despliegue:** en el plan gratuito (1 GB RAM) usa el detector `opencv` (por defecto). El detector `retinaface` es más preciso pero pesado; ideal si corres la app en una máquina propia.

## 🧩 Problemas frecuentes

| Problema | Solución |
|---|---|
| `pip` no se reconoce | `python -m pip install -r requirements.txt` |
| La cámara no aparece | Acepta el permiso del navegador; la página debe estar en `localhost` o HTTPS |
| Primera predicción lenta | Es la descarga/carga inicial del modelo; las siguientes son rápidas |
| Memoria insuficiente en la nube | Mantén el detector `opencv` |

## 🔒 Privacidad

Las imágenes se procesan en memoria y no se almacenan. Los registros emocionales viven solo en la sesión del navegador. El análisis emocional de terceros requiere su consentimiento informado.
