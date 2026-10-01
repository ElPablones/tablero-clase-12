import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.set_page_config(page_title="Tablero de Dibujo", layout="wide")
st.title("Tablero para dibujo 🎨")

with st.sidebar:
    st.header("Herramientas")
    
    # Agrupación de controles de trazo
    with st.expander("✏️ Configuración de Trazo", expanded=True):
        drawing_mode = st.selectbox(
            "Modo:",
            ("freedraw", "line", "rect", "circle", "transform", "polygon", "point")
        )
        stroke_width = st.slider('Grosor del trazo', 1, 30, 15)
        stroke_color = st.color_picker("Color del trazo", "#FFFFFF")

    # Agrupación de controles del lienzo
    with st.expander("🖼️ Fondo y Dimensiones", expanded=False):
        bg_color = st.color_picker("Color de fondo", "#000000")
        bg_image_file = st.file_uploader("Subir imagen de fondo:", type=["png", "jpg", "jpeg"])
        
        # Devolver los sliders de dimensiones
        canvas_width = st.slider("Ancho", 300, 1000, 600, 50)
        canvas_height = st.slider("Alto", 200, 800, 400, 50)

# Cargar imagen de fondo si el usuario sube una
background_image = Image.open(bg_image_file) if bg_image_file else None

# Crear el canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=background_image,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key="canvas" 
)

# Lógica para descargar el dibujo
if canvas_result.image_data is not None:
    st.divider()
    st.subheader("Exportar")
    
    # Convertir el array de numpy a imagen PIL
    img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
    
    # Crear un buffer para la descarga
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    
    st.download_button(
        label="💾 Descargar dibujo como PNG",
        data=buffer.getvalue(),
        file_name="mi_dibujo.png",
        mime="image/png"
    )
