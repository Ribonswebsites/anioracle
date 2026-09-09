from pathlib import Path

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
text = index.read_text()

# The user requested the supplied artwork alone on the intro screen.
text = text.replace('  <img class="splash-3d-logo" src="./assets/anioracle-logo-3d-web.webp" alt="AniOracle 3D logo">\n', '')
text = text.replace('  <img class="splash-3d-logo" src="./assets/anioracle-logo-3d.png" alt="AniOracle 3D logo">\n', '')

# Replace shimmer-only motion with visible, restrained drift plus color movement.
text = text.replace('animation: ao-text-shimmer 9s linear infinite;', 'animation: ao-text-drift 4.5s ease-in-out infinite alternate, ao-text-shimmer 9s linear infinite;')
text = text.replace('animation: ao-marquee-right 42s linear infinite;', 'animation: ao-marquee-right 18s linear infinite;')
text = text.replace('@keyframes ao-text-shimmer { to { background-position: -240% center; } }', '@keyframes ao-text-drift { from { transform: translateX(-10px); } to { transform: translateX(10px); } }\n@keyframes ao-text-shimmer { to { background-position: -240% center; } }')
text = text.replace('@media (prefers-reduced-motion: reduce) { .sec-title, .hero-title, .ao-marquee-track { animation: none !important; } }', '@media (prefers-reduced-motion: reduce) { .sec-title, .hero-title, .ao-marquee-track { animation: none !important; } }')

index.write_text(text)
print('Removed center 3D overlay and enabled visible text drift plus faster looping rail')
