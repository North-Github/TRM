import numpy as np 
from skimage.draw import line

def find_8_neighbors(point, step_size, max_size):
    x, y = point
    neighbor_offsets = [
        (-step_size, -step_size), (0, -step_size), (step_size, -step_size),
        (-step_size,   0),           (step_size,   0),
        (-step_size,  step_size), (0,  step_size), (step_size,  step_size)
    ]

    neighbors = [(x + dx, y + dy) for dx, dy in neighbor_offsets]
    neighbors = np.array(neighbors)
    neighbors[neighbors<0] = 0
    neighbors[neighbors>=max_size] = max_size - 1
    neighbors = np.array(neighbors, dtype=np.uint16)
    return neighbors

def max_intensity_along_line(img, point1, point2):
    """
    Get the maximum intensity value along the straight line between two points.
    
    Parameters:
        img: 2D NumPy array (grayscale image)
        point1, point2: (x, y) tuples or lists

    Returns:
        max_intensity: maximum pixel intensity along the line
    """
    rr, cc = line(int(point1[1]), int(point1[0]), int(point2[1]), int(point2[0]))  # (row, col) = (y, x)
    intensities = img[rr, cc]
    return np.max(intensities)