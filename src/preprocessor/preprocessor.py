from PIL import Image
import os

# Intenta importar pillow_avif, si no está instalado, simplemente lo ignora
try:
    import pillow_avif
except ImportError:
    pass

def preprocess_images(input_dir, output_dir, size=(128, 128)):
    # Asegurar que las carpetas existan
    if not os.path.exists(input_dir):
        print(f"Error: La carpeta de entrada '{input_dir}' no existe.")
        print("Asegúrate de que tus imágenes estén dentro de esa carpeta.")
        return

    os.makedirs(output_dir, exist_ok=True)

    extensiones = (".jpg", ".jpeg", ".png", ".avif", ".webp")
    total_found = 0
    total_processed = 0

    print(f"Buscando imágenes en: {os.path.abspath(input_dir)}")

    for file in os.listdir(input_dir):
        if file.lower().endswith(extensiones):
            total_found += 1
            try:
                path_in = os.path.join(input_dir, file)
                path_out = os.path.join(output_dir, os.path.splitext(file)[0] + ".png")

                img = Image.open(path_in)

                # 1. Manejo de transparencia (Fondo Blanco)
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGBA')
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    bg.paste(img, (0, 0), img.split()[3])
                    img = bg
                else:
                    img = img.convert("RGB")

                # 2. Recorte cuadrado central (Evita deformaciones)
                w, h = img.size
                min_dim = min(w, h)
                left = (w - min_dim) // 2
                top = (h - min_dim) // 2
                img = img.crop((left, top, left + min_dim, top + min_dim))

                # 3. Redimensionado de alta calidad
                img = img.resize(size, Image.Resampling.LANCZOS)

                # 4. Guardar como PNG (Sin pérdida)
                img.save(path_out, "PNG")
                total_processed += 1

            except Exception as e:
                print(f"Error con {file}: {e}")

    print(f"Imágenes encontradas: {total_found}")
    print(f"Imágenes procesadas correctamente: {total_processed}")
    print(f"Resultados guardados en: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    # --- CONFIGURACIÓN DE RUTAS ---
    # Si estás en Google Colab, usa la ruta de tu Drive:
    # input_folder = "/content/drive/MyDrive/tu_carpeta/raw"
    
    input_folder = "data/raw/original_tshirts"
    output_folder = "data/processed/new_tshirts"

    preprocess_images(
        input_dir=input_folder,
        output_dir=output_folder,
        size=(128, 128)
    )