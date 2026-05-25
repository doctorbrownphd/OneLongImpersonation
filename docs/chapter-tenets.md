# One Long Impersonation -- Chapter Tenets
## Canonical Standards for Every Chapter -- v1.0

**Status:** CANONICAL -- all chapters conform to these standards
**Authority:** Project owner (Jeremy Haynes)
**Enforced by:** Agent team (Rosetta, Elias, Vera, Ida, Gates)
**Last updated:** May 2026

These tenets govern every chapter on this platform without exception. They are not guidelines. They are the standard against which every PR is reviewed and every chapter is shipped or held.

---

## The Nine Core Platform Tenets

1. Accuracy above all
2. No corners cut
3. Legally defensible
4. Copyright is a hard wall
5. The data is the prosecutor
6. The evidence speaks, the reader decides
7. Confidence is earned, not assumed
8. One voice
9. Museum quality

---

## Chapter Tenets

### 01. Self-Contained, Cross-Referenced, No Assumptions

Every chapter works for a reader who has never seen another chapter. It introduces its own context, defines its own terms, tells its own complete prosecution. It links to related chapters where relevant but never requires them. A reader who arrives from a Google search, a social share, or a music journalist's article lands on solid ground immediately.

Cross-references are editorial and specific. Not "explore more chapters" but "The teacher-student gap measured who waited. The next chapter measures how long."

**Gate:** Rosetta verifies that all historical context required to understand the chapter is present. No assumed knowledge.

---

### 02. Shared Shell, Chapter-Specific Interior

Every chapter uses: the platform nav fragment, the design tokens, the asset register, the agent review process, and the "Have you heard" opening voice.

Inside that shell, structure follows content. The teacher-student gap chapter earned a network visualization because a network serves that content. The genre desertification chapter earned a stacked timeline because a timeline serves that content. Each chapter earns its own shape.

What never varies: the opening name hook, the platform nav, the methodology section, the citation block, the closing connective tissue.

**Gate:** Vera verifies design system compliance. Ida verifies structural coherence with the prosecution arc.

---

### 03. Data and Evidence, Both at Museum Standard

A chapter is not complete with data alone. A chapter is not complete with narrative alone. Every chapter contains both, and both are held to identical evidentiary standards.

The number needs a source. The story needs a source. "32-year induction gap" requires a citation. "Chuck Berry said it at the ceremony" requires the same citation. "Wenner told the New York Times..." requires a specific, documented source just as the hazard ratio does.

There is no hierarchy between quantitative and qualitative evidence. Both are evidence. Both are checked. Both ship only when sourced.

**Gate:** Rosetta verifies all narrative claims. Elias verifies all quantitative claims. Neither defers to the other.

---

### 04. Every Chapter Opens with a Name

The "Have you heard of [name]?" hook is mandatory. It is the first substantive thing a reader encounters after the platform nav. The name is a specific person -- not a concept, not a genre, not an era.

The chapter may be about a pattern, a system, a statistical model. It opens with a person. The person is not an anecdote. The person is the prosecution made human before the data makes it structural.

The opening name is chosen for: significance to the chapter's thesis, relative obscurity to a general audience, and the quality of their two-sentence story.

**Gate:** Ida verifies the hook lands in the "Have you heard" voice. Rosetta verifies the historical accuracy.

---

### 05. The Narrative Through Line is Structural, Not Decorative

The through line has two forms, both mandatory:

**The spine:** "By their own rules, who did they get wrong?" is the question every chapter answers from a different angle. This is not stated explicitly in every chapter. It is the question the chapter's existence answers.

**The connective tissue:** Every chapter closes with an explicit editorial hand-off to the next chapter in the prosecution arc. Not a generic link. A specific sentence that names what comes next and why it follows from what just came. Written in the "Have you heard" voice.

Example: *"Now you know what they said they would do. The next chapter is the first thing they did instead."*

The connective tissue is written by the project owner or reviewed and approved by the project owner before the chapter ships. It is editorial, not generated.

