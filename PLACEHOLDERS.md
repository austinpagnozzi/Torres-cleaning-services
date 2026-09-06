# Placeholder checklist

Turn on **Highlight placeholder copy** (bottom-right of the page) to see each
remaining one in context. The counter beside the toggle should read **0** when
you're done. It currently reads **11**.

Prices and every turnaround-time guarantee (24-hour, hours of operation) have
been removed from the page entirely rather than left as placeholders — see
the README's "Pricing" and "Hours" sections.

## Already filled in — real, verified

- **Phone** `(207) 800-6690`, **email** `torrescleaning40@gmail.com`,
  **Facebook** — every instance and every `tel:`/`mailto:` href.
- **Business name**, tagline, and **the real crest logo** (`assets/img/logo.jpg`,
  four places — see README's "The logo").
- **Service lines** — lawn care, landscaping, yard cleanups, house cleaning.
- **Positioning copy** — "reliable, affordable and detail-oriented", "quality
  work, honest service", "free estimates" — from their own About text.
- **Location** — Portland, Maine, serving the greater Portland area. The six
  area chips (Portland, South Portland, Westbrook, Falmouth, Cape Elizabeth,
  Scarborough) are a reasonable reading of "greater Portland" — worth
  confirming town-by-town.
- **Reviews** — Owen Bernsee and Karen Nichols are real Facebook
  recommendations, not invented.
- **Hours** — "Always open", matching what Facebook lists.
- **Photography** — six real job photos in `assets/img/photos/`, sourced via
  Google Drive. See `assets/img/photos/README.md`.

## Still needed

### Numbers — the highest-risk items left on the page

Do not publish a figure you can't back up.

- `10+` years in business
- `400+` properties maintained
- `4.9★` average rating

The stats bar is three invented numbers in a row. If real figures aren't
available, delete that section rather than soften it.

Two softer turnaround claims are still on the page, not marked `.ph` but worth
a look: **"Same-week walk-through"** and **"Same-week start"** on the hero
estimate card, and **"the same business day"** on the estimate form. Same
category of unverified promise as the 24-hour claim that was already removed
— keep, soften, or remove them the same way.

### "Licensed and insured" — read this one carefully

Appears four times: a hero chip, a hero bullet, a floating badge on the
estimate card, and a why-us feature. **The Facebook page does not claim
either.** These are the only statements on the page that carry legal weight in
most states, so keep them only if literally true. If the business is insured
but not licensed, say exactly that instead; if neither, delete all four.

### More reviews

Only two real recommendations were available to pull from Facebook. Add more
as they come in — same markup pattern, `.quote` inside `.quotes`, no `.ph`
needed once the quote is real.

### Commercial section

`HOAs, offices, retail centers, rental portfolios and construction sites` — trim
to the property types actually serviced. Their Facebook page says "homes and
businesses" without going further.

### Street address

The footer just says "Portland, ME" — no street address was supplied. Add one
if the business works from a public address.

## Also before launch

- [ ] Connect the estimate form to a real endpoint (see README)
- [ ] Remove the `.ph-bar` toggle, its JS block, and the `.ph` CSS rules
- [ ] Decide on the softer turnaround-time language noted above
- [ ] Add a favicon
- [ ] Fill in the `og:image` for social sharing previews
