# ASISTENTE MR MENTOR

Bot educativo en español para organizar sesiones de estudio con Python 3.12 y aiogram 3.

## Funciones

1. **Crear plan**: escribe una materia o tema y selecciona 30, 60 o 90 minutos; recibe un plan con bloques cronometrados.
2. **Consejo de estudio**: muestra recomendaciones breves de organización, concentración y repaso.
3. **Ayuda**: explica cómo usar el bot.

Comandos: /start, /help, /about, /cancel.

No usa IA externa ni promete resultados académicos. No tiene pagos, enlaces promocionales ni redirecciones. Los temas de estudio se guardan solo temporalmente en memoria durante la sesión.

## Perfil de Telegram integrado en el código

En `main.py` están definidos:
- `BOT_NAME`: nombre visible.
- `BOT_ABOUT`: descripción corta / About.
- `BOT_DESCRIPTION`: descripción detallada.

Al arrancar, el bot intenta configurar automáticamente el nombre, About, Description y comandos mediante la API oficial de Telegram. **La foto de perfil debe configurarse manualmente en @BotFather**. Verifica en Telegram que los cambios se hayan aplicado.

## Despliegue en Render (Background Worker)

1. Crea el bot con @BotFather y conserva el token de forma privada.
2. Conecta este repositorio a un servicio **Background Worker** en Render.
3. Selecciona Docker como runtime (se usa el Dockerfile incluido).
4. Añade `BOT_TOKEN` como variable de entorno secreta. Nunca guardes el token en GitHub.
5. Despliega y comprueba los logs del servicio.
6. Prueba /start, los tres botones y la generación de planes de 30, 60 y 90 minutos.

Ejecuta una sola instancia de polling por token para evitar conflictos de getUpdates.

## Ejecución local

```bash
python -m pip install -r requirements.txt
export BOT_TOKEN="TU_TOKEN_PRIVADO"
python main.py
```

## Pruebas

```bash
python -m unittest discover -p "test_*.py" -v
```

## Texto publicitario sugerido

**Título:** ASISTENTE MR MENTOR – Plan de estudio

**Texto:** Organiza tus sesiones de estudio con ASISTENTE MR MENTOR. Crea planes de 30, 60 o 90 minutos y consulta consejos prácticos en Telegram.

**Destino:** el enlace t.me de la cuenta real del bot.

Antes de enviar un anuncio, confirma que la foto, About, Description, comandos y botones están activos, y que el texto refleja exactamente las funciones disponibles. La aprobación depende de la revisión de Telegram.
