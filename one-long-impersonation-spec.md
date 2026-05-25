# One Long Impersonation
## Platform Specification v1.0

**Domain:** onelongimpersonation.report · onelongimpersonation.com
**Mission:** A data-driven prosecution of the Rock and Roll Hall of Fame using their own stated criteria as the instrument of indictment.
**Standard:** Museum quality. Legally defensible. Citable by journalists, historians, and music researchers.
**License:** MIT (code) · CC0 (data)
**Owner:** Jeremy Haynes
**Status:** SPEC COMPLETE
**Last updated:** May 2026

---

## The Name

In 1986, at the very first Rock and Roll Hall of Fame induction ceremony, Chuck Berry accepted his honor and said:

*"My whole career has been one long Sister Rosetta Tharpe impersonation."*

Sister Rosetta Tharpe was not inducted until 2018. Thirty-two years later.

The man they inducted said out loud, at the ceremony, that the woman who taught him everything was not there. And they did not induct her for three more decades.

Every artist in the Hall is, in some sense, an impersonation of someone the Hall did not bother to recognize. The pioneers taught the stars. The Hall inducted the stars and forgot the pioneers.

One long impersonation.

---

## The Opening Statement

*"My whole career has been one long Sister Rosetta Tharpe impersonation."*
-- Chuck Berry, Rock and Roll Hall of Fame induction ceremony, 1986

The Rock and Roll Hall of Fame has published its criteria since its founding in 1983. Artists become eligible 25 years after their first commercial recording. They are judged on: musical excellence, influence on other performers, length of career, depth of catalog, and contributions to rock and roll.

That is their standard. Not ours. Theirs.

This platform holds them to it.

Everything on this platform is derived from documented evidence. Every finding is sourced. Every verdict is rendered by the data. Named decision-makers are identified where documented voting records, public statements, and institutional decisions create a paper trail. The data is the prosecutor. The Hall's own criteria is the law. The reader is the jury.

The question: by their own rules, who did they get wrong?

The answer, revealed chapter by chapter, is this: they got it wrong systematically, in the same direction, across four decades, against the same kinds of artists.

The pattern has a name. This platform documents it.

---

## The Three Axes of Prosecution

**Axis One -- The Pioneers.**
Black artists, women, and genre inventors who created the music the Hall celebrates and were not inducted, or were inducted decades after their students were already enshrined. The teacher-student gap. The racial and gender dimension.

**Axis Two -- The Genres.**
Entire musical traditions with massive cultural footprints that the Hall systematically excluded or tokenized. Heavy metal waited 23 years for its first inductee. The model shows what the criteria-based score says about those artists vs. what actually happened.

**Axis Three -- The Voters.**
The nominating committee and the voting body, documented. Who they are. How long they served. What their documented aesthetic preferences show. The Rolling Stone connection. The concentration of decision-making power in a small, unrepresentative group. Named. Documented. Not speculated.

All three axes converge on the same institutional failure. This platform makes that convergence visible.

---

## The Through Line Question

**Who taught them?**

Every chapter answers it from a different direction. Who taught Chuck Berry. Who taught Led Zeppelin. Who taught Metallica. Who taught everyone the Hall celebrates -- and what the Hall did with those teachers.

---

## The Voice

The "Have you heard" register, sharpened. Less grief than The Other Box Score, more precision. The friend who did the research and built the case and is not going to let you leave without knowing what they found.

The tone is documented outrage. Not polemic. Not personal. The data is the prosecutor. The platform is the courtroom. The voice presents evidence. The reader delivers the verdict.

---

## Platform Architecture

### The Book Structure

**OPENING ARGUMENT**
The criteria. The institution. The founding. The named decision-makers. The through line question established before the evidence begins.

**PART ONE -- THE TEACHERS**
Who they were. What they built. What the Hall did with them. The racial and gender dimension made structural.

**PART TWO -- THE GENRES**
The systematic exclusion of entire musical traditions. Heavy metal. Punk underground. Electronic pioneers. The genre desertification documented year by year.

