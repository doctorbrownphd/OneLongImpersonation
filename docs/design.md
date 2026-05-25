# One Long Impersonation -- Design System
## v1.0 / May 2026

---

## Aesthetic

Prosecution exhibit meets data journalism. Every visualization is evidence. The design is the courtroom. The aesthetic says: this is serious, this is sourced, this is citable.

The mockup (Fraunces variable font, midnight navy backgrounds, gold accents, forensic crosshair framing) established the visual language. The production system preserves it exactly.

---

## Color Tokens

```css
/* Backgrounds */
--ink:        #14142b;   /* deep midnight navy -- primary bg */
--ink-2:      #1d1d3a;   /* card surfaces */
--ink-3:      #262648;   /* interactive hover states */
--rule:       #2e2e55;   /* divider lines on dark */

/* Paper surfaces (light sections) */
--paper:      #f1ece1;   /* warm parchment */
--paper-2:    #e8e1d1;   /* secondary paper */
--paper-3:    #ddd3bd;   /* tertiary paper */
--bone:       #f6f2ea;   /* lightest surface */

/* Text */
--cream:      #efe8d6;   /* primary text on dark -- never use #fff */
--cream-2:    #d8cfb6;   /* secondary text on dark */
--mute:       #8a8aa3;   /* tertiary text, metadata */
--rule-paper: #c8bea3;   /* dividers on paper */

/* Accents */
--gold:       #d4a017;   /* primary accent -- prosecution gold */
--gold-hot:   #e8b727;   /* hover/active gold */
--blood:      #b03434;   /* prosecution red -- used sparingly */
--blood-deep: #7a1f1f;   /* deep red for emphasis */
--moss:       #5f7d56;   /* "got it right" green -- Chapter 06 */
```

**Rules:**
- Never use pure white (#fff). Use --cream on dark, --ink on light.
- Gold is the primary accent. Blood is reserved for: never-inducted markers, prosecution emphasis, causation caveats.
- Moss appears only in Chapter 06 (The Other Side) and for "inducted" indicators.

---

## Typography

```css
--serif:   "Fraunces", Georgia, serif;
--sans:    "Inter", system-ui, sans-serif;
--mono:    "JetBrains Mono", ui-monospace, monospace;
```

**Usage:**
- **Fraunces (serif):** Display headlines, pull quotes, opening statements. Variable font with SOFT, WONK, and opsz axes.
- **Inter (sans):** Body text, descriptions, methodology prose.
- **JetBrains Mono (mono):** Data labels, exhibit labels, metadata, statistical figures, navigation.

**Type classes:**
- `.display` -- large headlines (SOFT 30, opsz 144, WONK 0)
- `.display-wonk` -- stylistic alternate headlines (SOFT 60, WONK 1)
- `.serif` -- body serif (SOFT 30, opsz 24)
- `.mono` -- data labels (ss02, ss03 features)
- `.smallcaps` -- section labels (Inter, uppercase, 0.18em tracking, 11px)

---

## Section Primitives

```css
.section          /* position: relative; padding: 120px 0 */
.section--ink     /* dark bg (--ink), light text (--cream) */
.section--ink2    /* slightly lighter dark (--ink-2) */
.section--paper   /* parchment bg (--paper), dark text (--ink) */
.section--bone    /* lightest bg (--bone), dark text (--ink) */

.container        /* max-width: 1240px, centered, 56px horizontal padding */
.container--wide  /* max-width: 1480px */
.container--narrow /* max-width: 880px */
```

---

## Exhibit Framing

Every visualization is an exhibit in the prosecution:

**Exhibit label** (`.exhibit-label`):
```
--- Ex. 001-A -- Documented Influence Pairs
```
Monospace, 11px, 0.22em tracking, uppercase, gold. Horizontal line before text.

**Crosshair corner ticks:** Four L-shaped ticks at SVG corners. Gold at 40% opacity. 12px length. These are the forensic framing element -- they say "this is evidence."

**Verdict stamp** (`.stamp`):
```
STRONG CASE FOR INDUCTION
```
Blood-red border, rotated -3deg, serif font. Used in the Docket.

---

## Genre Colors

```
Classic Rock:  #d4a017  (gold)
Soul/R&B:      #b03434  (blood)
Pop:           #c47a3a  (terracotta)
Folk/Country:  #8a7d48  (drab olive)
Hip-Hop:       #5a6f8a  (slate blue)
Heavy Metal:   #3d4a5c  (dark gray-blue)
Punk:          #7a4a8a  (purple)
Electronic:    #5f7d56  (moss green)
Blues/Early:    #5c3a2a  (dark brown)
Disco/Dance:   #8a5a6f  (mauve)
```

---

## Responsive Breakpoints

- **1200px+:** Full desktop layout
- **768px:** Tablet. Grids collapse. Padding reduces to 24px.
- **375px:** Mobile minimum. Single column. Font size 15px. Sections 60px vertical padding. All visualizations must be comprehensible.

---

## What Never Ships

- Pure white text or backgrounds
- A visualization without exhibit framing (label + crosshairs)
- A chart without a legend
- A statistical finding without a causation caveat where applicable
- Color as the sole encoding of meaning (must have shape, pattern, or label redundancy)
- An em dash
