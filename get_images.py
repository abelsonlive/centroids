from urllib import urlretrieve
from operator import itemgetter
import csv,json
import time
import os

import colorsys

def get_color_data(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in xrange(0,5,2))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    return {
      'red': r,
      'green': g,
      'blue': b,
      'hue': h,
      'saturation': s,
      'value': v
    }
        
# data
def get_data():
  reader = json.load(open('centroids-colors.json'))
  data = []
  for r in reader:
    if r['hex_code'] != 'ffffff':
      c = get_color_data(r['hex_code'])
      row = dict( r.items() + c.items() )
      data.append(row)
  return data

centroids = [r for r in reversed(sorted(get_data(), key=itemgetter('hue')))]

with open('centroids-colors.json', 'wb') as f:
  f.write(json.dumps(centroids, indent=4))

# google maps API
URL = 'http://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=15&size=400x400&maptype=satellite&sensor=true&key=%s'
API_KEY = os.getenv('GOOGLE_API_KEY')

# function to get image:
def get_image(lat, lng, country):
  url = URL % (lat, lng, API_KEY)
  fp = "images/%s.png" % country
  print "< saving %s >" % fp
  urlretrieve(url, fp)

def get_images(centroids):
  for c in centroids:
    get_image(c['lat'], c['lng'], c['fips'])
    time.sleep(1.5)

def crop_images():
  print "< cropping images >"
  for f in os.listdir('images'):
    cmd = "convert images/%s -crop 400x400-25-25  +repage images/%s" % (f, f)
    print cmd
    os.system(cmd)

def round_edges():
  print "< rounding edges >"
  for f in os.listdir('images'):
    cmd = "convert images/" + f + " " + \
          " \\( +clone  -alpha extract" + \
          " -draw 'fill black polygon 0,0 0,15 15,0 fill white circle 15,15 15,0'" + \
          " \\( +clone -flip \\) -compose Multiply -composite" + \
          " \\( +clone -flop \\) -compose Multiply -composite" + \
          " \\) -alpha off -compose CopyOpacity -composite " + "images/" + f
    os.system(cmd)

def resize_images():
  print "< resizing images >"
  for f in os.listdir('images'):
    cmd = " convert images/%s -resize 100x100 images/%s" % (f, f)
    os.system(cmd)

if __name__ == '__main__':
  # get_images(centroids)
  # crop_images()
  # round_edges()
  # resize_images()
  print ""

