@@TITLE Analysis Protocol, Codebook and Estimation Specification

*Companion to "From vision to measurable practice: circular accounting capability, chain transparency and the governance conditions of net-zero value creation in fragmented manufacturing networks"*

# 0. Status note and what I need from you

Now that data exist, the submission moves to **option (a)** in the editorial assessment: a conventional empirical *IJPR* submission with an unusually strong measurement pedigree. This is the strongest available position. Section 12 of this document lists exactly what changes in the manuscript.

**One important caveat about the items.** The manuscript refers to the full instrument as "Table VI" (original) / "Appendix A" (revision), but **that table is not present in the file you supplied.** Only one item is quoted anywhere in the document: *"we write down how much fruit we reject or lose"* (a CAC item). Everything in Section 2 below is therefore a **reconstruction** built to satisfy every constraint the manuscript states — 46 items; 9/5/6/6/11 focal allocation; the three CAC and three CVCP dimensions; the 22/11/10/3 source split; the specific item labels named in the text (CAC2, CGQ1, CGQ6, CVCI2, CIT3, IS1, IS2, IS3, MK1, MK3); current-state predictors and change-framed outcomes.

**You must reconcile it against the instrument you actually fielded.** Where they differ, your fielded version governs and this document's item IDs should be remapped. The codebook structure, model specification, protocol and code in Sections 3 to 11 are independent of the exact wordings and apply as-is.

## What I need from you to finalise this

1. **Achieved *n*** and the realised composition by stratum against the Table 5 targets. Several protocol steps branch on *n*.
2. **Your actual item list**, so the codebook can be remapped rather than reconstructed.
3. Whether all 46 items were fielded, or whether MK1 / IS2 / IS3 were dropped or revised first.
4. Whether the **fourth expert round** on the weak CAC items happened before fielding.
5. Whether the **objective-indicator subsample** (loss ratio, by-product value, realised vs modal price) was collected, and for how many cases.
6. **Software**: SmartPLS 4, R, or both. Section 9 is a SmartPLS click-path; Section 10 is a complete R script.
7. Whether ethics approval and informed consent are documented — *IJPR* will require a statement.

# 1. Construct system at a glance

@@TABLE Table A1. Construct inventory
Construct | Code | Specification | Mode | Dimensions | Items | Role in model
Circular Accounting Capability | CAC | Reflective-formative higher-order (Type II) | LOCs Mode A → HOC Mode B | 3 | 9 | Exogenous antecedent
Circular Information Transparency | CIT | Reflective (composite) | Mode A | – | 5 | Mediator 1
Circular Governance Quality | CGQ | Reflective (composite) | Mode A | – | 6 | Moderator + direct predictor
Circular Value-Chain Integration | CVCI | Reflective (composite) | Mode A | – | 6 | Mediator 2 (focal endogenous)
Circular Value Creation Performance | CVCP | Reflective-formative higher-order (Type II) | LOCs Mode A → HOC Mode B | 3 | 11 | Final outcome
Digital Traceability Capability | DTC | Reflective (composite) | Mode A | – | 3 | Control (rival explanation)
Institutional Support | IS | Reflective (composite) | Mode A | – | 3 | Control (rival explanation)
Marker (attitude toward the colour blue) | MK | Reflective (composite) | Mode A | – | 3 | Method-bias marker; excluded from structural model
**Focal subtotal** | | | | | **37** |
**Whole instrument** | | | | | **46** |
@@ENDTABLE

*Note.* 46 = 37 focal + 3 DTC + 3 IS + 3 MK. Source split: 22 adapted from validated scales (AV); 11 adapting validated item structures to circular resource-flow content (AS); 10 newly developed (ND); 3 marker administered verbatim (MK). This reproduces the split stated in Section 5.5 of the manuscript.

# 2. The instrument

**Response format.** All substantive items on seven-point scales, enumerator-administered with a visual ladder card.

**Predictor stem (CAC, CIT, CGQ, CVCI, DTC, IS) — current state.** *"Thinking about how your enterprise operates now, please indicate how far each statement describes what actually happens."* 1 = not at all, 4 = to a moderate extent, 7 = to a very great extent.

**Outcome stem (CVCP) — change over three seasons.** *"Compared with three seasons ago, how has each of the following changed for your enterprise?"* 1 = decreased greatly, 4 = no change, 7 = increased greatly. All CVCP items are worded so that **higher = better**; the loss items are phrased as *reduction in*, so no reverse-coding is required. Verify this against your fielded wording before analysis — if any item was worded as *"quantity of waste"* rather than *"reduction in waste"*, reverse-code it and record that you did.

## 2.1 Circular Accounting Capability (CAC) — 9 items, 3 dimensions

