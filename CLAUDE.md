# Torres Cleaning Services — site notes

Static multi-page HTML site. No build step, no framework, no npm install.
Every page is a real, independent `.html` file; header/nav/footer are
duplicated by hand across pages and kept in sync manually.

## Writing style (applies to all visible copy, every page)

- No em dashes, anywhere in user-facing copy. Use a period, comma, or
  colon instead, whichever reads most naturally for that sentence.
- Avoid obvious AI-sounding phrasing: filler asides ("and that's fine"),
  hedge-then-reassure constructions, generic marketing cliches ("seamless",
  "elevate", "unlock", "peace of mind"). Write plainly, the way the actual
  business owner would.

## Content rules

- Never invent facts, numbers, dates, credentials, or reviews. Anything
  unverifiable gets cut, not filled in with a placeholder claim.
- Only real photos of Torres Cleaning Services' own completed work (no
  stock or generated imagery). If a real photo isn't available for
  something, use an honest placeholder that doesn't pretend, rather than
  substituting a generic or fabricated image.

## Quality bar

The homepage as of commit `2fa3805` on `torres-spec-pitch-rework` (PR #1)
is the reference quality level for this project going forward: a real,
considered design system (not a default template); a Services grid that's
an actual photo gallery of completed work, not icon-and-bullet cards; the
two real reviews given real visual weight (green blocks) instead of a
padded testimonial grid; every section shaped differently rather than
repeating the same card pattern; no templated-AI tells (eyebrow-and-rule
kickers, arrow-appended links, hover-lift-everything); and the writing
style and content rules above already applied throughout. Match this bar
on future homepage or landing-page work for this business, not a generic
default.
