# Profile artwork

Self-contained SVG artwork for the GitHub profile README. No JavaScript, remote fonts, image downloads, or runtime packages are used by the artwork.

## Edit and regenerate

From the repository root, with Python 3.9+:

```sh
python3 scripts/generate_profile_assets.py
python3 scripts/validate_profile.py
```

Edit the content, colors, or animation timing in `scripts/generate_profile_assets.py`, then regenerate and commit the updated SVGs. The validator checks that committed artwork matches the generator.

## Artwork variants

| Artwork | Desktop | Compact / mobile |
| --- | --- | --- |
| Introduction | `hero-{dark,light}.svg` | `hero-mobile-{dark,light}.svg` |
| Technology ribbon | `stack-{dark,light}.svg` | `stack-mobile-{dark,light}.svg` |
| Capability map | `flow-{dark,light}.svg` | `flow-mobile-{dark,light}.svg` |
| Contact banner | `connect-{dark,light}.svg` | `connect-mobile-{dark,light}.svg` |

The README selects compact artwork at viewport widths up to 640px and uses `prefers-color-scheme` for light/dark mode. The three `badge-*.svg` files are static, dark contact buttons that work on either background.

## Motion and accessibility

- Animations use embedded CSS, so they can run when GitHub displays an SVG as an image.
- `prefers-reduced-motion: reduce` selects separate `*-static-*.svg` artwork at the README level, so motion stops even in browsers that do not pass their motion preference into embedded SVG images. The embedded CSS media query is an additional safeguard; the first introduction remains visible.
- Every SVG includes a title and description; README images also have alt text.
- Essential skills and project links remain real Markdown/HTML, not text trapped inside images.
- The capability map describes separate areas of expertise; it does not claim that every project uses every technology.

GitHub may cache artwork after publication. The profile itself only updates when these files reach the repository's default branch (`main`). GitHub statistics and language cards are external services and can occasionally be unavailable or rate-limited; the local artwork does not depend on them.