**PART THREE -- THE MACHINE**
How decisions were actually made. The nominating committee. The Rolling Stone connection. The institutional capture argument, named and documented.

**PART FOUR -- THE VERDICT**
The AI-generated docket. Every eligible artist who has not been inducted. The criteria applied. The verdict rendered. Updated annually before the nomination cycle.

**CLOSING ARGUMENT**
What the data shows in aggregate. What the Hall could do. What it has not done. The record, stated plainly.

---

## The Chapters

---

### Chapter 01: The Criteria
*Before the prosecution begins, the jury must know the law.*

**Have you heard what the Rock and Roll Hall of Fame says it does?**

The Hall has published its induction criteria publicly since 1983. Five factors: musical excellence, influence on other performers, length of career, depth of catalog, contributions to rock and roll. This chapter documents those criteria in full -- every public statement, every press release, every FAQ entry, every interview in which Hall leadership described the selection process.

Then it builds the Criteria Compliance Model: a transparent, documented scoring system that operationalizes each criterion using measurable proxies.

**The criteria operationalized:**

| Criterion | Proxy measures |
|-----------|---------------|
| Musical excellence | Critical reception score (aggregated from Pitchfork, AllMusic, Rolling Stone historical reviews), Grammy nominations, industry peer citations |
| Influence on other performers | Documented influence citations from MusicBrainz artist relationships, liner note citations, documented interview statements |
| Length of career | Years active from first commercial recording to last |
| Depth of catalog | Studio album count, total recorded output, catalog longevity score |
| Contributions to rock and roll | Genre origin attribution score, first-mover classification, influence network centrality |

**The original finding:** Every inducted artist and every eligible non-inducted artist receives a Criteria Compliance Score. The distribution of scores among inducted vs. non-inducted artists is the first exhibit in the prosecution. The gap between what the criteria predict and what actually happened is the Criteria Violation Index.

**Data sources:** Rock Hall official publications, MusicBrainz open database, Discogs release data, AllMusic editorial ratings, archived Rolling Stone reviews, RIAA certification data, Billboard historical chart data.

**ML component:** The Criteria Compliance Model is trained on Hall-published criteria documentation and scored against the full eligible artist population. Output: ranked violation list. Top of the list: the prosecution's opening witnesses.

**Oh wow moment:** The Criteria Violation Index leaderboard. The moment the reader sees who sits at the top -- artists who score highest on the Hall's own criteria and have never been inducted -- and recognizes the names. The gap between criteria score and induction status is not random noise. It has a direction.

**Connective tissue out:** *"Now you know what they said they would do. The next chapter is the first thing they did instead."*

---

### Chapter 02: One Long Impersonation
*The teacher-student gap. The founding exhibit.*

**Have you heard of Sister Rosetta Tharpe?**

She invented the electric guitar style that Chuck Berry built his career on. Chuck Berry was inducted in 1986 -- the first ceremony. Tharpe was inducted in 2018. Thirty-two years.

This chapter builds the Teacher-Student Gap dataset -- the most original finding on the platform. For every inducted artist, we construct a documented influence graph using: documented interview statements, liner note citations, MusicBrainz artist relationship data, and published biographical sources. We identify every documented teacher-student pair where the teacher is an eligible artist.

Then we measure the gap.

**The Teacher-Student Gap metric:**
For each documented teacher-student pair: induction year of student minus induction year of teacher (or current year if teacher never inducted). Positive values mean the teacher waited longer than the student. Negative values mean the teacher was inducted first. The distribution of this metric across all documented pairs is the chapter's central visualization.

**The racial breakdown:**
Of all teacher-student pairs where the teacher is Black and the student is white, what is the median gap? What is it for same-race pairs? For pairs where both are white? The racial breakdown of the Teacher-Student Gap is the prosecution's central exhibit. It is not asserted. It is calculated.

