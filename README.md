# TRM Image Analysis Tools

<!-- [![GitHub Actions CI](https://github.com/your-username/TRM-Image-Analysis-Tools/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/TRM-Image-Analysis-Tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) -->

A Python package providing tools for Topological Relation Mapping (TRM) analysis on grayscale images, including fast approximation methods and comprehensive weighted approaches, along with visualization utilities.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Example 1: Fast Link Remainder](#example-1-fast-link-remainder)
  - [Example 2: Weighted TRM with Directional Analysis](#example-2-weighted-trm-with-directional-analysis)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

The Topological Relation Model (TRM) is a method used in image processing to analyze the topological properties of image structures, often revealing patterns related to turbulence, flow, or complex textures. This repository provides a set of Python modules to perform TRM analysis, offering both a faster, simplified link remainder computation and a more detailed weighted analysis that includes directional information. It also includes functions to visualize the results directly on the image.

---

## Features

* **TRM_fast_link_remainder:** A highly optimized function to compute the link remainder metric, suitable for quick analysis or large datasets where precise directional data is not critical.
* **TRM_weighted:** A comprehensive function for TRM analysis that calculates link remainders and incorporates directional weights, providing richer topological insights.
* **Visualization Utilities:** Dedicated functions (`visualize_trm_link_remainder`, `visualize_trm_link_directions`) to graphically represent the computed TRM features on the input image using OpenCV.
* **Modular Design:** Organized into a Python package (`TRM_modules`) for clean separation of core algorithms and visualization tools.

---

## Installation

To get started with this package, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/North-Github/TRM.git
    cd TRM
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The required libraries are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install the package locally:**
    This will install `TRM_modules` so you can import it in your scripts.
    ```bash
    pip install .
    ```

---

## Usage

The `process_image_with_trm` function in `process_images.py` demonstrates how to use the `TRM_fast_link_remainder` and `TRM_weighted` methods, along with their respective visualizations.

First, ensure you have a sample grayscale image (e.g., `sample_1.jpg`) in a `data/` directory at the root of your project, structured as follows:
    
    TRM-Image-Analysis-Tools/
    ├── TRM_modules/
    │   ├── __init__.py                     # Initializes 'TRM_modules' as a Python package
    │   ├── TRM.py                          # Contains the core Topological Relation Mapping (TRM) algorithms
    │   └── utils/                          # Utility functions supporting TRM analysis and visualization
    │       ├── __init__.py                 # Initializes 'utils' as a Python sub-package
    │       ├── helper_functions.py         # Provides general helper functions for data processing or common tasks
    │       └── visualization_helpers.py    # Contains functions for visualizing TRM results on images
    ├── data/                               # Directory for sample input images
    │   └── sample_1.jpg                    # Sample grayscale image (e.g., of a lumbar spine) for testing
    ├── output/                             # Directory where generated output images are saved
    ├── main.py                             # Main script to run TRM analysis and demonstrations
    ├── pyproject.toml                      # Project metadata and build configuration (using modern Python packaging standards)
    ├── requirements.txt                    # Lists all Python dependencies required for the project
    └── README.md                           # The main documentation file for this repository

You can run the main demonstration script:
```bash
python main.py
```

### Example 1: Fast Link Remainder
This example demonstrates the use of `python TRM.TRM_fast_link_remainder` for a quick topological analysis, visualizing the link remainder counts.
```python 
# In your script (e.g., process_images.py)
import os
import cv2
import TRM_modules.TRM as TRM
import TRM_modules.visualization as TRM_vis

# Assuming img is your loaded grayscale image (e.g., from cv2.imread)
# And filename_stem, ext, output_dir are defined (e.g., in process_images.py)

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
```


### Example 2: Weighted TRM with Directional Analysis
This example showcases the more comprehensive `TRM.TRM_weighted` method, which provides both link remainder counts and directional information (`mem_THI`), allowing for two distinct visualizations.
```python 
# In your script (e.g., process_images.py)
import os
import cv2
import TRM_modules.TRM as TRM
import TRM_modules.visualization as TRM_vis
import numpy as np # Needed for np.real/np.imag if visualizing directions

# Assuming img is your loaded grayscale image (e.g., from cv2.imread)
# And filename_stem, ext, output_dir are defined (e.g., in process_images.py)

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
```

## Project Structure
The core logic of this project is organized as a Python package `TRM_modules`:

    TRM-Image-Analysis-Tools/
    ├── TRM_modules/
    │   ├── __init__.py                     # Initializes 'TRM_modules' as a Python package
    │   ├── TRM.py                          # Contains the core Topological Relation Mapping (TRM) algorithms
    │   └── utils/                          # Utility functions supporting TRM analysis and visualization/
    │       ├── __init__.py                 # Initializes 'utils' as a Python sub-package
    │       ├── helper_functions.py         # Provides general helper functions for data processing or common tasks
    │       └── visualization_helpers.py    # Contains functions for visualizing TRM results on images
    ├── data/                               # Directory for sample input images
    │   └── sample_1.jpg                    # Sample grayscale image (e.g., of a lumbar spine) for testing
    ├── output/                             # Directory where generated output images are saved
    ├── main.py                             # Main script to run TRM analysis and demonstrations
    ├── pyproject.toml                      # Project metadata and build configuration (using modern Python packaging standards)
    ├── requirements.txt                    # Lists all Python dependencies required for the project
    └── README.md                           # The main documentation file for this repository

## Contributing
Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature-name).
3. Make your changes.
4. Commit your changes (git commit -m 'Add new feature').
5. Push to the branch (git push origin feature/your-feature-name).
6. Open a Pull Request.

Please ensure your code adheres to good practices and includes relevant tests.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact
Got questions or inquiries? The best way to reach us is by opening an issue on this repository.

You can also contact Podchara Klinwichit directly at 63810055@go.buu.ac.th.

