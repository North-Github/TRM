TRM Image Analysis Tools<!-- Add a GitHub Actions CI badge here once you set up your workflow --><!--  -->A Python package providing tools for Topological Relation Mapping (TRM) analysis on grayscale images, including fast approximation methods and comprehensive weighted approaches, along with visualization utilities.Table of ContentsIntroductionFeaturesInstallationUsageExample 1: Fast Link RemainderExample 2: Weighted TRM with Directional AnalysisProject StructureContributingLicenseContactIntroductionThe Topological Relation Model (TRM) is a method used in image processing to analyze the topological properties of image structures, often revealing patterns related to turbulence, flow, or complex textures. This repository provides a set of Python modules to perform TRM analysis, offering both a faster, simplified link remainder computation and a more detailed weighted analysis that includes directional information. It also includes functions to visualize the results directly on the image.FeaturesTRM_fast_link_remainder: A highly optimized function to compute the link remainder metric, suitable for quick analysis or large datasets where precise directional data is not critical.TRM_weighted: A comprehensive function for TRM analysis that calculates link remainders and incorporates directional weights, providing richer topological insights.Visualization Utilities: Dedicated functions (visualize_trm_link_remainder, visualize_trm_link_directions) to graphically represent the computed TRM features on the input image using OpenCV.Modular Design: Organized into a Python package (TRM_modules) for clean separation of core algorithms and visualization tools.InstallationTo get started with this package, follow these steps:Clone the repository:git clone https://github.com/your-username/TRM-Image-Analysis-Tools.git
cd TRM-Image-Analysis-Tools
Create a virtual environment (recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:The required libraries are listed in requirements.txt.pip install -r requirements.txt
Install the package locally:This will install TRM_modules so you can import it in your scripts.pip install .
UsageThe process_image_with_trm function in process_images.py demonstrates how to use the TRM_fast_link_remainder and TRM_weighted methods, along with their respective visualizations.First, ensure you have a sample grayscale image (e.g., sample_1.jpg) in a data/ directory at the root of your project.TRM-Image-Analysis-Tools/
├── data/
│   └── sample_1.jpg
├── TRM_modules/
│   ├── __init__.py
│   ├── TRM.py
│   └── utils
│       ├── helper_functions.py
│       └── visualization_helpers.py
├── output/
├── main.py
<!-- ├── pyproject.toml
├── requirements.txt -->
└── README.md
You can run the main demonstration script:python process_images.py
This will generate output images in the output/ directory, showcasing the results of both TRM methods.Example 1: Fast Link RemainderThis example demonstrates the use of TRM.TRM_fast_link_remainder for a quick topological analysis, visualizing the link remainder counts.# In your script (e.g., process_images.py)
import os
import cv2
import TRM_modules.TRM as TRM
import TRM_modules.visualization as TRM_vis

# Assuming img is your loaded grayscale image (e.g., from cv2.imread)
# And filename_stem, ext, output_dir are defined

print("Running Example 1: TRM_fast_link_remainder")
try:
    fast_intersection_points, fast_link_counts = TRM.TRM_fast_link_remainder(img)
    
    output_path_fast_remainder = os.path.join(
        output_dir, f"{filename_stem}_(TRM_fast_remainder){ext}"
    )
    TRM_vis.visualize_trm_link_remainder(
        img, 
        fast_intersection_points, 
        fast_link_counts, 
        output_path_fast_remainder
    )
except Exception as e:
    print(f"Error calling TRM.TRM_fast_link_remainder: {e}")
Example 2: Weighted TRM with Directional AnalysisThis example showcases the more comprehensive TRM.TRM_weighted method, which provides both link remainder counts and directional information (mem_THI), allowing for two distinct visualizations.# In your script (e.g., process_images.py)
import os
import cv2
import TRM_modules.TRM as TRM
import TRM_modules.visualization as TRM_vis
import numpy as np # Needed for np.real/np.imag if visualizing directions

# Assuming img is your loaded grayscale image (e.g., from cv2.imread)
# And filename_stem, ext, output_dir are defined

print("\nRunning Example 2: TRM_weighted")
try:
    weighted_intersection_points, weighted_link_counts, weighted_mem_THI = TRM.TRM_weighted(img)
    
    # Visualize link remainder for TRM_weighted
    output_path_weighted_remainder = os.path.join(
        output_dir, f"{filename_stem}_(TRM_weighted_remainder){ext}"
    )
    TRM_vis.visualize_trm_link_remainder(
        img, 
        weighted_intersection_points, 
        weighted_link_counts, 
        output_path_weighted_remainder
    )

    # Visualize link directions for TRM_weighted
    output_path_weighted_directions = os.path.join(
        output_dir, f"{filename_stem}_(TRM_weighted_directions){ext}"
    )
    TRM_vis.visualize_trm_link_directions(
        img, 
        weighted_intersection_points, 
        weighted_link_counts, # Used for color scaling
        weighted_mem_THI, 
        output_path_weighted_directions
    )

except Exception as e:
    print(f"Error calling TRM.TRM_weighted: {e}")
Project StructureThe core logic of this project is organized as a Python package TRM_modules:TRM-Image-Analysis-Tools/
├── TRM_modules/
│   ├── __init__.py        # Makes 'TRM_modules' a Python package
│   ├── TRM.py             # Contains the core TRM algorithms (e.g., TRM_fast_link_remainder, TRM_weighted)
│   └── visualization.py   # Contains functions for visualizing TRM results (e.g., visualize_trm_link_remainder, visualize_trm_link_directions)
├── data/                  # Directory for sample input images
├── output/                # Directory for generated output images
├── process_images.py      # Main script demonstrating the use of the modules
├── pyproject.toml         # Project metadata and build configuration (modern Python packaging)
├── requirements.txt       # List of project dependencies
└── README.md              # This file
ContributingContributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to:Fork the repository.Create a new branch (git checkout -b feature/your-feature-name).Make your changes.Commit your changes (git commit -m 'Add new feature').Push to the branch (git push origin feature/your-feature-name).Open a Pull Request.Please ensure your code adheres to good practices and includes relevant tests.LicenseThis project is licensed under the MIT License - see the LICENSE file for details.ContactFor any questions or inquiries, please open an issue on this repository or contact:Your Name/Alias - your.email@example.comGitHub Profile - https://github.com/your-username