**The specific cases:**
The chapter profiles the ten most egregious documented gaps in detail. Each profile contains: the teacher, the student, the documented statements establishing the influence relationship, the induction dates, the gap in years, and what the teacher was doing during the years the student was being celebrated.

**Key documented cases:**
- Sister Rosetta Tharpe (teacher) / Chuck Berry (student): 32-year gap. Berry said it himself at the ceremony.
- Big Mama Thornton (teacher, never inducted) / Elvis Presley (student, inducted 1986): Thornton wrote and recorded Hound Dog three years before Presley. She was never inducted. Presley was in the first class.
- Louis Jordan (teacher, inducted 2024 Early Influence) / Chuck Berry, Little Richard, Ray Charles (students, inducted 1986-1987): Jordan's jump blues template is documented as the direct precursor to rock and roll by every historian who has written about the period. The students were in the first two classes. Jordan waited 38 years.
- The Ink Spots (teacher, never inducted) / vocal harmony tradition spanning the entire inducted roster: their influence on doo-wop, which influenced every rock and roll vocal style, is documented throughout the musicological literature. Never nominated.
- Charley Patton, Son House, Robert Johnson (teachers, Early Influence 1986-1992) / Led Zeppelin (student, inducted 1995): the gap here is not in induction timing but in compensation -- Zeppelin lifted compositions wholesale and the Hall celebrated them while never addressing the appropriation. This case is handled carefully and only the documented facts are stated.

**ML component:** A network centrality model over the full documented influence graph. The teachers who sit at the highest-centrality nodes in the network and are not inducted, or were inducted late, are identified and ranked. The racial breakdown of high-centrality non-inducted nodes is calculated with full uncertainty documentation.

**Oh wow moment:** The visualization of the Teacher-Student Gap distribution, colored by the racial composition of each pair. The skew is visible. The direction is unmistakable. No annotation required.

---

### Chapter 03: The Wait
*Time is not neutral. Who waited longest, and why.*

**Have you heard how long Judas Priest waited?**

Judas Priest became eligible in 1999. They were inducted in 2022. Twenty-three years. During that time, the Hall inducted multiple artists with lower criteria compliance scores, shorter careers, and smaller catalogs.

This chapter builds the full Wait Time dataset for every inducted artist: years from first eligibility to first nomination, years from first nomination to induction, and total wait from eligibility to induction. Then it breaks that data down across three dimensions simultaneously: race, gender, and genre.

**The three-way breakdown:**
- Black artists vs. white artists: median wait time from eligibility to induction
- Female artists vs. male artists: same metric
- Metal/hard rock vs. classic rock vs. pop: same metric

Each breakdown is controlled for era (when did they become eligible?), commercial success (certified sales), and influence score (from the Criteria Compliance Model). The disparity that remains after controls is the unexplained gap -- the documented bias.

**The Axios baseline:**
Axios found in 2023 that the median first nomination time for female nominees was eight years versus two years for male nominees, and 46% of male artists are inducted on their first nomination versus 37% of female artists. This chapter extends that finding: we add race as a dimension, add genre as a dimension, and add controls for commercial success and influence score that Axios did not apply. What remains after controls is stronger evidence than what Axios found.

**The genre dimension:**
Heavy metal specifically: Black Sabbath eligible 1994, inducted 2006 (12-year wait). Judas Priest eligible 1999, inducted 2022 (23-year wait). Motörhead eligible 2001, never inducted (Lemmy died in 2015, inducted posthumously in Musical Excellence 2020 -- 19 years). Iron Maiden eligible 2005, inducted 2026 (21-year wait). The metal wait time distribution vs. classic rock wait time distribution is visualized as overlapping density curves. The gap is not subtle.

**ML component:** A survival analysis model (Cox proportional hazards) predicting time to induction as a function of criteria compliance score, race, gender, genre, and era. The hazard ratios on race and genre after controlling for criteria score are the documented bias coefficients.

**Oh wow moment:** The survival curves, stratified by race and genre simultaneously. The moment the reader sees that a high-criteria-score Black artist has the same predicted wait time as a medium-criteria-score white artist. The model makes the disparity quantitative and the disparity is large.