**Gate:** Ida verifies both forms are present and functional.

---

### 06. Uncertainty is Labeled at the Point of Claim

Not only in the methodology section. At the moment a model output, an estimated figure, or a disputed historical claim appears in the chapter body, it is labeled as such inline.

The language of uncertainty:
- "The model estimates..." for ML outputs
- "Documented in [source] as..." for verified historical claims
- "Estimated from incomplete records as..." for reconstructed figures
- "Reported in [source] as..." for claims from single secondary sources
- "Disputed -- the most widely cited figure is..." for contested data
- "AI-generated with human review..." for Claude API outputs

The reader never has to go to the methodology section to know whether a claim is verified or modeled. The uncertainty travels with the claim.

**Gate:** Elias verifies all quantitative uncertainty labeling. Rosetta verifies all historical uncertainty labeling.

---

### 07. The Methodology is Always Visible and Always Readable

Every chapter has a METHODOLOGY.md file and a method section accessible from the chapter's main navigation.

The methodology is written for a music researcher, not a developer. Target reader: a journalist at Billboard or a historian writing about the Hall who wants to understand exactly what was done, what assumptions were made, and where the uncertainty lives.

Required elements:
- Data sources used, with license and known limitations
- Analytical methods, described in plain language with technical detail available
- Model parameters and their rationale
- Confidence levels on all outputs
- Data gaps explicitly documented
- Validation approach
- Version date

**Gate:** Elias verifies technical accuracy. Rosetta verifies historical framing. Vera verifies design and readability. All three must approve.

---

### 08. One Original Finding, Minimum (Aspiration)

Every chapter aspires to contain at least one finding that does not exist anywhere else. A dataset nobody has assembled. An analysis nobody has run. A connection nobody has documented.

This is an aspiration, not a hard gate. But the ambition is always original contribution. When a chapter identifies its original finding, that finding is the "oh wow" moment.

The original finding is documented explicitly in the chapter spec before build begins.

---

### 09. The "Oh Wow" Moment is Required and Tested

Every chapter must contain at least one moment -- a visualization, a statistic, a connection -- that stops a reader cold. That makes them want to share it immediately.

**Testing protocol:**

All five agents review the chapter independently without being told what the "oh wow" moment is supposed to be. Each agent documents, unprompted, the single moment that hit hardest. If at least three of five agents independently identify the same moment, the test passes.

```
OH WOW ASSESSMENT:
The moment that hit hardest for me: [description]
Would I share this immediately: YES | NO
```

Gates tallies the responses and documents the result in the final verdict.

---

### 10. ML and AI are Maximized Throughout

Every chapter explores the full range of what ML and AI can contribute to the prosecution. The question is never "should we use ML here?" The question is "what is the most powerful use of ML we can responsibly make here?"

Responsible means: the output is labeled with its confidence level, the methodology is documented, and Rosetta has verified the historical grounding.

Required ML/AI consideration at spec time:
- **What can be modeled?** Criteria compliance, survival analysis, network centrality, genre diversity
- **What can be generated?** Artist briefs, verdict summaries, editorial conclusions
- **What can be measured?** Bias coefficients, hazard ratios, correlation after controls
- **What can be visualized with ML?** Influence networks, survival curves, regression overlays

The ML pipeline for each chapter is documented in the spec. Outputs are pre-computed and committed as static JS. No runtime ML inference.

**Gate:** Elias verifies methodology. Vera verifies visualization. Ida verifies that ML serves the prosecution.

---

### 11. The Design is Elegant and Authoritative

Elegant means: every visual element earns its place. Nothing decorative. Nothing that performs sophistication without delivering clarity. The design system in `docs/design.md` is the standard.

Authoritative means: this platform is making a serious argument about institutional failure. The design should feel like that. Not heavy-handed, not performative -- but serious. The prosecution exhibit framing (exhibit labels, crosshair ticks, monospace annotations) is the visual identity. It communicates: this is evidence.

