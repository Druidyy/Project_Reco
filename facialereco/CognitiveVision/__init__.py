import logging
import os
import io
import json
import azure.functions as func
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from PIL import Image


def main(myblob: func.InputStream,docout:func.Out[func.Document]):
    #region = os.environ['ACCOUNT_REGION']
    key = os.environ['ACCOUNT_KEY']
    region ='francecentral'
    #key ='7c2d5d3665ae4d17995003122ebced5a'
    language = "en"
    max_descriptions = 3

    credentials = CognitiveServicesCredentials(key)
    client = ComputerVisionClient(
        endpoint="https://" + region + ".api.cognitive.microsoft.com/",
        credentials=credentials
    )
    image = Image.open(io.BytesIO(myblob))
    analysis = client.describe_image_in_stream(image, max_descriptions, language)
    description=""
    for caption in analysis.captions:
        description=description+caption.text
        print(caption.text)
        print(caption.confidence)
    doc=func.Document.from_json(json.dumps({'description':description}))
    docout.set(description)
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