---

### Chapter 04: The Genre Desertification
*What the Hall decided rock and roll was -- and what it actually was.*

**Have you heard that the first heavy metal band wasn't inducted until 2006?**

The Rock and Roll Hall of Fame opened in 1986. Black Sabbath -- the band that invented heavy metal, whose influence on the genre is as documented and direct as any influence relationship in rock history -- was not inducted until 2006. Twenty years. During those twenty years, the Hall inducted dozens of artists in genres it deemed acceptable.

This chapter builds the Genre Representation Timeline: a visualization of every induction from 1986 to 2026, organized by genre, showing how genre representation shifted as the nominating committee changed.

**The genre taxonomy:**
We build a documented genre classification for every eligible artist using MusicBrainz genre tags, Discogs style classifications, and AllMusic genre designations. Each artist receives a primary genre and up to three secondary genres. The classification is documented and reproducible.

**The genre desertification finding:**
The chapter measures genre diversity among inductees by year using Simpson's Diversity Index -- the same metric ecologists use to measure species diversity in an ecosystem. The chart shows how genre diversity changed over the Hall's history. The Wenner era (1986-2019) is compared against the post-Wenner era (2020-present). The pattern is documented.

**The metal case in detail:**
A dedicated section on heavy metal specifically. The documented influence of metal on subsequent popular music. The certified sales figures for non-inducted metal artists. The fan vote data showing consistent high support for metal acts that the nominating committee overrode. The gap between fan preference and committee selection as a documented institutional disconnect.

**Key metal cases:**
- Motörhead: First eligible 2001. Never inducted as performers. Inducted in Musical Excellence 2020 -- a category used when acts can't get enough votes in the main ballot. Lemmy did not live to see it.
- Thin Lizzy: Eligible 1996. Never nominated. Phil Lynott died in 1986 -- never saw eligibility.
- Soundgarden: Eligible 2016. Multiple nominations. Never inducted. Chris Cornell died in 2017.
- Rage Against the Machine: Eligible 2017. Inducted 2023 -- 6-year wait for a band whose political impact alone meets the criteria.
- System of a Down: Eligible 2023. Not yet inducted.
- Tool: Eligible 2018. Not yet inducted despite consistently topping fan votes.

**The documented explanation:**
Jann Wenner admitted in a 2022 podcast interview that Foreigner, Boston, Styx, and "that whole era" had simply "never come up" in nominating committee discussions. He was on that committee from 1986 to 2006. The documented explanation for why entire genres were invisible to the committee is that the committee's composition determined what came up for consideration. The composition is documented. The connection is drawn.

**ML component:** A genre diversity model that predicts expected genre representation based on eligible artist population vs. actual inducted genre representation. The deviation from expected is the Genre Bias Score by era and by genre. The model identifies which genres were systematically under-inducted relative to their eligible population.

**Oh wow moment:** The Genre Desertification timeline animated. Watching the color coding of inductees by genre across 40 years -- the narrow band of classic rock dominating decade after decade while the eligible population diversifies dramatically. The visual argument for institutional capture made in thirty seconds.

---

### Chapter 05: The Rolling Stone Connection
*The Wenner Coefficient. How one publication's taste became an institution's selection criteria.*

**Have you heard who built the Rock and Roll Hall of Fame?**

Ahmet Ertegun, co-founder of Atlantic Records, convened the founding group in 1983. Among them: Jann Wenner, founder and publisher of Rolling Stone magazine. Wenner served on the nominating committee from 1986 to 2006 and as Chairman from 2006 to 2019. The committee was, in the words of a disillusioned member quoted in Billboard in 2015, "stacked with current and former Rolling Stone writers and editors."

In September 2023, Wenner was removed from the Hall's board of directors after telling the New York Times that Black and women artists didn't meet his "historical standard" -- the standard he had been applying for thirty-seven years.

This chapter documents the institutional capture argument quantitatively.

