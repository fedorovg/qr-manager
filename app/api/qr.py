import os
import qrcode
import qrcode.image.svg
from flask import current_app


def generate_qr(payload, name):
    """
    Generates a QR code with a given payload and saves it in a file with the provided name
    :param payload:
    :param name:
    :return:
    """
    qr_code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=6
    )
    qr_code.add_data(payload, optimize=True)
    qr_code.make(fit=True)
    img = qr_code.make_image(fill_color='black', back_color='white', image_factory=qrcode.image.svg.SvgImage)
    path = os.path.join(current_app.config['GENERATED_CODES_PATH'], name)
    img.save(f'{path}.svg')