@@TABLE Table A2. CAC items
ID | Dimension | Item | Source class
CAC1 | Material and resource-flow measurement | We keep a written or electronic record of the quantity of raw material we take in each season. | AS
CAC2 | Material and resource-flow measurement | We write down how much of what we handle is rejected, downgraded or lost. | AS
CAC3 | Material and resource-flow measurement | We record what happens to the material that does not become saleable product — where it goes and who takes it. | AS
CAC4 | Loss and waste costing | We work out what the material we lose or reject cost us to buy or to produce. | AS
CAC5 | Loss and waste costing | We know what the rejected or lost material would have earned had it been sold as product. | AS
CAC6 | Loss and waste costing | We keep the cost of losses separate from our general operating costs rather than absorbing it into overall cost. | ND
CAC7 | Recovery and circular investment evaluation | Before deciding whether to recover a by-product or residue, we estimate what it could earn. | ND
CAC8 | Recovery and circular investment evaluation | We compare the cost of recovering a residue against the cost of disposing of it. | ND
CAC9 | Recovery and circular investment evaluation | When we consider equipment or capacity for processing residues, we work out whether the investment would pay back. | ND
@@ENDTABLE

*Note.* CAC2 is the item quoted in the manuscript. CAC2 was among the twelve reworded in round 3. The recovery-valuation dimension (CAC7–CAC9) is wholly new because no validated instrument exists for it, and it is the dimension on which expert disagreement concentrated — which is why CAC is the weakest focal scale at 0.889. Expect this dimension to be the most likely source of a low outer weight or loading, and read Section 6 step 3 before deleting anything from it.

## 2.2 Circular Information Transparency (CIT) — 5 items

@@TABLE Table A3. CIT items
ID | Item | Source class
CIT1 | Partners we deal with can see how much material is rejected or lost at our stage. | AV
CIT2 | We can see how much material is rejected or lost at the stages before and after us. | AV
CIT3 | Information about recoverable residues and by-products reaches the people who could use them, in time for them to act. | AV
CIT4 | Information about material flows and losses in this chain is accurate and reliable enough to base a decision on. | AS
CIT5 | We can see how the money paid for the final product is divided among the actors in this chain. | ND
@@ENDTABLE

*Note.* CIT1–CIT3 adapted from the supply chain visibility measure of Williams et al. (2013); CIT4 adapts the information-quality structure of Li et al. (2005). CIT5 (value-distribution transparency) is new — no validated instrument exists. CIT3 was reworded in round 3 and reached 0.975. **CIT5 is the item most likely to behave differently from the other four**, because it concerns price information rather than material information; check its loading carefully and see Section 6 step 3 for the escalation rule.

## 2.3 Circular Governance Quality (CGQ) — 6 items

@@TABLE Table A4. CGQ items
ID | Governance element | Item | Source class
CGQ1 | Responsibility allocation | It is clear which party is answerable when material is lost or spoiled between us and our partners. | ND
CGQ2 | Joint monitoring and verification | Our partners and we jointly check the quantities and quality recorded when material changes hands. | AV
CGQ3 | Codified standards | What counts as an acceptable level of loss is agreed and recorded with our partners. | AS
CGQ4 | Participatory decision-making | We are able to take part in decisions that affect how material and losses are handled in this chain. | AV
CGQ5 | Participatory decision-making | Our views are taken into account when the terms of trade in this chain are set. | AV
CGQ6 | Enforceable commitment | Commitments our partners make about handling, collection or payment are honoured, and there are consequences if they are not. | AV
@@ENDTABLE

*Note.* CGQ2 adapted from the verification logic of Gualandris et al. (2015); CGQ4–CGQ5 adapted from the validated cooperative-governance participation measure of Österberg and Nilsson (2009). CGQ1 (responsibility for losses) is new. CGQ1 and CGQ6 were reworded in round 3. Because CGQ is the moderator, its reliability matters more than usual: a low ρ_A here attenuates the interaction directly.

## 2.4 Circular Value-Chain Integration (CVCI) — 6 items

@@TABLE Table A5. CVCI items
ID | Item | Source class
CVCI1 | We plan jointly with partners how material that would otherwise be wasted will be collected and moved. | AV
CVCI2 | We coordinate the timing of our operations with partners so that recoverable material is handled before it deteriorates. | AV
CVCI3 | We share equipment, storage or transport with partners for handling residues and by-products. | AV
CVCI4 | We and our partners exchange the information needed to route recoverable material to where it can be used. | AV
CVCI5 | We agree with partners in advance how the proceeds from recovered material will be shared. | AS
CVCI6 | We work together with partners to find new uses for material that used to be discarded. | AV
@@ENDTABLE

*Note.* Adapted from Flynn, Huo, and Zhao (2010) supply chain integration and Cao and Zhang (2011) collaboration, with the object changed from commercial flows to recoverable flows. CVCI2 was reworded in round 3. **CVCI4 is the item to watch for discriminant overlap with CIT** — it mentions information exchange. If HTMT(CIT, CVCI) approaches 0.85, CVCI4 is the first candidate for scrutiny; note, however, that the blind placement test put boundary leakage at 4.2 per cent, so this is a watch item rather than an expected problem.

## 2.5 Circular Value Creation Performance (CVCP) — 11 items, 3 dimensions