**The Wenner Coefficient:**
Using the complete archive of Rolling Stone's artist reviews, cover appearances, and critical rankings from 1967 to 2019, we build a Rolling Stone Attention Score for every eligible artist: a weighted composite of review coverage, cover appearances, and inclusion in major Rolling Stone lists (500 Greatest Albums, 100 Greatest Artists, etc.).

We then measure the correlation between Rolling Stone Attention Score and Hall induction probability, controlling for criteria compliance score, era, and commercial success. The partial correlation that remains after controls is the Wenner Coefficient -- the documented influence of Rolling Stone aesthetic preferences on Hall induction decisions, net of legitimate artistic merit measures.

**The finding we expect:**
Rolling Stone's historical aesthetic preferences are documented: the magazine consistently prioritized certain strands of white rock -- Dylan, Springsteen, the British Invasion, classic rock -- over heavy metal, Black music that didn't fit its crossover narrative, and women except those who fit the singer-songwriter mold. If the Wenner Coefficient is positive and significant after controls, it documents that those preferences shaped Hall inductions.

**The named decision-makers:**
This chapter documents the nominating committee composition for every year it has been publicly disclosed. Named members, their publications and institutional affiliations, their documented aesthetic preferences based on public writing. The Rolling Stone writers and editors on the committee are identified by name, with their documented Rolling Stone coverage of eligible artists cross-referenced against their committee membership years.

This section is legally reviewed before publication. Every named individual is documented from public sources. No motives are imputed. Documented facts are stated. The reader draws conclusions.

**The before and after:**
Wenner resigned as Chairman in 2019. John Sykes took over. A measurable shift in induction patterns followed: more women, more hip-hop, more artists outside classic rock, more diverse genres. The chapter documents this shift quantitatively using the same Genre Bias Score from Chapter 04. The before/after comparison around 2019 is the natural experiment. The data determines whether the change was real and how large it was.

**ML component:** The Wenner Coefficient model. Logistic regression predicting induction probability from criteria compliance score, Rolling Stone Attention Score, era fixed effects, genre, and race/gender indicators. The coefficient on Rolling Stone Attention Score after controlling for everything else is the documented institutional capture estimate.

**Oh wow moment:** The scatter plot of Rolling Stone Attention Score vs. Induction Probability, with the regression line showing a steeper slope than the Criteria Compliance Score vs. Induction Probability plot. The visual demonstration that how much Rolling Stone covered you predicted your induction better than how well you met the stated criteria.

---

### Chapter 06: The Docket
*Every eligible artist who has not been inducted. The criteria applied. The verdict rendered.*

**Have you heard the case for [artist name]?**

This chapter is a living document. It is updated annually before the nomination cycle. It contains an AI-generated legal brief for every eligible artist who has not been inducted, structured as follows:

- **Findings of fact:** documented career summary, chart performance, certified sales, genre classification, documented influence citations
- **Application of criteria:** the five Hall criteria applied to the documented facts, with the Criteria Compliance Score shown
- **The gap:** the difference between the artist's Criteria Compliance Score and the average Criteria Compliance Score of inducted artists in their era
- **The verdict:** STRONG CASE FOR INDUCTION / CASE FOR INDUCTION / BORDERLINE / INSUFFICIENT EVIDENCE -- with confidence level
- **The teacher-student context:** documented influence relationships connecting this artist to inducted artists

Every verdict is labeled as AI-generated. Every factual claim is sourced. Every conclusion carries a confidence level. The methodology is fully documented and reproducible.

**The AI generation methodology:**
Model: Claude API (claude-sonnet-4-20250514). Each brief is generated from a structured prompt containing the artist's documented data record. The prompt instructs the model to apply the Hall's stated criteria exactly and to cite only documented facts. All generated briefs are reviewed by a human editor before publication -- factual errors are corrected, unsourced claims are removed. The review process is documented.

