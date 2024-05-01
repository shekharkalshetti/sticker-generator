import cv2
import numpy as np
from PIL import Image


def extract_alpha_channel(img):
    return img[:, :, 3]


def get_largest_contour(alpha_channel):
    # Smoothing using GaussianBlur
    smoothed = cv2.GaussianBlur(alpha_channel, (15, 15), 0)
    contours_smoothed = cv2.findContours(
        smoothed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_smoothed = contours_smoothed[0] if len(
        contours_smoothed) == 2 else contours_smoothed[1]
    big_contour_smoothed = max(contours_smoothed, key=cv2.contourArea)

    # Use the smoothed contour
    peri = cv2.arcLength(big_contour_smoothed, True)
    return cv2.approxPolyDP(big_contour_smoothed, 0.001 * peri, True)


def draw_filled_contour_on_black_background(big_contour, shape):
    contour_img = np.zeros(shape)
    cv2.drawContours(contour_img, [big_contour], 0, 255, -1)
    return contour_img


def apply_dilation(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)


def apply_overlays(canvas, img, dilate):
    alpha = np.expand_dims(img[:, :, 3], 2)
    alpha = np.repeat(alpha, 3, 2)
    alpha = alpha / 255

    canvas[dilate == 255] = (255, 255, 255, 255)
    canvas[:, :, 0:3] = canvas[:, :, 0:3] * \
        (1 - alpha) + alpha * img[:, :, 0:3]

    return canvas


def create_sticker(img):
    alpha = extract_alpha_channel(img)
    big_contour = get_largest_contour(alpha)
    contour_img = draw_filled_contour_on_black_background(
        big_contour, alpha.shape)
    dilate = apply_dilation(contour_img)

    canvas = np.zeros(img.shape, dtype=np.uint8)
    canvas = apply_overlays(canvas, img, dilate)

    return canvas.astype(np.uint8)


def show_sticker_from_image(image):
    sticker = Image.fromarray(image)
    sticker.show()
