# src/viewercode/vcpygments.py
# Ya no necesitamos matplotlib.pyplot aquí, así que lo quitamos.
# import matplotlib.pyplot as plt 
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token
import tkinter.font as tkFont # Necesario para obtener información de fuentes

PYGMENTS_STYLE = get_style_by_name('default') # O elige 'monokai', 'solarized-dark' etc.

def display_code_with_highlighting(ctk_textbox_widget, python_code: str):
    """
    Muestra código Python en un widget CTkTextbox con resaltado de sintaxis.
    Opera en el widget subyacente tkinter.Text para la inserción basada en etiquetas.

    Args:
        ctk_textbox_widget: El widget customtkinter.CTkTextbox.
        python_code: Una cadena que contiene el código Python a mostrar.
    """
    if not ctk_textbox_widget:
        print("Error: ctk_textbox_widget is None.")
        return
    if not hasattr(ctk_textbox_widget, '_textbox'):
        print("Error: ctk_textbox_widget does not have a '_textbox' attribute. Is it a CTkTextbox?")
        return
        
    if not isinstance(python_code, str):
        print("Error: python_code is not a string.")
        ctk_textbox_widget.configure(state="normal")
        ctk_textbox_widget.delete("1.0", "end")
        ctk_textbox_widget.insert("1.0", "Error: Invalid code input.")
        ctk_textbox_widget.configure(state="disabled")
        return

    ctk_textbox_widget.configure(state="normal")
    ctk_textbox_widget.delete("1.0", "end")

    tk_textbox = ctk_textbox_widget._textbox

    # --- NUEVO: Obtener la familia y el tamaño de la fuente actual del CTkTextbox ---
    font_family = "TkDefaultFont" # Valor por defecto seguro
    font_size = 10 # Valor por defecto seguro

    # Intentar obtener la configuración de la fuente del CTkTextbox
    # customtkinter stores font as a tuple (family, size, styles) or a font object name
    try:
        current_font_config = ctk_textbox_widget.cget("font")
        if isinstance(current_font_config, str):
            # If it's a font name string (e.g., "TkDefaultFont"), convert to actual font object
            default_font_obj = tkFont.nametofont(current_font_config)
            font_family = default_font_obj.actual("family")
            font_size = default_font_obj.actual("size")
        elif isinstance(current_font_config, tuple) and len(current_font_config) >= 2:
            # If it's a tuple (family, size, ...), extract family and size
            font_family = current_font_config[0]
            font_size = current_font_config[1]
        # Ensure size is an integer, as Tkinter expects it for font tuples
        if not isinstance(font_size, int):
            font_size = 10 # Fallback if size couldn't be determined as integer
    except Exception as e:
        print(f"Warning: Could not determine CTkTextbox font, falling back to default. Error: {e}")
        # Defaults (TkDefaultFont, 10) are already set above.
    # --- FIN DE OBTENCIÓN DE FUENTE ---


    # Limpiar etiquetas existentes
    for tag in tk_textbox.tag_names():
        tk_textbox.tag_delete(tag)

    # Configurar las etiquetas según el estilo de Pygments elegido
    for token_type, style_dict in PYGMENTS_STYLE:
        tag_name = str(token_type)
        
        config_kwargs = {} # Diccionario para construir los argumentos de configuración de la etiqueta

        # Configurar el color de primer plano (texto)
        if 'color' in style_dict and style_dict['color']:
            config_kwargs['foreground'] = f"#{style_dict['color']}"
        
        # Configurar el color de fondo (si el estilo lo define, por ejemplo para errores)
        if 'bgcolor' in style_dict and style_dict['bgcolor']:
            config_kwargs['background'] = f"#{style_dict['bgcolor']}"
        
        font_styles = []
        if style_dict.get('bold'):
            font_styles.append('bold')
        if style_dict.get('italic'):
            font_styles.append('italic')
        
        # --- FIX APLICADO AQUÍ (USANDO FUENTE Y TAMAÑO REALES) ---
        # Solo aplicar el argumento 'font' si hay estilos de fuente que aplicar.
        # Usamos la familia y el tamaño de fuente que hemos extraído del CTkTextbox.
        if font_styles:
            config_kwargs['font'] = (font_family, font_size, " ".join(font_styles))

        # Aplicar la configuración de la etiqueta si hay argumentos para configurar
        if config_kwargs:
            tk_textbox.tag_config(tag_name, **config_kwargs)

    # Ahora procede a lexar e insertar el código con las etiquetas ya configuradas
    lexer = PythonLexer()
    for token_type, token_value in lex(python_code, lexer):
        tag_name = str(token_type)
        tk_textbox.insert("end", token_value, (tag_name,))

    # Usar el método de CTkTextbox para establecer el estado final
    ctk_textbox_widget.configure(state="disabled")