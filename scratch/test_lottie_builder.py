import json

def make_lottie_kf(t, s, e=None):
    kf = {
        "t": t,
        "s": s if isinstance(s, list) else [s],
        "i": {"x": [0.45, 0.45, 0.45] if isinstance(s, list) else [0.45], "y": [1.0, 1.0, 1.0] if isinstance(s, list) else [1.0]},
        "o": {"x": [0.55, 0.55, 0.55] if isinstance(s, list) else [0.55], "y": [0.0, 0.0, 0.0] if isinstance(s, list) else [0.0]}
    }
    if e is not None:
        kf["e"] = e if isinstance(e, list) else [e]
    return kf

# Test building lottie JSON and checking size
# In lottie: shapes can use bezier path with "ks": {"a": 0, "k": {"c": True, "i": [...], "o": [...], "v": [...]}}
print("Lottie helper ready.")
