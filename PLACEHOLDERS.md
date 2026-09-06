# Placeholder checklist

Turn on **Highlight placeholder copy** (bottom-right of the page) to see each
remaining one in context. The counter beside the toggle should read **0** when
you're done. It currently reads **15**.

Prices and the 24-hour turnaround claim have been removed from the page
entirely rather than left as placeholders — see the README's "Pricing"
section. The gallery photography is tracked separately too, in
`assets/img/generated/README.md`, since it isn't text copy.

## Already filled in — real, verified

- **Phone** `(207) 800-6690` — top bar, hero CTA, estimate panel, footer, mobile
  call bar, and every `tel:` href
- **Email** `torrescleaning40@gmail.com` — top bar, estimate panel, footer, and
  every `mailto:` href
- **Facebook / Messenger** `facebook.com/profile.php?id=61591036726888`
- **Business name** and the "Landscaping & Property Maintenance" tagline
- **Service lines** — lawn care, landscaping, yard cleanups and house cleaning
- **Positioning copy** — "reliable, affordable and detail-oriented", "quality
  work, honest service", "free estimates" — from their own About text
- **Location** — Portland, Maine, serving the greater Portland area. Top bar,
  hero paragraph, footer blurb, service-area intro and footer address all use
  this now. The six area chips (Portland, South Portland, Westbrook, Falmouth,
  Cape Elizabeth, Scarborough) are a reasonable reading of "greater Portland"
  — add, remove, or reorder to match what's actually covered.
- **Reviews** — the two testimonials (Owen Bernsee, Karen Nichols) are real
  recommendations copied from the Facebook page, not invented.

## Still needed

### Hours

`Mon–Sat, 7am–6pm` in the top bar, estimate panel and footer. Invented.

### Street address

The footer currently just says "Portland, ME" — no street address was
supplied. Add one if the business has a public address, or leave it as a city
only.

### Numbers — the highest-risk items on the page

Do not publish a figure you can't back up.

- `10+` years in business
- `400+` properties maintained
- `4.9★` average rating

The stats bar is three invented numbers in a row. If real figures aren't
available, delete that section rather than soften it.

Two related, softer turnaround claims are still on the page and worth a second
look even though they're not marked `.ph`: **"Same-week walk-through"** and
**"Same-week start"** on the hero estimate card, and **"the same business day"**
on the estimate form. The explicit "24-hour" version of this claim has already
been removed as unverified (see README) — these are the same kind of promise
in softer language. Keep, soften further, or remove them the same way.

### "Licensed and insured" — read this one carefully

The claim appears four times: a hero chip, a hero bullet, a floating badge on
the estimate card, and a why-us feature. **The Facebook page does not claim
either.** These are the only statements on the page that carry legal weight in
most states, so keep them only if literally true. If the business is insured but
not licensed, say exactly that instead; if neither, delete all four.

### More reviews

Only two real recommendations were available to pull from Facebook. Add more
as they come in — same markup pattern, `.quote` inside `.quotes`, no `.ph`
needed once the quote is real.

### Commercial section

`HOAs, offices, retail centers, rental portfolios and construction sites` — trim
to the property types actually serviced. Their Facebook page says "homes and
businesses" without going further.

### Gallery photography — generated, not real

The hero background, the estimate section's background, and the three "On the
job" gallery tiles are procedurally generated art in the site's palette, not
real photographs — no stock-photo host was reachable to source real ones, and
real job photos sent in chat couldn't be saved to disk this session either
(see README's "The photography" section for what happened there). See
`assets/img/generated/README.md`. The gallery section has its own `.ph` note
saying the same thing; remove that note when the photos are swapped.

## Also before launch

- [ ] Connect the estimate form to a real endpoint (see README)
- [ ] Swap the placeholder crest SVG for the real logo file
- [ ] Replace the five generated images with real job photography
- [ ] Remove the `.ph-bar` toggle, its JS block, and the `.ph` CSS rules
- [ ] Decide on the softer turnaround-time language noted above
- [ ] Add a favicon
- [ ] Fill in the `og:image` for social sharing previews
