import requests
import numpy as np
from PIL import Image
from skimage.segmentation import slic, mark_boundaries
from skimage.color import label2rgb
import pymeanshift as pms

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def graythresh(array, level):
    try:
        maxVal = np.max(array)
        minVal = np.min(array)

        if maxVal <= 1:
            array = array*255
            # print "New max value is %s" %(np.max(array))
        elif maxVal >= 256:
            array = np.int((array - minVal)/(maxVal - minVal))

        # turn the negative to natural number
        negIdx = np.where(array < 0)
        array[negIdx] = 0

        # calculate the hist of 'array'
        dims = np.shape(array)
        hist = np.histogram(array, range(257))
        P_hist = hist[0]*1.0/np.sum(hist[0])

        omega = P_hist.cumsum()

        temp = np.arange(256)
        mu = P_hist*(temp+1)
        mu = mu.cumsum()

        n = len(mu)
        mu_t = mu[n-1]

        sigma_b_squared = (mu_t*omega - mu)**2/(omega*(1-omega))

        # try to found if all sigma_b squrered are NaN or Infinity
        indInf = np.where(sigma_b_squared == np.inf)

        CIN = 0
        if len(indInf[0]) > 0:
            CIN = len(indInf[0])

        maxval = np.max(sigma_b_squared)

        IsAllInf = CIN == 256
        if IsAllInf != 1:
            index = np.where(sigma_b_squared == maxval)
            idx = np.mean(index)
            threshold = (idx - 1)/255.0
        else:
            threshold = level

        if np.isnan(threshold):
            threshold = level
        return threshold

    except Exception as e:
        print(e)


def get_image(i, heading):
    try:
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

        # plt.imshow(mark_boundaries(im, im_segments))
        # plt.imshow(label2rgb(im_segments, im, kind = 'avg'))

        I = im_segments/255.0
        red = I[:, :, 0]
        green = I[:, :, 1]
        blue = I[:, :, 2]

        # calculate the difference between green band with other two bands
        green_red_Diff = green - red
        green_blue_Diff = green - blue

        ExG = green_red_Diff + green_blue_Diff

        diffImg = green_red_Diff*green_blue_Diff

        redThreImgU = red < 0.6
        greenThreImgU = green < 0.9
        blueThreImgU = blue < 0.6

        shadowRedU = red < 0.3
        shadowGreenU = green < 0.3
        shadowBlueU = blue < 0.3
        del red, blue, green, I

        greenImg1 = redThreImgU * blueThreImgU*greenThreImgU
        greenImgShadow1 = shadowRedU*shadowGreenU*shadowBlueU
        del redThreImgU, greenThreImgU, blueThreImgU
        del shadowRedU, shadowGreenU, shadowBlueU

        greenImg3 = diffImg > 0.0
        greenImg4 = green_red_Diff > 0
        threshold = graythresh(ExG, 0.1)

        if threshold > 0.1:
            threshold = 0.1
        elif threshold < 0.05:
            threshold = 0.05

        greenImg2 = ExG > threshold
        greenImgShadow2 = ExG > 0.05
        greenImg = greenImg1*greenImg2 + greenImgShadow2*greenImgShadow1
        del ExG, green_blue_Diff, green_red_Diff
        del greenImgShadow1, greenImgShadow2

        # calculate the percentage of the green vegetation
        greenPxlNum = len(np.where(greenImg != 0)[0])
        greenPercent = greenPxlNum/(400.0*400)*100
        del greenImg1, greenImg2
        del greenImg3, greenImg4

        print(i, greenPercent)

    except Exception as e:
        print(e)


token = 'AIzaSyBXOg6f3ZNKIHw7-6Y_M_ZvMkFq5N3DOLU'
latlng = '18.80951985327199,98.95249514295107'
# headingArr = 360/6*np.array([0, 1, 2, 3, 4, 5])
pitch = 0

for x in range(0, 5):
    heading = 360/6*x
    i = x+1
    get_image(i, heading)
