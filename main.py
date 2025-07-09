import os
import cv2
import numpy as np # Often useful with image processing, so good to include

# Assuming TRM is located at TRM_modules/TRM.py
# This import path correctly reflects the module structure you're aiming for.
try:
    import TRM_modules.TRM as TRM
except ImportError:
    print("Error: TRM_modules.TRM could not be imported.")
    print("Please ensure TRM_modules directory is correctly set up in your Python path.")
    exit() # Exit if the core module is not found

import TRM_modules.utils.visualization_helpers as TRM_viz

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

    filename_base = os.path.basename(input_image_path)
    filename_stem, ext = os.path.splitext(filename_base)
    
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Error: Could not read image from {input_image_path}")
        return
    
    # --- EXAMPLE 1: Using TRM_fast_link_remainder ---
    print("Running Example 1: TRM_fast_link_remainder")
    try:
        fast_intersection_points, fast_link_counts = TRM.TRM_fast_link_remainder(img)
        
        # Visualize the result from TRM_fast_link_remainder
        # Note: TRM_fast_link_remainder only provides link_counts, so only one type of viz is applicable
        output_path_fast_remainder = os.path.join(
            output_dir, f"{filename_stem}_(EX_1_TRM_fast_remainder){ext}"
        )
        TRM_viz.visualize_trm_link_remainder(
            img, 
            fast_intersection_points, 
            fast_link_counts, 
            output_path_fast_remainder
        )
    except Exception as e:
        print(f"Error calling TRM.TRM_fast_link_remainder: {e}")

     # --- EXAMPLE 2: Using TRM_weighted ---
    print("\nRunning Example 2: TRM_weighted")
    try:
        weighted_intersection_points, weighted_link_counts, weighted_mem_THI = TRM.TRM_weighted(img)
        
        # Visualize link remainder for TRM_weighted (using its link_counts)
        output_path_weighted_remainder = os.path.join(
            output_dir, f"{filename_stem}_(EX_2.1_TRM_weighted_remainder){ext}"
        )
        TRM_viz.visualize_trm_link_remainder(
            img, 
            weighted_intersection_points, 
            weighted_link_counts, 
            output_path_weighted_remainder
        )

        # Visualize link directions for TRM_weighted (using its mem_THI)
        output_path_weighted_directions = os.path.join(
            output_dir, f"{filename_stem}_(EX_2.2_TRM_weighted_directions){ext}"
        )
        TRM_viz.visualize_trm_link_directions(
            img, 
            weighted_intersection_points, 
            weighted_link_counts, # Still needed for color scaling
            weighted_mem_THI, 
            output_path_weighted_directions
        )

    except Exception as e:
        print(f"Error calling TRM.TRM_weighted: {e}")


# Example usage:
if __name__ == "__main__":
    data_dir = 'data' 
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}. Please place sample_1.jpg here.")

    INPUT_IMAGE_PATH = os.path.join(data_dir, 'sample_1.jpg')
    
    if not os.path.exists(INPUT_IMAGE_PATH):
        print(f"Error: Input image not found at {INPUT_IMAGE_PATH}")
        print("Please ensure 'sample_1.jpg' is placed in the 'data' directory.")
    else:
        process_image_with_trm(INPUT_IMAGE_PATH)
    