@@TABLE Table A6. CVCP items (change over three seasons; higher = better)
ID | Dimension | Item | Source class
CVCP1 | Economic | Income earned from selling by-products or residues that were previously discarded. | AV
CVCP2 | Economic | Savings from reusing material internally instead of buying new. | AV
CVCP3 | Economic | The price we realise for our main product. | AS
CVCP4 | Economic | Reduction in the cost of disposing of waste. | AS
CVCP5 | Environmental | Reduction in the quantity of material leaving our operation as waste. | AV
CVCP6 | Environmental | Reduction in the share of what we handle that is lost or spoiled. | AV
CVCP7 | Environmental | Reduction in the energy and water used per unit of product. | AS
CVCP8 | Environmental | Reduction in the quantity of residues sent to landfill, burned or dumped. | ND
CVCP9 | Social | The share of the value from recovered material that reaches the producers who supplied it. | ND
CVCP10 | Social | Employment or paid work created by handling and processing recovered material. | ND
CVCP11 | Social | Fairness with which the gains from reducing losses are shared among the actors in this chain. | ND
@@ENDTABLE

*Note.* Economic and environmental items draw on the investment-recovery dimension of Zhu, Sarkis, and Lai (2008). The three social items are wholly new; the social dimension rests on the least developed indicator literature and is the dimension most likely to behave differently in the formative HOC. **That asymmetry is theoretically interesting, not a defect** — see Section 8, Table A13.

## 2.6 Controls, marker, screening and objective indicators

@@TABLE Table A7. Controls (eight), marker, screening and objective indicators
Code | Variable | Measurement | Entered how
DTC1–DTC3 | Digital traceability capability | 3 reflective items, 7-point (see below) | Composite, Mode A; predicts CIT, CVCI, CVCP
IS1–IS3 | Institutional support | 3 reflective items, 7-point (see below) | Composite, Mode A; predicts CIT, CVCI, CVCP
SIZE_ln | Enterprise size | Number of persons engaged (incl. unpaid family labour); natural log of (1 + n) | Single-item composite
AGE_ln | Enterprise age | Years in operation; natural log of (1 + years) | Single-item composite
VOL_ln | Volume handled | Tonnes handled last season; natural log of (1 + tonnes) | Single-item composite
EDU | Key informant education | Ordinal 1–6 (none, primary, secondary, higher secondary, graduate, postgraduate) | Single-item composite
AFF | Collective affiliation | 1 = producer-organisation / cooperative member, 0 = not | Single-item composite (binary)
TIER | Network position | 1 = upstream producer, 2 = midstream intermediary, 3 = processing/recovery, 4 = downstream buyer | **Not entered as a covariate — used as the MGA grouping variable.** See Section 4.3
MK1–MK3 | Marker: attitude toward the colour blue | 3 items from Miller and Simmering (2023), **administered verbatim from the source** | Method-bias assessment only; excluded from the structural model
SCR1–SCR4 | Key-informant screening | See below | Eligibility filter, not analysed
OBJ1–OBJ3 | Objective indicators (subsample) | See below | Convergent-validity check on CVCP
@@ENDTABLE

**DTC items (AV).** DTC1 We use digital tools — mobile apps, spreadsheets or software — to record the quantities we handle. DTC2 Material we handle can be traced back to its source using our records or codes. DTC3 We can exchange records of quantities and quality with our partners electronically.

**IS items (AV).** IS1 Government or industry bodies provide us with useful guidance on reducing losses and using residues. IS2 Training and technical advice on handling and processing residues are available to us. IS3 Financial support or subsidy is available for equipment that would let us process residues.

> **IS2 and IS3 are the double-barrelled items** flagged in Section 5.5 as below threshold and never revised. If they were fielded as written, do not silently drop them. Report their psychometrics, and if IS underperforms, the defensible move is to retain IS1 as a single-item control (institutional support is a control, not a focal construct, and single-item control measures are acceptable) and to disclose the reason. Note this in the limitations.

**Marker items.** Reproduce Miller and Simmering's (2023) attitude-toward-blue items exactly from the published source. Do not paraphrase them: the warrant for using a validated marker comes from administering the validated wording, and rewording forfeits it. MK1 rated below the content-validity threshold and was deliberately not revised — for a marker, low substantive relevance is the qualifying property, not a defect.

**Screening items.** SCR1 Do you keep or supervise records of quantities, costs or sales for this enterprise? (must be *yes*). SCR2 Do you take part in decisions about pricing, or about what happens to material that is not sold as product? (must be *yes*). SCR3 How many seasons have you held this role? (must be ≥ 3, because the outcome items are framed as change over three seasons). SCR4 Which best describes your enterprise's role in this chain? (assigns TIER and the sampling stratum).

**Objective indicators (subsample).** OBJ1 loss ratio = quantity rejected or lost ÷ quantity taken in, last season, from records. OBJ2 by-product quantity sold and value realised, last season, from records. OBJ3 realised price for the main product ÷ district modal price for the same period. Use these in a convergent-validity check against CVCP (Section 6 step 4). Remember the check is itself conditional: enterprises able to produce records are those with higher accounting capability, so report the subsample's CAC mean against the full sample's.

# 3. Data file layout and preparation

## 3.1 Variable naming

One row per respondent. Recommended column order and names, which the R script in Section 10 assumes exactly:

`ID, STRATUM, TIER, SCR1, SCR2, SCR3, SCR4, CAC1..CAC9, CIT1..CIT5, CGQ1..CGQ6, CVCI1..CVCI6, CVCP1..CVCP11, DTC1..DTC3, IS1..IS3, MK1..MK3, SIZE_n, AGE_yr, VOL_t, EDU, AFF, OBJ1, OBJ2_qty, OBJ2_val, OBJ3, ENUM, DUR_min, DATE`

Derive `SIZE_ln = log(1 + SIZE_n)`, `AGE_ln = log(1 + AGE_yr)`, `VOL_ln = log(1 + VOL_t)` before estimation. Keep `ENUM` (enumerator ID) and `DUR_min` (interview duration) — both are needed for the robustness battery.

## 3.2 Pre-specified cleaning rules

Apply in this order and report the number of cases removed at each step. The count must reconcile: contacted → screened → completed → analysed.

@@TABLE Table A8. Data cleaning rules and reporting
Step | Rule | Action | Report
1 | Screening failure (SCR1 = no, or SCR2 = no, or SCR3 < 3) | Exclude | n excluded
2 | Missing data on any focal indicator > 15% of items | Exclude case | n excluded
3 | Missing data ≤ 15% | Mean replacement is acceptable in PLS-SEM; **report the proportion of replaced values** | % replaced
4 | Straight-lining: identical response across all 37 focal items | Exclude | n excluded
5 | Long-string: identical response across ≥ 10 consecutive items | Flag, retain, test sensitivity | n flagged
6 | Interview duration below the 5th percentile | Flag, retain, test sensitivity | n flagged
7 | Enumerator effects | Retain; test ICC by enumerator on each construct in the robustness battery | ICC per construct
8 | Multivariate outliers (Mahalanobis D², p < .001 on the 37 focal items) | Retain; re-estimate without them as a robustness check | n identified
@@ENDTABLE

Steps 5, 6 and 8 are **flag-and-test**, not delete. Deleting flagged cases without reporting the sensitivity analysis is the single most common source of an undisclosed specification search in this literature.

## 3.3 Descriptives to report before the measurement model

Per item: n, mean, SD, skewness, kurtosis, % at floor (1), % at ceiling (7). Per construct: mean, SD, and mean by stratum. **Check CGQ's dispersion specifically.** The entire design rests on the claim that governance quality varies widely within this single network and regulatory environment. If CGQ's SD is small or its distribution is bimodal by affiliation only, the interaction will be hard to detect and you need to say so before reporting a null. Report the CGQ standard deviation and its range in the sample-profile table — it is direct evidence for the setting's suitability, and reviewers will look for it.

# 4. Model specification

## 4.1 The two higher-order constructs: disjoint two-stage

Follow Sarstedt et al. (2019). Do **not** use the repeated-indicators approach: it biases the HOC paths when the numbers of indicators across dimensions are unequal, which they are here (3/3/3 for CAC is balanced but 4/4/3 for CVCP is not).

**Stage 1.** Estimate a model in which the six lower-order constructs appear in the structural positions their higher-order construct occupies, all as Mode A composites. Save the construct scores.

- CAC lower-order: `CAC_MEA` = CAC1–CAC3, `CAC_COST` = CAC4–CAC6, `CAC_VAL` = CAC7–CAC9
- CVCP lower-order: `CVCP_ECO` = CVCP1–CVCP4, `CVCP_ENV` = CVCP5–CVCP8, `CVCP_SOC` = CVCP9–CVCP11
- CIT, CGQ, CVCI, DTC, IS keep their own indicators in both stages

**Stage 2.** `CAC` becomes a Mode B composite of the three CAC lower-order scores; `CVCP` becomes a Mode B composite of the three CVCP lower-order scores. All other constructs retain their original indicators.

## 4.2 The latent interaction

Use the **two-stage approach** for CIT × CGQ (not product-indicator, which multiplies the indicator count and is sensitive to indicator counts differing between the two constructs — 5 and 6 here). Standardise CIT and CGQ before forming the product so that the interaction coefficient is interpretable and the main effects remain the effects at the mean.

Report the interaction effect size *f²* against **interaction-specific benchmarks of 0.005, 0.01 and 0.025**, not Cohen's 0.02/0.15/0.35. This is pre-specified in Table 8 of the manuscript and it matters: a genuine conditional effect judged on Cohen's benchmarks will look trivial and a reviewer may say so.

## 4.3 Controls and why network position is not one of them

Predictors on CVCI must number **11**, because the a-priori power analysis (Approach A, Table 6) was computed for 11 predictors on the focal endogenous construct. Preserving that is what keeps the reported power claim honest.

- 4 focal: CIT, CAC, CGQ, CIT × CGQ
- 7 single-degree-of-freedom controls: DTC, IS, SIZE_ln, AGE_ln, VOL_ln, EDU, AFF

Network position (TIER) is therefore **not** entered as a covariate. Dummy-coding four tiers would add three degrees of freedom to an interaction model powered for eleven predictors, and position is in any case a stratification variable rather than a confounder to be partialled out. It is handled through multi-group analysis, which is what the manuscript already specifies. State this reasoning in the methods section — pre-specified and justified is very different from omitted.

## 4.4 The estimated structural equations

Write these into the manuscript; reviewers in this journal expect them.

