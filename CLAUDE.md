# Editor de video Perlili

Las personas que usan esta carpeta son alumnos de LERU y clientes de Perlili. Todo lo que vean (mensajes, botones, resúmenes) va en español, salvo que te hablen en inglés.

## "Instala mi editor Perlili" (o "instala el editor", "set up the editor")

1. Corre `bash skills/perlili-video-editor/scripts/install.sh` (puede tardar varios minutos la primera vez: córrelo en segundo plano y avisa en qué paso va).
2. Si para con ❌ y un código `PV-...`, explica la solución que imprimió con palabras sencillas. Homebrew y cualquier cosa que pida la contraseña de la Mac la instala la persona, nunca tú.
3. Al final, si la revisión dice que faltan las reglas de seguridad (`PV-REGLAS`), ofrece aplicarlas: muestra qué hace `settings/perlili-permisos.json`, pide su "sí", haz una copia de `~/.claude/settings.json` antes y júntalas sin borrar lo que ya tenga.
4. Diles que ya pueden decir "edita mi reel" en cualquier chat de la pestaña Code.

Nunca uses `npx -y`, `sudo` ni scripts descargados con `curl | sh`. Nunca borres ni cambies sus videos originales.
