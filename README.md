# Perlili Video Editor

**Editor de video con IA para reels, en español y en inglés.** Grabas un video hablando a la cámara con tu teléfono, se lo das a Claude en tu Mac, y te regresa un reel vertical (1080×1920) terminado: sin pausas ni muletillas, con subtítulos y con tu marca. Tú apruebas cada corte antes de que se haga.

> **Estado: versión 1 (uso interno de Trust In Gus y pruebas con LERU).** Ya se puede instalar en una Mac con chip Apple. Las lecciones en español para LERU vienen después.

## Instalar (una sola vez)

Necesitas una Mac con chip Apple (M1 o más nuevo), macOS 13 o más nuevo, unos 15 GB libres y la app de Claude para escritorio.

1. Instala **Homebrew** tú mismo con el instalador `.pkg` de [brew.sh](https://brew.sh) (te pide la contraseña de tu Mac; Claude nunca la escribe).
2. Abre la app de Claude, ve a la pestaña **Code** y abre la carpeta de este editor.
3. Escribe: **"instala mi editor Perlili"**.

Claude corre `skills/perlili-video-editor/scripts/install.sh`, que hace 7 pasos fijos: revisa tu Mac, instala FFmpeg, Node.js, Whisper y uv con Homebrew (solo los que falten), el motor de video en su versión fija, las plantillas, el modelo de subtítulos (~3 GB), la limpieza de ruido (~1 GB) y conecta el editor con Claude. Termina con la revisión del sistema: **LISTO ✅**, **LISTO CON LÍMITES ⚠️** o **FALTA ALGO ❌**, con la solución en español. Puedes volver a correrlo cuando quieras: lo que ya está se salta.

Después, en cualquier chat de la pestaña Code: **"edita mi reel"**. La primera vez te hace 5 minutos de preguntas sobre tu marca.

## Qué va a cambiar respecto al original (versión 1, en desarrollo)

- **Subtítulos en español, en inglés y en Spanglish.** El idioma se detecta solo, y puedes traducir de uno al otro (revisas la traducción antes de quemarla en el video). El original usaba un modelo solo para inglés y convertía el español en inglés inventado.
- **Muletillas en español** ("eh", "este", "o sea", "pues", "bueno").
- **Versiones fijas, sin telemetría y sin actualizaciones automáticas.** Nada cambia sin que Perlili lo pruebe primero.
- **Instalación con pasos fijos y revisados**, más un chequeo del sistema con ✅/❌ y soluciones en español.
- **Tus videos originales nunca se modifican ni se borran.**

## Créditos

Basado en [claude-reel-editor](https://github.com/nicolapocock/claude-reel-editor) de **Nicola Pocock** ([@getgitgirl](https://instagram.com/getgitgirl)), licencia MIT. Gracias, Nicola. El README original está en [docs/upstream-README.md](docs/upstream-README.md).

Usa [HyperFrames](https://github.com/heygen-com/hyperframes) (Apache-2.0, de HeyGen) para transcribir y armar el video. Perlili no está afiliado con HeyGen. Detalles en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Hecho por [Perlili Development Studio](https://perlili.dev) para Trust In Gus Contracting y LERU (Latinos En Roofing University).

---

**English:** a Perlili fork of claude-reel-editor with automatic Spanish/English/Spanglish captions, Spanish filler words, pinned versions and telemetry off. Version 1: install it from the Claude desktop app's Code tab by saying "instala mi editor Perlili" (runs `skills/perlili-video-editor/scripts/install.sh`). Licensed under [MIT](LICENSE); see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
