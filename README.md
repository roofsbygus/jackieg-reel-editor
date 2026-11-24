# Perlili Video Editor

**Editor de video con IA para reels, en español y en inglés.** Grabas un video hablando a la cámara con tu teléfono, se lo das a Claude en tu Mac, y te regresa un reel vertical (1080×1920) terminado: sin pausas ni muletillas, con subtítulos y con tu marca. Tú apruebas cada corte antes de que se haga.

> **Estado: en construcción (uso interno de Trust In Gus).** Todavía no está listo para instalar. Las instrucciones de instalación, el chequeo del sistema y las lecciones en español para LERU vienen después.

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

**English:** a Perlili fork of claude-reel-editor with automatic Spanish/English/Spanglish captions, Spanish filler words, pinned versions and telemetry off. It's a work in progress and not ready to install yet. Licensed under [MIT](LICENSE); see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
