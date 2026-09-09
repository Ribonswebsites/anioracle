from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / "assets/anioracle-logo-3d.png"
optimized = root / "assets/anioracle-logo-3d-web.webp"
image = Image.open(source).convert("RGB")
image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
image.save(optimized, format="WEBP", quality=86, method=6)
print(f"saved {optimized} at {optimized.stat().st_size} bytes")
