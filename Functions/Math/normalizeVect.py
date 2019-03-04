def normVect(v):
    import numpy as np
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm