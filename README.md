# Torres Cleaning Services — Website Mockup

A multi-page static site mockup for **Torres Cleaning Services — Landscaping
& Property Maintenance**, Portland, Maine. Plain HTML, one shared stylesheet,
one shared script. No build step, no framework, no npm install — every page
is a real, independent `.html` file; nothing is templated or assembled at
request time.

```
index.html                        homepage
about.html                        under construction
contact.html                      under construction
estimate.html                     the real, functional free-estimate page
services/index.html               services overview (all 6 services)
services/lawn-care-mowing.html
services/landscape-design-installation.html
services/mulch-beds-weed-control.html
services/tree-shrub-trimming.html
services/property-cleanups-hauling.html
assets/css/styles.css             all styling
assets/js/main.js                 mobile nav, dropdown, form mock, placeholder toggle
assets/img/logo.jpg                the real crest logo
assets/img/photos/                 six real job photos (see photos/README.md)
scripts/build-artifact.mjs         inlines the homepage into one shareable file
```

## Site structure

The primary nav is the same on every page: a **Services** dropdown (overview
+ the five pages above), Why Us / Reviews / Service Area (anchors back to
sections on the homepage), About, Contact, and a Free Estimate button. House
Cleaning — the business's sixth real service — has a card on the services
overview page but no dedicated page of its own; only five services got the
"one page per service" treatment, per how this was scoped.

The dropdown is a plain `<details>/<summary>` — it works with zero JavaScript.
`assets/js/main.js` only adds the conveniences a real menu needs on top of
that: closing on an outside click, on Escape, and after a link inside it is
chosen.

**No templating engine** stands behind any of this — the header, nav, and
footer are duplicated in every `.html` file, same as the rest of this project.
That was a deliberate call to match the project's existing "no build step"
posture rather than introduce one. The tradeoff: editing shared chrome (the
nav, the footer) means editing it in all nine files, not one. There's no
tooling here to keep them in sync — if that becomes painful, templating (even
something as simple as a shared include file assembled at edit time) would be
the natural next step, but hasn't been added.

## Viewing it

Open `index.html` directly, or serve it:

```sh
npx http-server -p 8080 .   # then open http://localhost:8080
```

## The placeholder system

Contact details, service lines, positioning copy, the logo, the photography
and the reviews are all **real**, taken from the business's Facebook page.
Everything still unverified — service-area town list, stats, and the
licensing claim — is wrapped in `<span class="ph">`.

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

`assets/img/logo.jpg` is the real crest — shield, crown, TS monogram, crossed
tools over a house, embroidered-patch style. It appears four times: header,
hero estimate card, a small badge in the "Torres Standard" panel, and the
footer. The panel and footer instances sit on dark backgrounds, so they're
wrapped in a `.crest-badge` — a small white rounded mount — so the logo reads
as a mounted patch rather than a floating cutout. See `.brand__crest` and
`.crest-badge` in `assets/css/styles.css`.

## Design notes

- **Palette** comes from the crest: near-black charcoal (`--charcoal`,
  `--charcoal-3`) and off-white, with a single grass green (`--green`) as the
  accent, plus gold reserved for review stars.
- **Type**: Oswald (condensed, uppercase) for headings, nav and buttons, echoing
  the banner lettering on the crest; Inter for body copy. Both load from Google
  Fonts with full system fallbacks — the page is designed to survive the fonts
  failing to load.
- **Photography** is real — six job photos from the business's Facebook page.
  See "The photography" below for how they got here.
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

## Hours

There's no hours line on the page. Facebook lists this business as always
open, so the site says exactly that (top bar, estimate panel, footer) instead
of inventing a schedule.

## The photography

Six real job photos and the real logo (`assets/img/logo.jpg`,
`assets/img/photos/*.jpg`) — see `assets/img/photos/README.md` for what each
one is used for.

Getting them here took three attempts, worth knowing about if this comes up
again:

1. **Facebook and every stock-photo host** (Unsplash, Pexels, Pixabay) are
   blocked outright by this build environment's network policy — confirmed by
   direct `403`s at the proxy level, not something fixable mid-session.
2. **Images pasted straight into chat** didn't persist to a file this
   assistant could read — they were visible in conversation but produced no
   file path, so there was no pixel data to copy into the repo. (A procedurally
   generated stand-in — lawn/hedge/mulch art rendered from noise in the site's
   palette — filled in temporarily; it's gone now that real photos are in.)
3. **Google Drive worked.** The client uploaded the logo and six photos to a
   Drive folder, and Drive's MCP connector (already available in this session)
   could read them directly — first-party connector, not subject to the same
   network block. That's the path that actually got real assets into the repo.

If more photos need to go in later, Drive is the reliable route, not pasting
into chat.

## The estimate form

`assets/js/main.js` intercepts the submit and shows a "nothing was actually
sent" message. **It is not connected to anything.** Point it at a real endpoint
(Formspree, Netlify Forms, a CRM webhook) before launch, or swap the whole form
for a `mailto:` link.

## Shareable single file

```sh
node scripts/build-artifact.mjs   # writes dist/torres-homepage.html
```

Inlines the CSS, JS and homepage images (as base64 data URIs) into one
self-contained file that can be emailed or opened from a USB stick with no
server. **This bundles the homepage only** — now that the site is multi-page,
a true single file can't represent all nine pages at once. Nav links inside
that bundle to About, Contact, Free Estimate, or any Services page won't
resolve; anchor links back to the homepage's own sections (Why Us, Reviews,
Service Area) still work fine. To see the full site navigate, serve the
whole directory (see "Viewing it" above) rather than relying on this bundle.