- **(1)** CIT = β₁·CAC + γ₁ᵈ·DTC + γ₁ⁱ·IS + γ₁ˢ·SIZE_ln + γ₁ᵃ·AGE_ln + γ₁ᵛ·VOL_ln + γ₁ᵉ·EDU + γ₁ᶠ·AFF + ζ₁
- **(2)** CVCI = β₂·CIT + β₄·CAC + β₆ₐ·CGQ + β₆♭·(CIT × CGQ) + γ₂·(7 controls) + ζ₂
- **(3)** CVCP = β₃·CVCI + β₅·CIT + γ₃·(7 controls) + ζ₃

**No path is specified from CAC to CVCP.** That is deliberate and it is what makes H9 a clean claim: accounting's effect on circular value creation is entirely indirect. Do not add the direct path "to see whether it is significant" — if you estimate it, you must report it and the theoretical claim changes.

@@TABLE Table A9. Hypothesis-to-parameter map
Hypothesis | Parameter | Equation | Expected | Decision rule
H1 | β₁ | (1) | + | Bootstrap 95% CI excludes zero, positive
H2 | β₂ | (2) | + | Bootstrap 95% CI excludes zero, positive
H3 | β₃ | (3) | + | Bootstrap 95% CI excludes zero, positive
H4 | β₄ | (2) | + | Bootstrap 95% CI excludes zero, positive
H5 | β₅ | (3) | ≈ 0 / ns | **Supported if the CI includes zero.** Report the point estimate and CI either way
H6a | β₆ₐ | (2) | + | Bootstrap 95% CI excludes zero, positive
H6b (focal) | β₆♭ | (2) | + | CI excludes zero, positive; report f² against 0.005/0.01/0.025
H7 | β₁·β₂ | (1)(2) | + | Specific indirect effect CI excludes zero; complementary mediation expected given H4
H8 | β₂·β₃ | (2)(3) | + | Specific indirect effect CI excludes zero; indirect-only mediation expected given H5
H9 | β₁·β₂·β₃ | (1)(2)(3) | + | Serial indirect effect CI excludes zero; **and** index of moderated mediation β₁·β₆♭·β₃ CI excludes zero
@@ENDTABLE

## 4.5 The three failure conditions — commit now

Section 4.4 of the manuscript forbids three outcomes. Write the reporting sentences before you look at the output.

1. **β₆♭ null while β₂ and β₆ₐ are positive** → the model reduces to an additive capability bundle and the theoretical contribution fails. Report it as a failure, not as "partial support".
2. **β₅ strong and positive net of CVCI** → favours an information-economics account over the mediated conditional one. Report it as disconfirmation of the mechanism, not as "an additional finding".
3. **β₁ null or negative** → accounting is a consequence rather than an antecedent of visibility, inverting the framework.

A paper that pre-registers failure conditions and then reports one honestly is more publishable than one that quietly reframes. If condition 1 occurs, the paper is still publishable as a scale-development-plus-null-interaction contribution, and the null is itself informative given how widely the conditional claim is assumed.

# 5. Common method bias and endogeneity

@@TABLE Table A10. Method-bias and endogeneity procedures
Concern | Procedure | Threshold / decision
Common method variance | **Full collinearity assessment**: regress all constructs on a random dummy; inspect VIF | All VIF < 3.3 → no substantial CMV
Common method variance | **Marker-variable correlations**: MK composite against each focal construct | Correlations near zero expected; report the matrix
Common method variance | **Measured latent marker variable (MLMV)** correction: add MK as a predictor of every endogenous construct and compare path estimates with and without | Report both sets; substantive conclusions must not change
Common method variance | Harman's single-factor test | **Do not run it.** It is pre-specified as not used, and running it invites the criticism that you relied on a discredited diagnostic
Procedural remedies (already built in) | Anonymity; current-state vs change-over-three-seasons separation between predictors and outcome; scripted break; neutral item framing | Describe in methods
Endogeneity | **Gaussian copula** (Park and Gupta 2012) on CAC, CIT and CVCI in turn | First confirm the regressor is non-normal (Kolmogorov–Smirnov / Shapiro–Wilk, p < .05); the method is invalid for normal regressors. Copula term non-significant → no evidence of endogeneity
Endogeneity | **Reversed model**: estimate CIT ← CVCI and compare fit and predictive power | Theorised direction should dominate; report both
Endogeneity | **Rival explanations as measured controls**: DTC and IS | **The key test of the smart-production argument.** If β₁ collapses when DTC enters, CAC is a proxy for digital instrumentation rather than a distinct calculative capacity, and you must say so
Convergent validity of outcome | Objective-indicator subsample (OBJ1–OBJ3) against CVCP | Report correlations and the subsample's CAC mean vs full sample
Non-response / selection | Compare early vs late respondents; compare register-listed vs referral-recruited actors on all focal constructs | Report; referral-recruited informal intermediaries are the segment whose exclusion would bias results upward
@@ENDTABLE

# 6. Estimation protocol — the eleven steps

Run in this order. Each step has a pre-specified action if a criterion is breached, per Table 8 of the manuscript.

