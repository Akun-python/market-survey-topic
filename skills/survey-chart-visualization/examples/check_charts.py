from pathlib import Path
from PIL import Image

root = Path(__file__).parent / "output"
expected = [
    "fig_01_gender.png", "fig_02_radar.png", "fig_03_cluster.png",
    "fig_04_forecast.png", "fig_05_heatmap.png",
]
missing = [x for x in expected if not (root / x).exists()]
bad = []
for x in expected:
    p = root / x
    if p.exists():
        im = Image.open(p)
        if im.width < 1000 or im.height < 600:
            bad.append((x, im.size))
print("expected", len(expected), "missing", missing, "bad_size", bad)
assert not missing and not bad
