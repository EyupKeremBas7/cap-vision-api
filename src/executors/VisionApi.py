import os
import cv2
import sys

from google.cloud import vision
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.helper.executor import Executor
from capsules.VisionApi.src.utils.response import build_response
from capsules.VisionApi.src.models.PackageModel import PackageModel
from capsules.VisionApi.src.utils.utils import API_AUTH

class VisionApi(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.text = ""

    @staticmethod
    def bootstrap(config: dict) -> dict:
        API_AUTH()
        return {}

    def detect_text_from_local_image(self, image):
        """
        Yerel bir resim dosyasındaki metni (yazıları) algılar ve yazdırır.

        Args:
            image_path: Algılanacak metnin bulunduğu resim dosyasının yolu.
        """
        client = vision.ImageAnnotatorClient()
        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()
        image = vision.Image(content=image_bytes)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        if not texts:
            return None

        full_text = texts[0].description

        print("\nDetaylı Metin Parçaları:")
        for i, text in enumerate(texts):
            if i == 0:
                continue
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])
            print(f"  - '{text.description}'  Konum: {','.join(vertices)}")

        if response.error.message:
            raise Exception(
                'Vision API Hatası: {}\nDaha fazla bilgi için: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return full_text


    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        self.text = self.detect_text_from_local_image(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
