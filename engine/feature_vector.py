from typing import List, NewType
import numpy as np

FeatureVector = NewType("FeatureVector", np.ndarray)

# To sum feature vectors, we want the latest non-zero value of a column
uf_sum = np.frompyfunc(lambda a, b: a if b == 0 else b, 2, 1)


def fv_sum(fvs: List[FeatureVector]) -> FeatureVector:
    return uf_sum.reduce(fvs).astype(np.int8)