**Gate:** Vera enforces elegance. Rosetta enforces accuracy.

---

### 12. Media Assets Verified Before Build Begins

Every media asset required by a chapter has a documented rights determination, entered in `data/asset-register.json` with Rosetta's approval, before a single line of chapter code is written.

The chapter spec includes an asset list. Rosetta reviews the asset list as part of spec approval. The build does not start with open rights questions.

**Gate:** Rosetta blocks any spec without a complete preliminary asset list. Vera blocks any build PR with an unregistered asset.

---

### 13. Mobile is First-Class

Every chapter reads and functions at 375px viewport width. The data is legible. The visualization is comprehensible. The prosecution's argument lands on mobile.

If a visualization genuinely cannot be made legible at 375px, a mobile-specific alternative view is designed. The alternative is not a downgrade -- it is a different expression of the same data optimized for the context.

**Gate:** Vera tests at 375px, 768px, and 1200px. Any failure at 375px is a block.

---

### 14. The Chapter is Citable

When a chapter ships, it ships with sufficient documentation for a journalist, historian, or music researcher to cite it.

Required citation elements on every chapter:

```
Cite this chapter:
Haynes, Jeremy. "[Chapter Title]." One Long Impersonation,
onelongimpersonation.report/chapters/[slug]/, [Month Year].
Accessed [access date].

For academic citation (Chicago):
Haynes, Jeremy. "[Chapter Title]." One Long Impersonation. [Month Year].
https://onelongimpersonation.report/chapters/[slug]/.

Data citation (CC0):
One Long Impersonation. "[Chapter Title] Dataset." CC0 1.0.
https://github.com/onelongimpersonation/chapters/[slug]/data/.
[Version date].
```

**Gate:** Gates verifies the citation block is present and complete.

---

### 15. The Build Sequence Has Three Hard Gates

Every chapter moves through three phases. No exceptions.

**Gate 1 -- Spec Approved**
The chapter spec is written, reviewed by all five agents, and approved. Gates issues a SPEC APPROVED verdict before build begins.

**Gate 2 -- Build Complete**
The chapter is fully built. All content sourced. All visualizations complete. All ML outputs pre-computed. All assets registered. Agent reviews in progress.

**Gate 3 -- All Five Agents Sign Off**
Rosetta, Elias, Vera, Ida, and Gates all issue APPROVED. The "oh wow" test passes. Gates issues MERGE. The chapter ships.

---

## Summary Table

| Tenet | Hard Gate | Agent Owner | Blocks Spec | Blocks Ship |
|-------|-----------|-------------|-------------|-------------|
| 01 Self-contained | Yes | Rosetta | No | Yes |
| 02 Shared shell, own interior | Yes | Vera + Ida | Yes | Yes |
| 03 Data and evidence both | Yes | Rosetta + Elias | Yes | Yes |
| 04 Opens with a name | Yes | Ida + Rosetta | Yes | Yes |
| 05 Narrative through line | Yes | Ida | Yes | Yes |
| 06 Uncertainty inline | Yes | Elias + Rosetta | Yes | Yes |
| 07 Methodology visible | Yes | All | No | Yes |
| 08 Original finding | Aspiration | Ida | Yes (spec) | No |
| 09 "Oh wow" moment | Yes | All five | Yes (spec) | Yes |
| 10 ML maximized | Yes | Elias + Ida | Yes (spec) | Yes |
| 11 Elegant and authoritative | Yes | Vera + Rosetta | No | Yes |
| 12 Assets before build | Yes | Rosetta | Yes | Yes |
| 13 Mobile first-class | Yes | Vera | No | Yes |
| 14 Chapter is citable | Yes | Gates | No | Yes |
| 15 Three-gate build sequence | Yes | Ida + Gates | Structure | Structure |

---

*Chuck Berry said it in 1986. The Hall took thirty-two more years to hear him.*
*The data is the prosecutor. The reader is the jury. This platform is the courtroom.*
