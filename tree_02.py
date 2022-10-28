import requests
import numpy as np
from PIL import Image
from skimage.segmentation import slic, mark_boundaries
from skimage.color import label2rgb
import pymeanshift as pms

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


token = 'AIzaSyBXOg6f3ZNKIHw7-6Y_M_ZvMkFq5N3DOLU'
latlng = '18.795855425657738,98.95961454981598'
heading = 0
pitch = 0

url = f'https://maps.googleapis.com/maps/api/streetview?location={latlng}&size=456x456&fov=60&heading={heading}&pitch=0&sensor=false&key={token}'

im = Image.open(requests.get(url, stream=True).raw)
(im_segments, labels_image, number_regions) = pms.segment(im, spatial_radius=6,
                                                          range_radius=7, min_density=40)
plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)
plt.imshow(im)


plt.subplot(1, 2, 2)
plt.imshow(im_segments)
plt.show()
