import numpy as np
import functions as fn

def TRM_single_point(
    img: np.ndarray,
    point: tuple,
    step_size: int = 15,
    weights: np.ndarray = np.array([
        [-1-1j, 0-1j, 1-1j],
        [-1,    0,   1],
        [-1+1j, 0+1j, 1+1j]
    ]),
    scale: bool = False,
    return_points: bool = False
) -> complex | tuple:
    """
    Computes the THI value at a single point using the Turbulent Region Model.

    Parameters:
        img (np.ndarray): 2D input image (grayscale).
        point (tuple): (y, x) coordinate of the point.
        step_size (int): Distance to find neighbors.
        weights (np.ndarray): Complex weights (default: 3x3 kernel).
        scale (bool): Whether to scale THI by gradient stats.
        return_points (bool): If True, return (THI, neighbor_points).

    Returns:
        complex: THI value, or (THI, neighbors) if return_points is True.
    """
    # Flatten weights and remove center (index 4 in 3x3)
    weights_flat = weights.flatten()
    weights_flat = np.delete(weights_flat, 4)

    h, w = img.shape

    # Compute gradients
    dx, dy = np.gradient(img)
    magnitude = np.hypot(dx, dy)

    # Compute gradient threshold
    mean = np.mean(magnitude)
    std = np.std(magnitude)
    thresh = mean + 2 * std

    # Find 8 neighbors
    near_points = fn.find_8_neighbors(point, step_size=step_size, max_size=h)

    mem_link_state = np.ones(8)

    for i, near_point in enumerate(near_points):
        max_value = fn.max_intensity_along_line(magnitude, point, near_point)
        if max_value >= thresh:
            mem_link_state[i] = 0

    THI = np.sum(mem_link_state * weights_flat)

    if scale:
        THI /= (mean + 1e-8)  # Avoid divide by zero

    if return_points:
        return THI, near_points

    return THI


def TRM_weighted(
    img: np.ndarray,
    step_size: int = 15,
    weights: np.ndarray = np.array([
        [-1-1j, 0-1j, 1-1j],
        [-1,    0,    1],
        [-1+1j, 0+1j, 1+1j]
    ]),
    scale: bool = False,
    return_points: bool = True
) -> tuple[list[list[int]], list[complex]]:
    """
    Computes THI values over a grid of points using the Turbulent Region Model.

    Parameters:
        img (np.ndarray): 2D grayscale image.
        weights (np.ndarray): 3x3 complex weights matrix.
        step_size (int): Grid spacing for sampling points.
        scale (bool): Option to scale THI by gradient stats (currently unused).
        return_points (bool): If True, return grid points with THI values.

    Returns:
        tuple: (intersection_points, mem_THI)
    """
    # Flatten weights and remove center
    weights_flat = weights.flatten()
    weights_flat = np.delete(weights_flat, 4)

    h, w = img.shape

    # Compute gradient magnitude
    dx, dy = np.gradient(img)
    magnitude = np.hypot(dx, dy)

    # Compute threshold
    mean = np.mean(magnitude)
    std = np.std(magnitude)
    thresh = mean + 2 * std

    # Generate grid points
    intersection_points = [
        [i, j]
        for i in range(0, h, step_size)
        for j in range(0, w, step_size)
    ]

    mem_THI = []

    for point in intersection_points:
        near_points = fn.find_8_neighbors(point, step_size=step_size, max_size=h)
        mem_link_state = np.ones(8)

        for idx, near_point in enumerate(near_points):
            max_value = fn.max_intensity_along_line(magnitude, point, near_point)
            if max_value >= thresh:
                mem_link_state[idx] = 0

        THI = np.sum(mem_link_state * weights_flat)

        if scale:
            THI /= (mean + 1e-8)  # Safe scale to avoid division by zero

        mem_THI.append(THI)

    mem_THI = np.array(mem_THI, dtype=np.complex128)
    if return_points:
        return intersection_points, mem_THI

    return mem_THI

def TRM_link_remainder(
    img: np.ndarray,
    step_size: int = 15,
    scale: bool = False,
    return_points: bool = True
) -> tuple[list[list[int]], list[int]]:
    """
    Computes the link remainder for each grid point using the Turbulent Region Model.

    Parameters:
        img (np.ndarray): 2D grayscale image.
        step_size (int): Grid spacing for sampling points.
        scale (bool): Unused flag, placeholder for future scaling.
        return_points (bool): If True, return points with their link remainder counts.

    Returns:
        tuple: (intersection_points, link_counts)
    """
    h, w = img.shape

    # Compute gradient magnitude
    dx, dy = np.gradient(img)
    magnitude = np.hypot(dx, dy)

    mean = np.mean(magnitude)
    std = np.std(magnitude)
    thresh = mean + 2 * std

    # Generate grid points
    intersection_points = [
        [i, j]
        for i in range(0, h, step_size)
        for j in range(0, w, step_size)
    ]

    mem_links = []

    for point in intersection_points:
        near_points = fn.find_8_neighbors(point, step_size=step_size, max_size=h)
        # Only use bottom & diagonal neighbors (idx 4, 5, 6, 7)
        for idx in [4, 5, 6, 7]:
            neighbor = near_points[idx]
            mem_links.append([point, neighbor])

    mem_links = np.array(mem_links)

    # Initialize link states
    mem_link_state = np.ones(mem_links.shape[0])

    for i, (p1, p2) in enumerate(mem_links):
        max_value = fn.max_intensity_along_line(magnitude, p1, p2)
        if max_value >= thresh:
            mem_link_state[i] = 0

    # Get remaining (filtered) links
    filter_links = mem_links[mem_link_state == 0].reshape(-1, 2)
    filter_points = filter_links.reshape(-1, 2)

    # Find unique points and their link counts
    unique_points, counts = np.unique(filter_points, axis=0, return_counts=True)

    # Count links for each grid point
    mem_link_counts = []
    for point in intersection_points:
        matches = np.all(unique_points == point, axis=1)
        link_count = counts[matches][0] if np.any(matches) else 0
        mem_link_counts.append(link_count)
    mem_link_counts = np.array(mem_link_counts)
    if return_points:
        return intersection_points, mem_link_counts

    return mem_link_counts
 