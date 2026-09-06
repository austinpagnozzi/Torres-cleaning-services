# Generated photography

These five images stand in for real photography. Facebook, and every stock-
photo host tried (Unsplash, Pexels, Pixabay), are unreachable from this build
environment — the network policy here blocks them outright — so nothing could
be fetched or hotlinked. Rather than ship the page with no imagery at all,
`scripts/generate_images.py` procedurally renders lawn, hedge and mulch
textures in the site's own palette using Pillow and numpy: layered noise
standing in for grass blades and mowing stripes, not a photograph of any real
property.

| File | Used for |
|---|---|
| `hero-lawn.jpg` | Hero section background |
| `estimate-bg.jpg` | Estimate section background (darker crop, same technique) |
| `gallery-lawn.jpg` | "On the job" gallery — Mow, edge & blow |
| `gallery-hedge.jpg` | "On the job" gallery — Hedge & shrub trimming |
| `gallery-mulch.jpg` | "On the job" gallery — Mulch, beds & edging |

**Replace all five with real job photography before launch.** The gallery
section header carries a placeholder note (`.ph`) saying exactly that, and it
should be removed at the same time the images are swapped.

To regenerate with different tuning (darker, different stripe angle, etc.),
edit and rerun:

```sh
python3 -m venv .venv && source .venv/bin/activate   # or use your own env
pip install pillow numpy
python3 scripts/generate_images.py
```

Swapping in real photos is a drop-in: keep the same five filenames and
dimensions (or update the `width`/`height` attributes on the `<img>` tags in
`index.html` and the `background-size: cover` rules already handle any aspect
ratio). After replacing them, rerun `node scripts/build-artifact.mjs` to
refresh the single-file build.
