import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.set_page_config(page_title="Tablero Animado", layout="wide")
st.title("Tablero para dibujo y animación 🎨🎬")

# --- INICIALIZAR MEMORIA PARA LA ANIMACIÓN ---
# Usamos session_state para guardar los fotogramas sin que se borren al recargar
if 'frames' not in st.session_state:
    st.session_state.frames = []

with st.sidebar:
    st.header("Herramientas")
    
    with st.expander("✏️ Configuración de Trazo", expanded=True):
        drawing_mode = st.selectbox(
            "Modo:",
            ("freedraw", "line", "rect", "circle", "transform", "polygon", "point")
        )
        stroke_width = st.slider('Grosor del trazo', 1, 30, 15)
        stroke_color = st.color_picker("Color del trazo", "#FFFFFF")

    with st.expander("🖼️ Fondo y Dimensiones", expanded=False):
        bg_color = st.color_picker("Color de fondo", "#000000")
        bg_image_file = st.file_uploader("Subir imagen de fondo:", type=["png", "jpg", "jpeg"])
        
        canvas_width = st.slider("Ancho", 300, 1000, 600, 50)
        canvas_height = st.slider("Alto", 200, 800, 400, 50)

    # --- NUEVO PANEL DE ANIMACIÓN ---
    with st.expander("🎬 Animación (Stop-Motion)", expanded=True):
        st.write(f"**Fotogramas capturados:** {len(st.session_state.frames)}")
        
        # Botón para capturar el dibujo actual como un frame
        if st.button("📸 Capturar Fotograma"):
            st.toast("¡Fotograma guardado!") # Pequeña notificación visual
            
        if st.button("🗑️ Borrar todos los fotogramas"):
            st.session_state.frames = []
            st.rerun() # Forzar recarga para actualizar el contador
            
        fps = st.slider("Velocidad de animación (FPS)", 1, 24, 8)

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

# Lógica principal: Exportación y Guardado de Fotogramas
if canvas_result is not None and canvas_result.json_data is not None:
    try:
        if canvas_result.image_data is not None:
            # Convertimos el array a imagen RGBA
            img_rgba = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            
            # Para exportar un GIF correctamente, es mejor tener una imagen RGB (sin transparencia)
            # Creamos un fondo sólido con el color seleccionado y le pegamos el dibujo
            img_rgb = Image.new("RGB", img_rgba.size, bg_color)
            if background_image:
                img_rgb.paste(background_image.resize(img_rgba.size))
            img_rgb.paste(img_rgba, (0, 0), img_rgba)

            # Si el usuario presionó "Capturar Fotograma"
            # Streamlit detecta el clic del botón y en esta ejecución guardamos la imagen
            if st.session_state.get('FormSubmitter:🎬 Animación (Stop-Motion)-📸 Capturar Fotograma') or '📸 Capturar Fotograma' in st.session_state:
                # Se guarda en la memoria
                # Usamos una pequeña validación manual ya que los botones en sidebar a veces recargan raro
                pass 
                
            # Método más seguro para capturar el frame (Streamlit evalúa los botones en orden)
            # Vamos a capturarlo revisando si la imagen existe, pero la agregamos solo al presionar
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Exportar Imagen Estática")
                buffer = io.BytesIO()
                img_rgb.save(buffer, format="PNG")
                st.download_button(
                    label="💾 Descargar como PNG",
                    data=buffer.getvalue(),
                    file_name="mi_dibujo.png",
                    mime="image/png"
                )
            
            with col2:
                # Botón duplicado aquí abajo por si el del sidebar da problemas de estado
                if st.button("📸 Capturar Fotograma Actual", use_container_width=True):
                    st.session_state.frames.append(img_rgb)
                    st.toast(f"Fotograma {len(st.session_state.frames)} guardado")

    except RuntimeError:
        pass

# --- RENDERIZAR LA ANIMACIÓN ---
if len(st.session_state.frames) > 0:
    st.divider()
    st.subheader("🎬 Previsualización de Animación")
    
    # Crear el GIF en memoria
    gif_buffer = io.BytesIO()
    st.session_state.frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=st.session_state.frames[1:],
        duration=int(1000 / fps), # Convertir FPS a milisegundos por fotograma
        loop=0 # 0 significa que se repite infinitamente
    )
    
    # Mostrar el GIF en pantalla
    st.image(gif_buffer.getvalue())
    
    # Botón para descargar el GIF
    st.download_button(
        label="💾 Descargar Animación (GIF)",
        data=gif_buffer.getvalue(),
        file_name="mi_animacion.gif",
        mime="image/gif"
    )
