import json, requests
from pprint import pprint
import pdfkit
from pdf2image import convert_from_path
import os
import numpy as np
from PIL import Image

# install-pkg poppler-utils, wkhtmltopdf


def ayaat():
  
  english = ''

  data = json.loads(requests.get('https://api.quran.com/api/v4/verses/random?language=en&words=true').text)["verse"]

  verse = data["verse_key"]
  words = data["words"]

  words.sort(key=lambda x: x["position"])

  for num, dic in enumerate(words):

    if num+1 < len(words):
      english += dic["translation"]["text"] + ' '


  return english, verse


def search_ayaat(aya):
  
  try: os.remove('aya.jpg')

  except FileNotFoundError: pass

  data = requests.get(f'https://quran.com/{aya}?font=v1&translations=131%2C20')

  if data.status_code == 200:

    pdfkit.from_url(f'https://quran.com/{aya}?font=v1&translations=131%2C20','aya.pdf')

    convert_from_path('aya.pdf')[0].save('aya.jpg', 'JPEG')

    os.remove('aya.pdf')

    image = Image.open('aya.jpg')
    os.remove('aya.jpg')
    img_array = np.array(image)


    indices = np.where(np.all(img_array == 	(128, 128, 128), axis=-1))

    #alter plus values
    coords = list(filter(lambda x: x[1]+17 in indices[1],list(zip(indices[0], indices[1]))))

    coords.sort(key = lambda x: x[1])
    
    cut = coords[-1][1] if coords and coords[-1][1] <= 1600 and coords[-1][1] >= 400 else 1600



    img_array = img_array[100:cut]

    image = Image.fromarray(img_array, 'RGB')
    image.save('ayaat.jpg')

