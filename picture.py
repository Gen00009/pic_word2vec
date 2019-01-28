from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import sys
from googletrans import Translator
import re
from gensim.models import word2vec
from urllib import request as req
from urllib import error
from urllib import parse
import bs4
import os
import time
import traceback
import flickrapi
from urllib.request import urlretrieve
from urllib.request import urlopen
import urllib.request
from retry import retry
from PIL import Image
import io
import datetime

@retry()
def get_photos(url, filepath):
    urlretrieve(url, filepath)
    time.sleep(1)

'''
画像ダウンロード
'''
flickr_api_key = "XXXXXXXXXXXXXX"
secret_key = "XXXXXXXXXXXXXX"

"""
翻訳用
"""
translator = Translator()

"""
ImageNetで学習済みのVGG16モデルを使って入力画像のクラスを予測する
"""
if len(sys.argv) != 2:
    print("usage: python3 test_vgg16.py [image file]")
    sys.exit(1)


filename = sys.argv[1]
model = VGG16(weights='imagenet')

img = image.load_img(filename, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
preds = model.predict(preprocess_input(x))
results = decode_predictions(preds, top=5)[0]
bunrui = results
gazou = []
i=0
while i<5:
	kekka = translator.translate(bunrui[i][1], src='en' ,dest='ja')
	bun = str(kekka)
	final = re.sub(r'[!-~]', "", bun)
	final = str(final)
	final = final.replace(' ', '')
	gazou.append(final)
	i += 1

'''
共起語
'''

model = word2vec.Word2Vec.load('wiki.pkl')
dt_now = datetime.datetime.now()
dt_now = str(dt_now.replace(microsecond=0))
dt_now = dt_now.replace(':', '-')
new_dir_path = './'+dt_now+'/'
os.mkdir(new_dir_path)
n=0
while n<5:
	if gazou[n] in model:
		pre = model.most_similar(positive = [gazou[n]])
		text = str(pre)
		result = re.sub(r'[!-~]', "", text)

		n += 1
		num = 0
		while num < 10:
			keyword = gazou[n],pre[num][0]
			if __name__ == '__main__':
				flicker = flickrapi.FlickrAPI(flickr_api_key, secret_key, format='parsed-json')
				response = flicker.photos.search(
					text=keyword,
					per_page=1,
					media='photos',
					sort='relevance',
					safe_search=1,
					extras='url_q,license'
				)
				photos = response['photos']

			for photo in photos['photo']:
				url_q = photo['url_q']
				picnum = (n-1)*10+num
				number = str(picnum)

				savename = "test"+number+".png"
				urllib.request.urlretrieve(url_q, new_dir_path + savename)

			num += 1
	else:
		n += 1