**Step 1 — Data preparation.** Apply Table A8. Report the reconciliation count. Derive logged controls. Standardise CIT and CGQ for the interaction.

**Step 2 — Stage-1 measurement assessment (reflective constructs and lower-order constructs).**
- Outer loadings ≥ 0.708. Retain 0.40–0.708 only where deletion does not raise AVE above threshold and content validity requires retention. Below 0.40, delete.
- Reliability ρ_A and ρ_c in 0.70–0.95. Below 0.70, investigate. Above 0.95, check indicator redundancy.
- AVE ≥ 0.50. If breached, apply the pre-registered escalation to a two-dimensional specification rather than deleting items until it passes.
- HTMT < 0.85 with bootstrap CIs. **If HTMT(CAC, CIT) or HTMT(CGQ, CVCI) reaches 0.85, the corresponding claim is withdrawn** — this is pre-specified and must be honoured, not defended.

**Step 3 — Item-retention decisions.** Any deletion must be recorded in a deletion log stating the item, the criterion breached, the action, and the effect on AVE and ρ_A. Content validity takes precedence over statistical criteria. Watch CIT5, CAC7–CAC9 and CVCP9–CVCP11 — the newly developed items, which are also the items that carry the paper's measurement contribution. **Deleting a new item because it underperforms removes the contribution it represents.** If CIT5 must go, say what is lost.

**Step 4 — Stage-2 construction of the formative higher-order constructs.**
- Indicator collinearity VIF < 3 among the three lower-order scores per HOC. 3–5 report and discuss.
- Outer weights significant, or outer loading ≥ 0.50 where the weight is not.
- **Redundancy analysis**: regress each HOC on a global single-item measure of the same construct; path ≥ 0.70. If you did not field global single items, this cannot be done and must be reported as a limitation — check your instrument now, because it is not recoverable after the fact.
- Run the objective-indicator convergent check for CVCP here.

**Step 5 — Method-bias assessment.** Table A10, rows 1–4.

**Step 6 — Structural model estimation.** Inner VIF < 3 (3–5 report and discuss). Path coefficients with 10,000-subsample bootstrap, percentile **and** bias-corrected CIs. R² and adjusted R² for CIT, CVCI, CVCP. f² for every path, with interaction-specific benchmarks for β₆♭.

**Step 7 — Simple slopes and Johnson–Neyman.** Plot the CIT → CVCI slope at CGQ = −1 SD, mean, +1 SD. Compute the **Johnson–Neyman point**: the CGQ value at which the slope's CI first includes zero. This is the paper's actionable output — the governance level below which transparency does not move material. Report it in the construct's original scale as well as in standard-deviation units so a practitioner can locate it.

**Step 8 — Mediation and conditional indirect effects.**
- Specific indirect effects for H7, H8, H9, each with bootstrap CIs. **The criterion is the indirect effect's CI, not a significant total effect.**
- Classify mediation: complementary (partial) expected for H7 given H4; indirect-only (full) expected for H8 given H5.
- **Index of moderated mediation** = β₁ · β₆♭ · β₃, with bootstrap CI.
- **Conditional indirect effects** of CAC on CVCP at CGQ = −1 SD, mean, +1 SD. The theoretical claim is that the low-governance conditional indirect effect is **not** distinguishable from zero. That is the central empirical quantity in the paper — put it in the abstract.

**Step 9 — Predictive assessment.** Q²predict > 0 for all endogenous constructs. PLSpredict with 10 folds and 10 repetitions; compare PLS-SEM RMSE against the linear-model benchmark, item by item. Run CVPAT (cross-validated predictive ability test) against both the linear benchmark and the indicator-average benchmark. Additionally, run **prediction-oriented comparison against the two rejected specifications** from Section 4.3 of the manuscript — the four-link serial chain and the parallel-capabilities model. This converts the paper's a-priori specification argument into an empirical result and is a genuinely distinctive contribution; do not skip it.

**Step 10 — Multi-group analysis.** Grouping variables, in priority order: TIER (upstream / midstream / processing / downstream), AFF (affiliated / not), SIZE (median split). Establish measurement invariance first via **MICOM** (configural, compositional, equality of means and variances) before comparing paths — an MGA reported without MICOM will be challenged. Use permutation-based MGA. **Do not run the producer-versus-processor comparison**: with roughly 70 processors it requires β ≥ 0.30 to be detectable, and the manuscript already states it will not be conducted and why. Honour that.

**Step 11 — Robustness battery (eleven checks).**

@@TABLE Table A11. Robustness battery
# | Check | What it addresses
1 | Re-estimate excluding multivariate outliers | Influential cases
2 | Re-estimate excluding long-string and fast-completion flagged cases | Careless responding
3 | Re-estimate with listwise deletion instead of mean replacement | Missing-data treatment
4 | Re-estimate without the seven controls | Control-set sensitivity
5 | Re-estimate with the reversed path (CVCI → CIT) | Directional assumption
6 | Re-estimate with the MLMV marker correction applied | Common method variance
7 | Re-estimate with CVCP as three separate dependent constructs rather than one HOC | Dimensional asymmetry (see Table A13)
8 | Re-estimate using the product-indicator instead of two-stage interaction | Interaction operationalisation
9 | Re-estimate by consistent PLS (PLSc) | Composite vs common-factor assumption
10 | Re-estimate by covariance-based SEM on the reflective portion | Estimator sensitivity (see Section 11) |
11 | Enumerator ICC and re-estimation with enumerator fixed effects | Interviewer effects
@@ENDTABLE

