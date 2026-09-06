# Torres Cleaning Services — Homepage Mockup

A single-page homepage mockup for **Torres Cleaning Services — Landscaping &
Property Maintenance**. Static HTML, one stylesheet, one small script. No build
step, no framework, no npm install.

```
index.html                  the page
assets/css/styles.css       all styling
assets/js/main.js           mobile nav, form mock, placeholder toggle
assets/img/                 drop the real logo here (see below)
assets/img/generated/       procedurally generated photography (see below)
scripts/generate_images.py  regenerates the imagery above
scripts/build-artifact.mjs  inlines everything into one shareable file
```

## Viewing it

Open `index.html` directly, or serve it:

```sh
npx http-server -p 8080 .   # then open http://localhost:8080
```

## The placeholder system

Contact details, service lines and positioning copy are **real**, taken from the
business's Facebook About page. Everything still unverified — hours, service
area, stats, review text and the licensing claims — is wrapped in
`<span class="ph">`. Prices have been removed from the page entirely rather
than marked as placeholders (see "Pricing" below), and the same goes for the
turnaround-time claims that used to sit alongside them.

There's a toggle in the bottom-right corner of the page: **Highlight
placeholder copy**. Flip it on and every one lights up yellow, with a live
count. Nothing should ship until that count is zero.

To find them all in the source:

```sh
grep -n 'class="ph"' index.html
```

See `PLACEHOLDERS.md` for the checklist grouped by what you need to supply.

Before launch, delete the `.ph-bar` element at the bottom of `index.html`, the
placeholder block at the end of `assets/js/main.js`, and the `.ph` / `.ph-bar`
rules in the stylesheet. The `class="ph"` attributes themselves are inert once
those rules are gone, but stripping them is tidier.

## The logo

The header, footer, estimate card and "Torres standard" panel currently use an
**inline SVG approximation** of the crest — shield, crown, TS monogram, crossed
tools over a house, banner. It's a stand-in so the layout reads correctly; it is
not the real mark.

To swap in the real logo: drop the file in `assets/img/` and replace each
`<svg class="brand__crest" …>` with, for example:

```html
<img class="brand__crest" src="assets/img/logo.png" alt="Torres Cleaning Services">
```

There are four crest instances (`grep -c 'viewBox="0 0 100 122"' index.html`).
The footer one is tinted for a dark background via `--crest-paper`; an `<img>`
of a white-on-transparent logo replaces that behaviour.

A transparent-background PNG or, better, an SVG will look sharpest. The current
supplied artwork is monochrome, which is what the palette below was built
around.

## Design notes

- **Palette** comes from the crest: near-black charcoal (`--charcoal`,
  `--charcoal-3`) and off-white, with a single grass green (`--green`) as the
  accent, plus gold reserved for review stars.
- **Type**: Oswald (condensed, uppercase) for headings, nav and buttons, echoing
  the banner lettering on the crest; Inter for body copy. Both load from Google
  Fonts with full system fallbacks — the page is designed to survive the fonts
  failing to load.
- **Photography** is procedurally generated, not stock — no stock-photo host
  was reachable from this build environment (see "The photography" below).
  Real job photos, before/after especially, would be a strong upgrade.
- Fully responsive; verified with no horizontal overflow at 1440px and 390px.
  Below 660px a sticky Call / Free Estimate bar pins to the bottom.
- Respects `prefers-reduced-motion`, has a skip link, labelled form fields, and
  `aria-expanded` wired to the mobile menu.

## Pricing

There are no prices on the page. An earlier draft had per-service placeholder
prices; they've been removed entirely rather than left as placeholders, since
a wrong number here is worse than no number — every service card and the hero
estimate card now just list what's included and point to "Get a quote." Add
real prices back service-by-service whenever they're settled, or leave the page
quote-only.

Turnaround-time claims ("24-hour estimate," "within 24 hours") have also been
removed for the same reason — none were verified. `PLACEHOLDERS.md` still
flags the softer "same-week" and "same business day" language that remains,
in case that should go too.

## The photography

Five images live in `assets/img/generated/`: the hero background, the estimate
section's background, and three tiles in the "On the job" gallery (lawn
stripes, a trimmed hedge, a mulch bed). Facebook and every stock-photo host
this build tried (Unsplash, Pexels, Pixabay) are blocked by this environment's
network policy, so none of them are hotlinked or downloaded photographs —
they're procedurally rendered in Python (Pillow + numpy) from layered noise,
tuned to the site's own charcoal-and-green palette rather than borrowed from
somewhere else. See `assets/img/generated/README.md` for how to regenerate or
replace them — swapping in real job photos is a same-filename drop-in.

Real job photos were sent in chat once, as a batch of four. Only images the
harness explicitly persists to disk are usable here — they arrive with a
file path — and none of that batch got one; the one review-screenshot sent
alongside them did, and its text is what's now in the Reviews section. So the
four photos were visible in conversation but never became files this
assistant could read pixel data from or copy into the repo. If you want them
in, resend them (one at a time is more likely to persist reliably than a
batch) and they can be swapped in the same way the crest logo eventually
should be — see "The logo" above.

## The estimate form

`assets/js/main.js` intercepts the submit and shows a "nothing was actually
sent" message. **It is not connected to anything.** Point it at a real endpoint
(Formspree, Netlify Forms, a CRM webhook) before launch, or swap the whole form
for a `mailto:` link.

## Shareable single file

```sh
node scripts/build-artifact.mjs   # writes dist/torres-homepage.html
```

Inlines the CSS and JS into one self-contained file that can be emailed or
opened from a USB stick with no server.
