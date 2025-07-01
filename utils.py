import cv2
import numpy as np

def overlay_transparent(background, overlay, x, y, overlay_size=None):
    if overlay_size:
        overlay = cv2.resize(overlay.copy(), overlay_size)

    h, w = overlay.shape[:2]

    if x + w > background.shape[1] or y + h > background.shape[0] or x < 0 or y < 0:
        return background

    # Extract alpha channel for transparency
    alpha_overlay = overlay[:, :, 3] / 255.0
    alpha_background = 1.0 - alpha_overlay

    for c in range(3):  # For BGR channels
        background[y:y+h, x:x+w, c] = (
            alpha_overlay * overlay[:, :, c] +
            alpha_background * background[y:y+h, x:x+w, c]
        )

    return background
