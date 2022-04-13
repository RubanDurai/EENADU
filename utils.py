import logging
import requests
import pyvips
import img2pdf
from typing import List, Tuple
import enum

logger = logging.getLogger(__name__)

class Editions(enum.Enum):
    TELANGANA = 1
    ANDHRAPRADESH = 2
    HYDERABAD = 3
    SUNDAY = 4

def download_and_merge(filename: str, data: List[Tuple[str, str]]):
    pdf = open(filename, "wb")
    processed = []

    for (image_layer, text_layer) in data:
        logger.info("\n\tpair =>\n\timage layer = %s \n\t(x)\n\ttext layer = %s", image_layer, text_layer)
        image = requests.get(image_layer)
        text = requests.get(text_layer)

        image = pyvips.Image.new_from_buffer(image.content, "", access="sequential").addalpha()
        text = pyvips.Image.new_from_buffer(text.content, "", access="sequential")

        image = image.composite2(text, pyvips.enums.BlendMode.ATOP)
        image = image.write_to_buffer(".jpg", Q=50)
        processed.append(image)
        logger.debug("pair appended!")
    
    pdf.write(img2pdf.convert(processed))
    pdf.close()
    logger.info("PDF created!")