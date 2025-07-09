import numpy as np
import cv2

def visualize_trm_link_remainder(
    img: np.ndarray, 
    intersection_points: list, 
    link_counts: list, 
    output_path: str
):
    """
    Visualizes intersection points with color intensity based on link counts
    (for TRM_link_remainder or similar methods).

    Args:
        img (np.ndarray): The original grayscale image.
        intersection_points (list): A list of (x, y) tuples for intersection points.
        link_counts (list): A list of link counts corresponding to each intersection point.
        output_path (str): The full path where the output image will be saved.
    """
    display_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for i, point in enumerate(intersection_points):
        # Scale color intensity, ensuring it's within [0, 255]
        # The '31' implies a max link_count around 8 for max intensity.
        color_intensity = min(255, int(31 * (8 - link_counts[i])))
        cv2.circle(display_img, point, radius=3, color=(0, 0, color_intensity), thickness=-1)

    cv2.imwrite(output_path, display_img)
    print(f"Visualization saved: {output_path}")

def visualize_trm_link_directions(
    img: np.ndarray, 
    intersection_points: list, 
    link_counts: list, # Still used for color intensity, but interpreted differently
    mem_thi: np.ndarray, # Renamed for clarity and consistency (THI seems like a value)
    output_path: str
):
    """
    Visualizes intersection points with arrows representing directional weights (mem_THI).

    Args:
        img (np.ndarray): The original grayscale image.
        intersection_points (list): A list of (x, y) tuples for intersection points.
        link_counts (list): Link counts, used here for color intensity (e.g., 8 - link_counts).
        mem_thi (np.ndarray): Array of complex numbers representing directional weights.
        output_path (str): The full path where the output image will be saved.
    """
    display_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for i, point in enumerate(intersection_points):
        # Color intensity inverted from link_counts (8 - link_counts)
        color_intensity = min(255, int(31 * (8 - link_counts[i])))
        
        z = mem_thi[i] # This is a complex number from TRM_weighted
        
        # Vector components (real for x-direction, imag for y-direction)
        # Multiply by -1 for dy if your image's y-axis increases downwards
        # and you want standard Cartesian (y increases upwards) interpretation.
        # Otherwise, if dy is positive for "down", keep as is.
        # Assuming point[0] is y-coordinate and point[1] is x-coordinate for OpenCV.
        # dx is for x-direction, dy for y-direction.
        dx = int(np.real(z) * 5)  # Scale for visibility
        dy = int(np.imag(z) * 5)  # Scale for visibility

        # OpenCV coordinates are (x, y)
        # point is (x, y) from TRM, which often means (column, row)
        # start_point is (x_orig, y_orig)
        # end_point is (x_orig + dx, y_orig + dy)
        start_point = (point[0], point[1]) # Assuming point is (x, y) directly from TRM
        end_point = (point[0] + dx, point[1] + dy)
        
        # Arrow color is (Blue, Green, Red)
        # Using (color_intensity, 0, 0) for blue arrows
        cv2.arrowedLine(display_img, start_point, end_point, 
                        color=(color_intensity, 0, 0), thickness=1, tipLength=0.3)
        
        # Circle at the intersection point, with color intensity for red channel
        cv2.circle(display_img, point, radius=2, color=(0, 0, color_intensity), thickness=-1)

    cv2.imwrite(output_path, display_img)
    print(f"Visualization saved: {output_path}")