Report every check in a supplementary table with the focal parameters β₂, β₆♭ and the index of moderated mediation in each. If any check reverses a conclusion, that belongs in the main text, not the supplement.

# 7. Result tables to produce

Build these as empty shells first and fill them. Numbering continues from the eight tables already in the manuscript.

@@TABLE Table A12. Required result tables
Table | Content | Columns
9 | Sample profile and response accounting | Stratum; targeted; contacted; screened out; completed; analysed; response rate; **CGQ mean and SD by stratum**
10 | Descriptive statistics and construct correlations | Construct; mean; SD; skew; kurtosis; correlations below diagonal; **HTMT above diagonal**
11 | Reflective measurement model | Construct; item; loading; t; ρ_A; ρ_c; AVE
12 | Formative higher-order constructs | HOC; dimension; outer weight; t; outer loading; VIF; redundancy-analysis path
13 | Discriminant validity | HTMT matrix with bootstrap upper CIs; flag the CAC–CIT and CGQ–CVCI cells explicitly
14 | Common method bias | Full-collinearity VIF; marker correlations; paths with and without MLMV correction
15 | Structural model | Path; β; SE; t; p; 95% percentile CI; 95% BC CI; f²; VIF; hypothesis; supported?
16 | Explanatory and predictive power | Construct; R²; adj. R²; Q²predict; RMSE(PLS) vs RMSE(LM); CVPAT loss difference
17 | Mediation | Effect; point estimate; CI; type (complementary / indirect-only / none); hypothesis
18 | Moderation | Interaction β; f² vs 0.005/0.01/0.025; simple slopes at −1SD/mean/+1SD with CIs; **Johnson–Neyman point in raw and SD units**
19 | Conditional indirect effects and index of moderated mediation | CGQ level; conditional indirect effect; CI; index; index CI
20 | Specification comparison | Model; R²(CVCI); R²(CVCP); Q²predict; CVPAT; serial indirect effect; verdict — adopted three-link vs rejected four-link vs parallel-capabilities
21 | Multi-group analysis | MICOM results; then group-wise β for β₂, β₆ₐ, β₆♭ with permutation p-values
22 (supplementary) | Robustness battery | Check; β₂; β₆♭; index of moderated mediation; conclusion changed?
@@ENDTABLE

# 8. Interpreting the three most likely outcome patterns

Prepare the interpretation in advance so that the discussion is not written to fit whatever emerged.

@@TABLE Table A13. Pre-committed interpretations
Pattern | What it means | Where it goes
β₆♭ positive; conditional indirect effect significant at high CGQ and not at low CGQ | **Full support for the central claim.** Governance is the conversion mechanism, not an additive good. The Johnson–Neyman point is the headline practical output | Abstract; §7 discussion; §11 policy sequencing argument
β₆♭ positive but small; conditional indirect effect significant at both levels, larger at high CGQ | Governance amplifies rather than gates. Weaker but still novel: the claim becomes "governance conditions the magnitude" not "governance conditions the existence" | Requires softening the §8 and §11 claims; say so explicitly rather than overstating
β₆♭ null | **Failure condition 1.** The theoretical contribution fails and the model is an additive bundle | Report as a null. Reposition the paper's contribution onto the instrument and the specification comparison, both of which stand independently
CVCP_SOC weight low or non-significant while ECO and ENV are strong | The distributional finding: circularity releases value that the actors who observe the losses do not capture | This is a **finding, not a measurement failure.** It is the strongest sustainability contribution available and connects directly to the just-transition argument in §10. Run robustness check 7 to confirm
β₅ significant and positive | **Failure condition 2.** Information-economics account favoured | Report as disconfirmation; discuss what it implies for transparency mandates that do not change physical flows
β₁ collapses when DTC is entered | CAC is a proxy for digital traceability | Fatal to the paper's premise. Report it; the honest conclusion is that the calculative and technical layers are not empirically separable in this setting
@@ENDTABLE

# 9. SmartPLS 4 click-path

