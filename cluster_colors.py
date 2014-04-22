import struct
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import json

def colorz(filename, n_clusters):

    im = Image.open(filename)
    im = im.resize((150, 150))     
    ar = scipy.misc.fromimage(im)
    shape = ar.shape
    try:
        ar = ar.reshape(scipy.product(shape[:2]), shape[2])
    except IndexError:
        print 'no color information'
        return "ffffffff"
    else:
        codes, dist = scipy.cluster.vq.kmeans(ar, n_clusters)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)       
        counts, bins = scipy.histogram(vecs, len(codes))   

        index_max = scipy.argmax(counts)               
        peak = codes[index_max]
        colour = ''.join(chr(c) for c in peak).encode('hex')
        return colour

def main(n_clusters=5):
    data = json.load(open('centroids.json'))
    new_data = []
    for row in data:
        f = "images/" + row['img']
        hex_code = colorz(f, n_clusters=5)
        row['hex_code'] = hex_code[:6]
        print row
        new_data.append(row)
    with open('centroids-colors.json', 'wb') as f:
        f.write(json.dumps(new_data))


if __name__ == '__main__':
    main()
    