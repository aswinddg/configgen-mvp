from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from ..core.settings import settings

def render_template(template_path: str, context: dict) -> str:
    # Obtener la ruta absoluta del directorio de templates
    template_dir = os.path.abspath(settings.TEMPLATE_DIR)

    # Crear el entorno de Jinja2
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Cargar y renderizar la plantilla
    template = env.get_template(template_path)
    return template.render(context)
    