**The annual publication cycle:**
The Docket is published in January, before the Hall announces its annual nominations. It is updated after nominations are announced to show which cases the Hall addressed and which it continued to ignore. The comparison between the Docket's recommendations and the Hall's actual decisions is published as an annual report card.

**The searchable interface:**
The Docket is a searchable, filterable database. Filter by genre, era, Criteria Compliance Score, teacher-student status, wait time. Sort by any column. Each artist's brief is one click away. The full dataset is downloadable as CC0.

**The viral mechanic:**
Each artist's brief is shareable as a standalone page with its own URL. Format: `onelongimpersonation.report/docket/[artist-slug]`. Each page includes the share mechanic: "Share this case" with pre-formatted social text. Released annually in January when music press is covering the nominations -- maximum relevance, maximum reach.

**Oh wow moment:** The top of the Docket. The first time the reader sees the ranked list of STRONG CASE FOR INDUCTION artists who have never been inducted, and recognizes every single name on it.

---

### Chapter 07: The Other Side
*What the Hall has gotten right. The cases that were correct. The trend since 2019.*

This chapter exists because the prosecution is honest.

The Hall has inducted thousands of artists and gotten thousands of those decisions right. The chapter documents the decisions that were correct by the criteria -- artists who were inducted promptly, whose criteria compliance scores match their induction timing, whose teacher-student relationships were honored.

It also documents the measurable improvement since 2019 under John Sykes. The data shows the shift is real. The chapter acknowledges it and measures its size. Partial credit where partial credit is due.

This is not softening the prosecution. It is strengthening it. A prosecution that acknowledges what the defendant got right is more credible than one that does not. And the documented improvement since 2019 sharpens rather than blunts the case against the Wenner era -- because it shows that different decisions were possible all along. The Hall was not constrained by the criteria to produce the outcomes it produced. It chose them.

---

### Closing Argument

*The record, stated plainly.*

Four data findings, stated without annotation:

1. The average teacher-student gap for Black teacher / white student pairs is [X] years. For same-race pairs it is [Y] years. The difference after controlling for commercial success and era is [Z] years. That difference is the documented cost of the pattern.

2. The correlation between Rolling Stone Attention Score and Hall induction probability, after controlling for criteria compliance score, is [r]. The same correlation for criteria compliance score alone is [s]. If r > s, the data shows that Rolling Stone coverage predicted induction better than the stated criteria did.

3. The top ten artists by Criteria Compliance Score who have never been inducted are: [list]. Their average wait time is [X] years. The average wait time for inducted artists with equivalent Criteria Compliance Scores is [Y] years. The gap is [Z] years.

4. Since 2019, the Genre Bias Score for heavy metal has moved from [X] to [Y]. For Black artists it has moved from [A] to [B]. The trend is real. The change required a change in who was making decisions.

The data does not tell the Hall what to do. The data tells you what the Hall did.

*Chuck Berry said it in 1986. It took thirty-two more years.*

---

## Data Sources

| Source | Coverage | License | Notes |
|--------|----------|---------|-------|
| Rock Hall official inductee database | 1986-present | Public | Complete induction history |
| MusicBrainz database | Full music catalog | CC0 | Artist relationships, release data, influence citations |
| Discogs database | Full music catalog | CC0 subset | Genre, release, format data |
| Billboard historical charts | 1958-present | Academic access | Chart performance data |
| RIAA certification database | 1958-present | Public | Certified sales data |
| AllMusic editorial ratings | Full catalog | Scraping/API | Critical reception scores |
| Rolling Stone archive | 1967-present | Research use | Cover appearances, review scores, list inclusions |
| Axios gender analysis dataset | 2023 | Published research | Baseline gender nomination/induction data |
| Jann Wenner documented statements | 1986-2023 | Public record | Podcast interviews, NY Times interview, Billboard interview |
| Nominating committee composition | Published years | Public record | Last fully disclosed: 2015 |
| Future Rock Legends nomination database | 1986-present | Public | Complete nomination history including non-inducted |

---

## ML and AI Components Summary

