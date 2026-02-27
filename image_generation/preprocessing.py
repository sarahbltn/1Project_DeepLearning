from PIL import Image
import os

try:
    import pillow_avif
except ImportError:
    pass

def preprocess_images(input_dir, output_dir, size=(128, 128)):
    if not os.path.exists(input_dir):
        print(f"Error: The input folder '{input_dir}' does not exist.")
        print("Make sure the images are in the folder.")
        return

    os.makedirs(output_dir, exist_ok=True)

    extensiones = (".jpg", ".jpeg", ".png", ".avif", ".webp")
    total_found = 0
    total_processed = 0

    print(f"Searching images in: {os.path.abspath(input_dir)}")

    for file in os.listdir(input_dir):
        if file.lower().endswith(extensiones):
            total_found += 1
            try:
                path_in = os.path.join(input_dir, file)
                path_out = os.path.join(output_dir, os.path.splitext(file)[0] + ".png")

                img = Image.open(path_in)

                # Fondo Blanco
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGBA')
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    bg.paste(img, (0, 0), img.split()[3])
                    img = bg
                else:
                    img = img.convert("RGB")

                # Cuadrado size
                w, h = img.size
                min_dim = min(w, h)
                left = (w - min_dim) // 2
                top = (h - min_dim) // 2
                img = img.crop((left, top, left + min_dim, top + min_dim))

                # Redimensionado de alta calidad
                img = img.resize(size, Image.Resampling.LANCZOS)

                # Guardar como PNG
                img.save(path_out, "PNG")
                total_processed += 1

            except Exception as e:
                print(f"Error con {file}: {e}")

    print(f"Imágenes encontradas: {total_found}")
    print(f"Imágenes procesadas correctamente: {total_processed}")
    print(f"Resultados guardados en: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    
    input_folder = "data/raw/original_tshirts"
    output_folder = "data/processed/new_tshirts"

    preprocess_images(
        input_dir=input_folder,
        output_dir=output_folder,
        size=(128, 128)
    )