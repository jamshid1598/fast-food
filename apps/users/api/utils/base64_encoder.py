import base64

from io import BytesIO
from PIL import Image


def encoder(file_path):
    with open(file_path, 'rb') as image_file:
        base64_bytes = base64.b64encode(image_file.read())

        with open("bs.txt", "w") as f:
            f.write(base64_bytes.decode())

    return {"msg": "encoded"}


def decoder(file_path, file_name, file_ext):
    with open(file_path, "rb") as binary_data:
        img = Image.open(
            BytesIO(
                base64.b64decode(
                    binary_data.read()
                )
            )
        )

        img.save(f"{file_name}.{file_ext.lower()}")
    return {"msg": "decoded"}
