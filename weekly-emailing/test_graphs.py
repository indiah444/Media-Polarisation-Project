# pylint: skip-file

import base64
import io

from PIL import Image

from graphs import chart_to_base64, create_whisker_plot


def test_chart_to_base64(sample_chart):

    result = chart_to_base64(sample_chart)

    assert isinstance(result, str)
    assert result.startswith('iVBORw0KGgo')


def test_create_whisker_plot(sample_data):
    result = create_whisker_plot(sample_data)
    image_data = base64.b64decode(result)
    image = Image.open(io.BytesIO(image_data))

    assert isinstance(result, str)
    assert result.startswith('iVBORw0KGgo')

    assert image.format == 'PNG'
    assert image.size[0] > 0 and image.size[1] > 0
