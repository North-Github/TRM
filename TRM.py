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


def TRM_weigthed(img, weights=np.array([[-1-1j, 0-1j, 1-1j],[-1, 0, 1],[-1+1j,0+1j,1+1j]]), step_size = 15, scale=False, return_points = False):
    weights = weights.reshape(1, -1)[0]
    weights = np.delete(weights, 4)
    h, w = img.shape
    # step_size = 15
    dx, dy = np.gradient(img)
    magnitude = np.sqrt(dx**2 + dy**2)
    mean = np.average(magnitude)
    std = np.std(magnitude)
    thresh = mean + 2 * std

    intersection_points = []
    mem_links = []
    for i in range(0, h, step_size):
        for j in range(0, w, step_size):
            point = [i, j]
            intersection_points.append(point)
    mem_THI = []
    for point in intersection_points:
        near_points = fn.find_8_neighbors(point, step_size=step_size, max_size=h)
        mem_link_state = np.ones(8)
        for i, near_point in enumerate(near_points):
            # print(point, near_point)
            max_value = fn.max_intensity_along_line(magnitude, point, near_point)
            if max_value>=thresh:
                mem_link_state[i] = 0

        THI = np.sum(mem_link_state * weights)
        mem_THI.append(THI)
        # print(mem_link_state, mem_link_state * weights, 'THI', THI)
        # quit()
    return intersection_points, mem_THI

def TRM(img, step_size = 15, scale=False, return_points = False):
    h, w = img.shape
    # step_size = 15
    dx, dy = np.gradient(img)
    magnitude = np.sqrt(dx**2 + dy**2)
    mean = np.average(magnitude)
    std = np.std(magnitude)
    thresh = mean + 2 * std

    intersection_points = []
    mem_links = []
    for i in range(0, h, step_size):
        for j in range(0, w, step_size):
            point = [i, j]
            intersection_points.append(point)
            near_points = fn.find_8_neighbors(point, step_size=step_size, max_size=h)
            # print(point, near_points)
            for idx in [4, 5, 6, 7]:  # Bottom and diagonal neighbors
                neighbor = near_points[idx]
                mem_links.append([point, neighbor])
    mem_links = np.array(mem_links)
    mem_link_state = np.ones((mem_links.shape[0]))
    # print(mem_links, mem_links.shape, mem_link_state.shape)
    for i, points in enumerate(mem_links):
        p1 = points[0]
        p2 = points[1]
        max_value = fn.max_intensity_along_line(magnitude, p1, p2)
        if max_value>=thresh:
            mem_link_state[i] = 0
    filter_links = mem_links[mem_link_state==0].reshape(-1, 2)
    filter_points = filter_links.reshape(-1, 2)

    # Get unique points and their counts
    unique_points, counts = np.unique(filter_points, axis=0, return_counts=True)
    delta_t = t2 - t1
    if return_points:
        mem_link_counts = []
        for points in intersection_points:
            target_point = np.array(points)
            # Find matching rows
            matches = np.all(unique_points == target_point, axis=1)
            # Get indices
            indices = np.where(matches)[0]
            link_count = 0
            if len(indices) != 0:
                link_count = counts[indices[0]]
                
            print(points, link_count)

            mem_link_counts.append(link_count)

        return intersection_points, mem_link_counts, delta_t
 