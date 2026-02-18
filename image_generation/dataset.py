from PIL import Image
import os
import pillow_avif


def preprocess_images(input_dir, output_dir, size=(64, 64)):
    os.makedirs(output_dir, exist_ok=True)

    extensiones = (".jpg", ".jpeg", ".png", ".avif")
    total_found = 0
    total_processed = 0

    for file in os.listdir(input_dir):
        if file.lower().endswith(extensiones):
            total_found += 1
            try:
                path_in = os.path.join(input_dir, file)
                path_out = os.path.join(
                    output_dir,
                    os.path.splitext(file)[0] + ".jpg"
                )

                img = Image.open(path_in).convert("RGB")

                # Crop centrado para hacerla cuadrada
                w, h = img.size
                min_dim = min(w, h)

                left = (w - min_dim) // 2
                top = (h - min_dim) // 2
                right = left + min_dim
                bottom = top + min_dim

                img = img.crop((left, top, right, bottom))

                # Resize a 64x64
                img = img.resize(size)

                img.save(path_out, "JPEG")
                total_processed += 1

            except Exception as e:
                print("Error con:", file, e)

    print("Found images:", total_found)
    print("Images processed correctly:", total_processed)
    print("Preprocessing complete")

if __name__ == "__main__":
    preprocess_images(
        "image_generation/raw/original_tshirts",
        "image_generation/processed/final_tshirts"
    )