| Model | Type | Purpose | Output |
|-------|------|---------|--------|
| Criteria Compliance Model | Weighted scoring | Operationalize Hall criteria | Score for every eligible artist |
| Teacher-Student Gap Model | Network analysis + statistics | Measure and decompose influence gaps | Gap distribution with racial breakdown |
| Wait Time Survival Model | Cox proportional hazards | Predict induction timing | Hazard ratios for race, gender, genre |
| Genre Diversity Model | Diversity index + deviation analysis | Measure genre representation gaps | Genre Bias Score by era |
| Wenner Coefficient Model | Logistic regression | Quantify Rolling Stone influence | Partial correlation after controls |
| AI Verdict Engine | Claude API + human review | Generate artist briefs | Structured legal briefs with confidence labels |

---

## The Agent Team

Same five agents as The Other Box Score with music-specific mandates:

**Oscar (music version -- working name: Rosetta)**
Historical accuracy authority for music history claims. Named for Sister Rosetta Tharpe. Same mandate as Oscar on TOBS: every factual claim about an artist, their career, their influence relationships, or the Hall's decisions must be sourced. Named decision-maker claims must come from documented public sources only. No imputed motives.

**Elias** -- statistical methodology, unchanged from TOBS

**Vera** -- visualization and assets, unchanged from TOBS

**Ida** -- project coherence and tenet enforcement, unchanged from TOBS

**Gates** -- final QA, unchanged from TOBS

---

## The Legal Standard

This platform holds itself to the standard of responsible investigative journalism. Every claim about a named individual is:
- Sourced to a documented public statement, public record, or published reporting
- Stated as documented fact, not as imputed motive
- Subject to correction if demonstrated to be inaccurate

The Wenner Coefficient is a statistical model. It documents correlation, not causation. The chapter that presents it says so explicitly. The documented statements Wenner made are quoted accurately with full context. The institutional structure he built is documented from public sources.

This platform does not assert that any individual acted with discriminatory intent. It documents what the data shows about outcomes and what the public record shows about the decisions that produced those outcomes. The reader draws conclusions.

---

## Relationship to The Other Box Score

Sibling project. Same mission, different institution. Same data journalism standard. Same agent team. Same commitment to CC0 data and open source code.

Cross-link: The Other Box Score's Chapter 06 (The Collapse) documents how integration killed the Negro Leagues by extracting their talent without compensation. One Long Impersonation documents how the Rock and Roll Hall of Fame honored the extraction's beneficiaries while forgetting the source.

The two platforms are complementary arguments. Different subjects, same pattern.

---

## Build Sequence

**Phase 1 -- Foundation (months 1-2)**
- Build the complete eligible artist database from Rock Hall public records and Future Rock Legends nomination history
- Download and process MusicBrainz database for artist relationships
- Build Criteria Compliance Model v1
- Build Teacher-Student Gap dataset from documented influence citations
- Agent review: Rosetta verifies all influence citations from primary sources

**Phase 2 -- The Core Cases (months 3-4)**
- Chapter 01 (The Criteria) and Chapter 02 (One Long Impersonation) built and agent-reviewed
- Teacher-Student Gap visualization built and oh wow tested
- Criteria Violation Index leaderboard built and published as preview

**Phase 3 -- The Statistical Arguments (months 5-6)**
- Chapter 03 (The Wait) survival analysis built
- Chapter 04 (Genre Desertification) built
- Chapter 05 (The Rolling Stone Connection) built -- legal review before publication

**Phase 4 -- The Docket (month 7)**
- AI Verdict Engine built and calibrated
- First full Docket published -- timed to January nomination cycle
- Annual update process established

**Phase 5 -- Completion (month 8)**
- Chapter 07 (The Other Side) built
- Closing Argument written
- Full agent review on all chapters
- Platform launch

---

## The Tagline

*Chuck Berry said it in 1986. The Hall took thirty-two more years to hear him.*

---

## The Last Line

*They built a hall of fame for the music. They forgot who built the music.*
