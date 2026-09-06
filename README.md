# Torres Cleaning Services — Homepage Mockup

A single-page homepage mockup for **Torres Cleaning Services — Landscaping &
Property Maintenance**. Static HTML, one stylesheet, one small script. No build
step, no framework, no npm install.

```
index.html            the page
assets/css/styles.css all styling
assets/js/main.js     mobile nav, form mock, placeholder toggle
assets/img/           drop the real logo here (see below)
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
area, prices, stats, review text and the licensing claims — is wrapped in
`<span class="ph">`.

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
- **No photography** is used. The hero uses a sample-estimate card instead of a
  stock image, so the mockup doesn't depend on photos that don't exist yet.
  Real job photos would be a strong upgrade — before/after shots especially.
- Fully responsive; verified with no horizontal overflow at 1440px and 390px.
  Below 660px a sticky Call / Free Estimate bar pins to the bottom.
- Respects `prefers-reduced-motion`, has a skip link, labelled form fields, and
  `aria-expanded` wired to the mobile menu.

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