1. Import the CSV. Set missing-value marker. Confirm all indicators are numeric.
2. **Stage-1 project.** Draw CAC_MEA, CAC_COST, CAC_VAL, CIT, CGQ, CVCI, CVCP_ECO, CVCP_ENV, CVCP_SOC, DTC, IS. All Mode A. Draw the theoretical paths with the lower-order constructs in their higher-order construct's positions. Calculate → PLS-SEM (path weighting, +1 initial weights, 3000 iterations, stop 1.0E-7).
3. Export latent variable scores. Merge the six lower-order construct scores into your dataset.
4. **Stage-2 project.** Import the merged file. CAC and CVCP as Mode B composites of their three scores; CIT, CGQ, CVCI, DTC, IS with original indicators; SIZE_ln, AGE_ln, VOL_ln, EDU, AFF as single-item constructs.
5. Add the moderation: right-click CVCI → Add Moderating Effect → independent CIT, moderator CGQ, **two-stage**, standardised.
6. Draw the three structural equations from Section 4.4. Confirm CVCI has exactly 11 predictors.
7. Calculate → PLS-SEM. Then Bootstrapping: 10,000 subsamples, complete bootstrapping, BCa **and** percentile intervals, two-tailed, 0.05, "no sign changes".
8. Moderation → simple slope plot; and use the continuous moderation output for the Johnson–Neyman region.
9. Bootstrapping output → Total Indirect Effects and Specific Indirect Effects for H7–H9; and Moderated Mediation for the index.
10. Calculate → PLSpredict: 10 folds, 10 repetitions. Then CVPAT.
11. Calculate → MICOM (permutation) for each grouping variable, then Multi-Group Analysis (permutation).
12. Robustness: Calculate → PLSc for check 9; Nonlinear Effects and Endogeneity (Gaussian copula) for the endogeneity assessment.

# 10. R script (seminr)

A complete script is supplied as `analysis_seminr.R` in the same folder. It assumes the column names in Section 3.1. Two cautions:

- **Verify the API against your installed `seminr` version.** Function signatures for `higher_composite()`, `specific_effect_significance()` and the bootstrap object's internals have changed across releases. Run the script section by section rather than end to end the first time.
- `seminr` does not implement MICOM as completely as SmartPLS. Use SmartPLS for step 10 (multi-group analysis) even if you run everything else in R, and say which software produced which result in the methods section.

# 11. Covariance-based robustness check

The manuscript pre-specifies CB-SEM as a robustness check and — importantly — states that the reason for choosing PLS was *not* sample size. Be precise about what the check can and cannot do.

The two reflective-formative higher-order constructs cannot be estimated in CB-SEM without identification constraints that distort the theorised structure. This is one of the stated reasons for choosing composite-based estimation, so a CB-SEM replication of the *full* model is not the right check and running one anyway would misrepresent the comparison.

Run instead: a CB-SEM (ML, robust SEs) estimate of the **reflective portion** — CIT, CGQ, CVCI as latent common factors, with the CAC and CVCP dimensions entered at lower-order level as three-indicator and three/four-indicator factors respectively, and the interaction handled by latent moderated structural equations or by the unconstrained product-indicator approach. Report χ², CFI, TLI, RMSEA, SRMR, and compare β₂, β₆ₐ and β₆♭ against the PLS estimates. Disclose any divergence. Report SRMR for the PLS model too, since it is the one absolute-fit index available there.

# 12. What changes in the manuscript now that data exist

@@TABLE Table A14. Manuscript revisions required
Location | Change
Title | Keep. "From vision to measurable practice" now reads as a claim the paper delivers on
Abstract | Replace with the alternative shell in Section 5 of the submission pack, filling every bracketed slot with real estimates. Lead the results with the **conditional indirect effect** and the **Johnson–Neyman point**, not with β₁
§1.3 Contributions and scope | Delete the boundary statement "the structural model is specified and its instrument validated here; it is not estimated." Replace with the sample description
§5 Research design | Change tense from proposed to executed throughout. Table 5 becomes achieved composition alongside targets. Add response-rate accounting, ethics approval and informed-consent statements
§5.4 | Retain the a-priori derivation, then add achieved *n* and, if *n* < 511, a post-hoc power statement for the interaction. Do not delete the derivation — computing power against the interaction rather than the largest path is a methodological strength
§5.5 | Keep in full. The three-round validation including the failed round remains a distinctive strength and now serves as the measurement-model foundation
§6 Analytical strategy | Change from "the protocol proceeds" to "the protocol proceeded". Move the threshold table forward as the criteria applied
**New §7 Results** | Insert Tables 9–21 with narrative. This is the section that does not currently exist
§7 → §8 Discussion | Rewrite around actual findings. Keep the three convergences and three tensions structure — the tensions section becomes the adjudication it promises
§8 → §9 Theoretical contributions | Convert predictions to findings. The Scope-3-as-accountability-problem claim becomes evidenced rather than argued
§9 → §10 Managerial implications | Replace "once the structural estimates are available" with the estimates. The Johnson–Neyman threshold becomes a number managers can use
§11 Policy implications | The sequencing argument becomes empirically grounded. If the low-governance conditional indirect effect is null, say so plainly — it is the strongest policy sentence in the paper
§12 Limitations | **Delete the first limitation** (model not estimated) and the whole framing that follows from it. Retain the cross-sectional, single-informant, non-probability, new-item, carbon-denomination and social-indicator limitations. Add any item deletions and the reason
Declarations | Add ethics approval reference, informed consent statement, and funding statement
Appendices | Appendix A the full instrument with source codes; Appendix B panel composition and item-level validation results; Appendix C scoring script and raw returns; Appendix D robustness battery
@@ENDTABLE

**On length.** Adding a results section to a body already at ~14,500 words makes the reduction plan in the editorial assessment mandatory rather than advisable. Target ~10,000 words including results. The literature review is where the space is: it is currently comprehensive to the point of being a review, and 1,800 words can come out of §2.4 and §2.5 without losing an argument.
