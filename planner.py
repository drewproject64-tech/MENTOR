"""Deterministic study schedules; no third-party AI service is used."""

SCHEDULES = {
    30: [
        (20, "Estudia las ideas principales"),
        (5, "Comprueba lo aprendido con preguntas"),
        (5, "Resume los puntos clave"),
    ],
    60: [
        (25, "Estudia las ideas principales"),
        (5, "Haz una pausa breve"),
        (25, "Practica con ejemplos o ejercicios"),
        (5, "Resume lo aprendido"),
    ],
    90: [
        (25, "Estudia las ideas principales"),
        (5, "Haz una pausa breve"),
        (25, "Practica con ejemplos o ejercicios"),
        (5, "Haz una pausa breve"),
        (25, "Repasa lo difícil y comprueba tus respuestas"),
        (5, "Resume lo aprendido"),
    ],
}


def make_plan(topic: str, minutes: int) -> str:
    """Return a plain-text timetable totaling the requested number of minutes."""
    topic = " ".join(topic.strip().split())
    if not 2 <= len(topic) <= 80:
        raise ValueError("El tema debe tener entre 2 y 80 caracteres.")
    if minutes not in SCHEDULES:
        raise ValueError("Duración no admitida.")
    lines = [f"Plan de estudio: {topic}", f"Duración total: {minutes} minutos", ""]
    for index, (duration, activity) in enumerate(SCHEDULES[minutes], 1):
        lines.append(f"{index}. {activity} — {duration} min")
    lines += ["", "Sugerencia: silencia las notificaciones durante la sesión."]
    return "\n".join(lines)
