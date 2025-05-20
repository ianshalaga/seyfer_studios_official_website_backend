class DatabaseAccessError(Exception):
    pass


class ScraperError(Exception):
    pass


class DynamicRequestError(Exception):
    pass


def build_detailed_error(exception: Exception) -> str:
    tb = exception.__traceback__

    while tb.tb_next:
        tb = tb.tb_next

    frame = tb.tb_frame
    filename = frame.f_code.co_filename
    func_name = frame.f_code.co_name
    line_no = tb.tb_lineno
    error_message = str(exception)
    error_type = exception.__class__.__name__

    suggestions = {
        "ScraperError": "📎 Verifica si la estructura HTML del sitio cambió.",
        "DatabaseAccessError": "🔌 Revisa la conexión a la base de datos o el estado del modelo.",
        "DynamicRequestError": "🌐 Asegúrate de que la URL esté activa o que el navegador headless esté funcionando.",
        "ValueError": "🧮 Verifica el tipo y rango de datos ingresados.",
        "TypeError": "🧩 Revisa si estás usando los tipos de datos correctos.",
        "KeyError": "🗝️ Asegúrate de que la clave exista en el diccionario.",
    }

    suggestion = suggestions.get(
        error_type, "🛠️ Revisa el traceback completo para más detalles.")

    return (
        f"\n"
        f"🛑 Exception: {error_type}\n"
        f"Filename   : {filename}\n"
        f"Method     : {func_name}()\n"
        f"Line       : {line_no}\n"
        f"Description: {error_message}\n"
        f"Suggestion : {suggestion}"
    )
