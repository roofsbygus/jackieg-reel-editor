# Perlili Video Editor

**Editor de video con IA para reels, en español y en inglés.** Grabas un video hablando a la cámara con tu teléfono, se lo das a Claude en tu Mac, y te regresa un reel vertical (1080×1920) terminado: sin pausas ni muletillas, con subtítulos y con tu marca. Tú apruebas cada corte antes de que se haga.

> **Estado: versión 1.0 (uso interno de Trust In Gus y pruebas con LERU).** Se instala en una Mac con chip Apple. Las lecciones en español para LERU vienen después.

## Instalar (una sola vez)

Necesitas una Mac con chip Apple (M1 o más nuevo), macOS 13 o más nuevo, unos 15 GB libres, un plan de pago de Claude (cada quien su cuenta) y la app de Claude para escritorio.

1. Instala **Homebrew** tú mismo con el instalador `.pkg` de [brew.sh](https://brew.sh) (te pide la contraseña de tu Mac; Claude nunca la escribe).
2. Abre la app de Claude y ve a la pestaña **Code**.
3. Agrega el editor (dos líneas, una sola vez):
   ```
   /plugin marketplace add roofsbygus/perlili-video-editor
   /plugin install perlili-video-editor@latinos-en-roofing
   ```
   *(Mientras este repositorio sea privado, solo funciona para quien tenga acceso en GitHub. Otra opción: abre la carpeta del editor en la pestaña Code.)*
4. Escribe: **"instala mi editor Perlili"**.

Claude corre `install.sh`, que hace 7 pasos fijos: revisa tu Mac, instala FFmpeg, Node.js, Whisper y uv con Homebrew (solo los que falten), el motor de video en su versión fija, las plantillas, el modelo de subtítulos (~3 GB), la limpieza de ruido (~1 GB) y conecta el editor con Claude. Termina con la revisión del sistema: **LISTO ✅**, **LISTO CON LÍMITES ⚠️** o **FALTA ALGO ❌**, con la solución en español. Puedes volver a correrlo cuando quieras: lo que ya está se salta. Para revisar después: **"revisa mi editor Perlili"**.

Después, en cualquier chat de la pestaña Code: **"edita mi reel"**. La primera vez te hace 5 minutos de preguntas sobre tu marca.

**¿Más de una marca?** (tu negocio, un cliente, LERU) Cada marca vive en su propia carpeta dentro de `~/reels/`, con sus colores, letras, logos y reels. Di **"configura una marca nueva para <nombre>"** para crearla, y luego **"edita mi reel de <nombre>"**: Claude usa la carpeta de esa marca. Si tienes varias y no dices cuál, te pregunta.

## Qué hace

- **Subtítulos en español, en inglés y en Spanglish.** Detecta el idioma solo. También **traducidos** (hablas en español, subtítulos en inglés, o al revés) o **bilingües** (dos líneas). Tú revisas la traducción antes de quemarla en el video.
- **Quita pausas y muletillas** en español e inglés ("eh", "este", "o sea", "pues", "bueno"), con el ritmo que elijas (natural, rápido o muy rápido).
- **Limpia el ruido de obra y viento** y deja tu voz al volumen que piden Instagram y TikTok.
- **Junta varios videos en un reel** (en el orden en que los grabaste, o el que tú digas).
- **Tu marca en todo:** colores, letras, logos, estilo de subtítulos y gráficos. Varias marcas en la misma Mac.
- **Música con licencia**, **portada/miniatura**, **texto para publicar** (caption, hashtags, título de Shorts).
- **Página de revisión:** tocas las palabras que quieres cortar, ves el corte en vivo y apruebas antes de crear el video.
- **Seguro por diseño:** tus videos originales nunca se modifican ni se borran; versiones fijas, sin telemetría ni actualizaciones automáticas; reglas para que Claude no use `sudo`, no corra scripts descargados y no borre videos.

## ¿Cuesta algo?

| Qué | Costo |
|---|---|
| El editor, Whisper, FFmpeg, el motor de video, la limpieza de ruido | **Gratis**, todo corre en tu Mac |
| Claude (pestaña Code) | Tu plan de pago de Claude (Pro o más) |
| ElevenLabs (subtítulos en la nube) | **Opcional, cobra.** Apagado si no lo prendes tú; sube tu audio |
| WoopSocial (borradores para redes) | Opcional; según tu cuenta de WoopSocial |
| CapCut | Opcional; el MP4 funciona sin CapCut |

**Velocidad:** todo usa la fuerza de tu Mac. Con 8 GB de memoria funciona, pero más lento (la revisión avisa con `PV-MEMORIA`); con 16 GB o más va mejor. La primera vez descarga ~4 GB (modelo de subtítulos y limpieza de ruido) y ~200 MB más al crear el primer video.

## Créditos

Basado en [claude-reel-editor](https://github.com/nicolapocock/claude-reel-editor) de **Nicola Pocock** ([@getgitgirl](https://instagram.com/getgitgirl)), licencia MIT. Gracias, Nicola. El README y las guías originales (en inglés) están en [docs/upstream/](docs/upstream/), solo como referencia.

Usa [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache-2.0, de HeyGen) para transcribir y armar el video. Perlili no está afiliado con HeyGen. Detalles en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Hecho por [Perlili Development Studio](https://perlili.dev) para Trust In Gus Contracting y LERU (Latinos En Roofing University).

---

**English:** a Perlili fork of claude-reel-editor with automatic Spanish/English/Spanglish captions, Spanish filler words, pinned versions and telemetry off. Version 1.0, packaged as a Claude Code plugin: `/plugin marketplace add roofsbygus/perlili-video-editor`, then `/plugin install perlili-video-editor@latinos-en-roofing`, then say "instala mi editor Perlili" in the Code tab (runs `scripts/install.sh`). Licensed under [MIT](LICENSE); see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
