import os
import cv2
import numpy as np # Often useful with image processing, so good to include
# Assuming TRM is a module you've defined elsewhere
import TRM 

def process_image_with_trm(input_image_path: str, output_dir: str = 'output'):
    """
    Processes an image using TRM (presumably a custom module for 
    Topological Relation Mapping or similar) to find intersection points 
    and display them based on link counts.

    Args:
        input_image_path (str): The full path to the input grayscale image.
        output_dir (str): The directory where the output image will be saved.
                          Defaults to 'output'.
    """
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = os.path.basename(input_image_path)
    
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Error: Could not read image from {input_image_path}")
        return

    # Call the TRM function. Using descriptive variable names.
    # Original commented lines are kept for reference if you want to switch methods
    # res_single_point = TRM.TRM_single_point(img, [50, 50]) # Example usage
    # res_weighted = TRM.TRM_weighted(img) # Example usage
    
    intersection_points, link_counts = TRM.TRM_link_remainder(img)

    # Convert grayscale image to BGR for colored circles
    display_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Draw circles at intersection points, with color intensity based on link_counts
    for i, point in enumerate(intersection_points):
        # Ensure color value is within 0-255. 
        # Max link_count needs to be considered for appropriate scaling.
        # Assuming link_counts are relatively small or you want a strong visual difference.
        # A simple linear scaling up to 255 might be:
        # color_intensity = min(255, int(link_counts[i] * some_scaling_factor))
        # For the original 'int(31*link_counts[i])' logic, this implies link_counts max around 8
        color_intensity = min(255, int(31 * link_counts[i])) 
        cv2.circle(display_img, point, radius=3, color=(0, 0, color_intensity), thickness=-1) # thickness=-1 fills the circle

    output_image_path = os.path.join(output_dir, 'TRM_' + filename)
    cv2.imwrite(output_image_path, display_img)
    print(f"Processed image saved to: {output_image_path}")

# Example usage:
if __name__ == "__main__":
    INPUT_IMAGE_PATH = os.path.join('data', 'sample_1.jpg')
    process_image_with_trm(INPUT_IMAGE_PATH)

    # You can also add more examples or a loop for multiple images
    # INPUT_IMAGE_PATH_2 = os.path.join('data', 'another_sample.png')
    # process_image_with_trm(INPUT_IMAGE_PATH_2)