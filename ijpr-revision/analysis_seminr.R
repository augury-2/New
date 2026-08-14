###############################################################################
# Circular accounting capability -> transparency -> integration -> circular value
# Moderated serial mediation with a governance contingency.
#
# Companion to: "From vision to measurable practice: circular accounting
# capability, chain transparency and the governance conditions of net-zero
# value creation in fragmented manufacturing networks"
#
# Implements the eleven-step protocol. Disjoint two-stage for the two
# reflective-formative higher-order constructs (Sarstedt et al. 2019);
# two-stage latent interaction; 10,000-subsample bootstrap.
#
# BEFORE YOU RUN:
#  1. seminr's API has changed across releases. Run SECTION BY SECTION the
#     first time and check each object, rather than sourcing the whole file.
#  2. Column names must match Section 3.1 of the analysis protocol.
#  3. MICOM/MGA (step 10) is more completely implemented in SmartPLS. Use
#     SmartPLS for that step and say so in the methods section.
###############################################################################

library(seminr)
library(psych)

set.seed(20260814)
NBOOT <- 10000
CORES <- max(1, parallel::detectCores() - 1)
OUT   <- "results"; dir.create(OUT, showWarnings = FALSE)
w     <- function(x, f) write.csv(x, file.path(OUT, f), row.names = TRUE)

## ===========================================================================
## STEP 1  DATA PREPARATION
## ===========================================================================

raw <- read.csv("data.csv", stringsAsFactors = FALSE)

FOCAL <- c(paste0("CAC", 1:9), paste0("CIT", 1:5), paste0("CGQ", 1:6),
           paste0("CVCI", 1:6), paste0("CVCP", 1:11))
CTRL_ITEMS <- c(paste0("DTC", 1:3), paste0("IS", 1:3))
MARKER <- paste0("MK", 1:3)
ALLITEMS <- c(FOCAL, CTRL_ITEMS, MARKER)

stopifnot(all(ALLITEMS %in% names(raw)))

log_n <- c(contacted = nrow(raw))

# --- rule 1: screening -------------------------------------------------------
df <- subset(raw, SCR1 == 1 & SCR2 == 1 & SCR3 >= 3)
log_n["after_screening"] <- nrow(df)

# --- rule 2: >15% missing on focal items ------------------------------------
miss_rate <- rowMeans(is.na(df[, FOCAL]))
df <- df[miss_rate <= 0.15, ]
log_n["after_missing"] <- nrow(df)

# --- rule 3: mean replacement for remaining missing, and report -------------
n_replaced <- sum(is.na(df[, ALLITEMS]))
pct_replaced <- 100 * n_replaced / (nrow(df) * length(ALLITEMS))
for (v in ALLITEMS) df[[v]][is.na(df[[v]])] <- mean(df[[v]], na.rm = TRUE)
cat(sprintf("Mean-replaced values: %d (%.2f%% of all item responses)\n",
            n_replaced, pct_replaced))

# --- rule 4: straight-lining across all focal items -------------------------
sl <- apply(df[, FOCAL], 1, function(r) length(unique(r)) == 1)
df <- df[!sl, ]
log_n["after_straightlining"] <- nrow(df)

# --- rules 5,6,8: FLAG ONLY (do not delete; test in robustness battery) -----
longest_run <- function(r) { rl <- rle(as.numeric(r)); max(rl$lengths) }
df$FLAG_LONGSTRING <- apply(df[, FOCAL], 1, longest_run) >= 10
df$FLAG_FAST <- if ("DUR_min" %in% names(df)) {
  df$DUR_min < quantile(df$DUR_min, 0.05, na.rm = TRUE)
} else FALSE
D2 <- mahalanobis(df[, FOCAL], colMeans(df[, FOCAL]), cov(df[, FOCAL]))
df$FLAG_OUTLIER <- pchisq(D2, df = length(FOCAL), lower.tail = FALSE) < 0.001

cat(sprintf("Flagged (retained): longstring %d | fast %d | outlier %d\n",
            sum(df$FLAG_LONGSTRING), sum(df$FLAG_FAST), sum(df$FLAG_OUTLIER)))

# --- derived controls -------------------------------------------------------
df$SIZE_ln <- log1p(df$SIZE_n)
df$AGE_ln  <- log1p(df$AGE_yr)
df$VOL_ln  <- log1p(df$VOL_t)
CTRL <- c("DTC", "IS", "SIZE_ln", "AGE_ln", "VOL_ln", "EDU", "AFF")

log_n["analysed"] <- nrow(df)
print(log_n); w(as.data.frame(log_n), "T09_response_accounting.csv")

## --- Table 10 inputs: item and construct descriptives ----------------------
item_desc <- psych::describe(df[, ALLITEMS])[, c("n","mean","sd","skew","kurtosis")]
item_desc$pct_floor   <- sapply(df[, ALLITEMS], function(x) 100 * mean(x == 1))
item_desc$pct_ceiling <- sapply(df[, ALLITEMS], function(x) 100 * mean(x == 7))
w(item_desc, "T10a_item_descriptives.csv")

# CRITICAL: does governance quality actually vary? The whole design rests on it.
cgq_raw <- rowMeans(df[, paste0("CGQ", 1:6)])
cat(sprintf("\n*** CGQ dispersion: mean %.3f, SD %.3f, range %.2f-%.2f, IQR %.2f\n",
            mean(cgq_raw), sd(cgq_raw), min(cgq_raw), max(cgq_raw), IQR(cgq_raw)))
cat("    Report this in Table 9. Low dispersion = the interaction cannot be\n")
cat("    detected, and that must be stated BEFORE reporting any null.\n\n")
if ("TIER" %in% names(df))
  print(aggregate(cgq_raw, list(TIER = df$TIER), function(x) c(m = mean(x), s = sd(x))))

## ===========================================================================
## STEP 2  STAGE-1 MEASUREMENT MODEL (LOCs + reflective constructs)
## ===========================================================================

mm1 <- constructs(
  composite("CAC_MEA",  multi_items("CAC",  1:3),  weights = mode_A),
  composite("CAC_COST", multi_items("CAC",  4:6),  weights = mode_A),
  composite("CAC_VAL",  multi_items("CAC",  7:9),  weights = mode_A),
  composite("CIT",      multi_items("CIT",  1:5),  weights = mode_A),
  composite("CGQ",      multi_items("CGQ",  1:6),  weights = mode_A),
  composite("CVCI",     multi_items("CVCI", 1:6),  weights = mode_A),
  composite("CVCP_ECO", multi_items("CVCP", 1:4),  weights = mode_A),
  composite("CVCP_ENV", multi_items("CVCP", 5:8),  weights = mode_A),
  composite("CVCP_SOC", multi_items("CVCP", 9:11), weights = mode_A),
  composite("DTC",      multi_items("DTC",  1:3),  weights = mode_A),
  composite("IS",       multi_items("IS",   1:3),  weights = mode_A)
)

# LOCs occupy the structural positions of their higher-order construct
sm1 <- relationships(
  paths(from = c("CAC_MEA","CAC_COST","CAC_VAL","DTC","IS"), to = "CIT"),
  paths(from = c("CAC_MEA","CAC_COST","CAC_VAL","CIT","CGQ","DTC","IS"), to = "CVCI"),
  paths(from = c("CVCI","CIT","DTC","IS"),
        to   = c("CVCP_ECO","CVCP_ENV","CVCP_SOC"))
)

m1 <- estimate_pls(data = df, measurement_model = mm1, structural_model = sm1,
                   inner_weights = path_weighting)
s1 <- summary(m1)

w(s1$loadings,    "T11_stage1_loadings.csv")
w(s1$reliability, "T11_stage1_reliability.csv")   # alpha, rhoC, AVE, rhoA
w(s1$validity$htmt, "T13_stage1_htmt.csv")

cat("\n--- Step 2 checks ---\n")
cat("Loadings < 0.708 (inspect; delete only if < 0.40 or AVE requires it):\n")
print(which(abs(s1$loadings) < 0.708 & s1$loadings != 0, arr.ind = TRUE))
cat("AVE < 0.50:\n"); print(s1$reliability[s1$reliability[, "AVE"] < 0.50, , drop = FALSE])

# PRE-SPECIFIED WITHDRAWAL RULE - honour it, do not defend it
h <- s1$validity$htmt
chk <- function(a, b, lbl) {
  v <- suppressWarnings(max(h[a, b], h[b, a], na.rm = TRUE))
  cat(sprintf("HTMT %-28s = %.3f  %s\n", lbl, v,
      ifelse(v >= 0.85, "*** BREACH: withdraw the corresponding claim ***", "ok")))
}
cat("\nCritical discriminant boundaries (pre-specified 0.85 withdrawal rule):\n")
for (d in c("CAC_MEA","CAC_COST","CAC_VAL")) chk(d, "CIT", paste(d, "<-> CIT"))
chk("CGQ", "CVCI", "CGQ <-> CVCI")

## ===========================================================================
## STEP 4  STAGE 2: FORMATIVE HIGHER-ORDER CONSTRUCTS + INTERACTION
## ===========================================================================

LOC <- c("CAC_MEA","CAC_COST","CAC_VAL","CVCP_ECO","CVCP_ENV","CVCP_SOC")
scores <- as.data.frame(m1$construct_scores)[, LOC]
df2 <- cbind(df, scores)

# Standardise the interaction constituents so main effects are effects at the mean
df2$CIT_z <- scale(rowMeans(df2[, paste0("CIT", 1:5)]))[, 1]
df2$CGQ_z <- scale(rowMeans(df2[, paste0("CGQ", 1:6)]))[, 1]

mm2 <- constructs(
  composite("CAC",  c("CAC_MEA","CAC_COST","CAC_VAL"),        weights = mode_B),
  composite("CVCP", c("CVCP_ECO","CVCP_ENV","CVCP_SOC"),      weights = mode_B),
  composite("CIT",  multi_items("CIT",  1:5),  weights = mode_A),
  composite("CGQ",  multi_items("CGQ",  1:6),  weights = mode_A),
  composite("CVCI", multi_items("CVCI", 1:6),  weights = mode_A),
  composite("DTC",  multi_items("DTC",  1:3),  weights = mode_A),
  composite("IS",   multi_items("IS",   1:3),  weights = mode_A),
  composite("SIZE_ln", single_item("SIZE_ln")),
  composite("AGE_ln",  single_item("AGE_ln")),
  composite("VOL_ln",  single_item("VOL_ln")),
  composite("EDU",     single_item("EDU")),
  composite("AFF",     single_item("AFF")),
  interaction_term(iv = "CIT", moderator = "CGQ", method = two_stage)
)

# Equations (1)-(3) from Section 4.4. NOTE: exactly 11 predictors on CVCI,
# matching the a-priori power analysis. No CAC -> CVCP path (H9 is a clean claim).
sm2 <- relationships(
  paths(from = c("CAC", CTRL),                            to = "CIT"),
  paths(from = c("CIT","CAC","CGQ","CIT*CGQ", CTRL),      to = "CVCI"),
  paths(from = c("CVCI","CIT", CTRL),                     to = "CVCP")
)

m2 <- estimate_pls(data = df2, measurement_model = mm2, structural_model = sm2,
                   inner_weights = path_weighting)
s2 <- summary(m2)

cat(sprintf("\nPredictors on CVCI = %d (must be 11)\n",
            sum(sm2[, "target"] == "CVCI")))

w(s2$weights,                "T12_HOC_outer_weights.csv")
w(s2$loadings,               "T12_HOC_outer_loadings.csv")
w(s2$validity$vif_items,     "T12_formative_indicator_VIF.csv")
w(s2$vif_antecedents,        "T15_inner_VIF.csv")
w(s2$paths,                  "T15_paths_point_estimates.csv")
w(s2$fSquare,                "T15_fsquared.csv")

cat("\nR-squared:\n"); print(s2$paths[c("R^2","AdjR^2"), , drop = FALSE])
cat("\n*** Interaction f2 must be judged against 0.005 / 0.01 / 0.025,",
    "NOT Cohen's 0.02/0.15/0.35 ***\n")
print(s2$fSquare["CIT*CGQ", "CVCI"])

## --- Redundancy analysis for the two formative HOCs ------------------------
## Requires GLOBAL SINGLE-ITEM measures (e.g. CAC_GLOBAL, CVCP_GLOBAL).
## If these were not fielded, this cannot be done after the fact and must be
## reported as a limitation. Check your instrument now.
if (all(c("CAC_GLOBAL","CVCP_GLOBAL") %in% names(df2))) {
  for (hoc in c("CAC","CVCP")) {
    g <- paste0(hoc, "_GLOBAL")
    dims <- if (hoc == "CAC") LOC[1:3] else LOC[4:6]
    rm_ <- constructs(composite(hoc, dims, weights = mode_B),
                      composite("G", single_item(g)))
    rs_ <- relationships(paths(from = hoc, to = "G"))
    r_  <- estimate_pls(df2, rm_, rs_)
    cat(sprintf("Redundancy analysis %s -> global: %.3f (need >= 0.70)\n",
                hoc, summary(r_)$paths[hoc, "G"]))
  }
} else {
  cat("\n!! No global single-item measures found: redundancy analysis cannot be\n")
  cat("   run. Report as a limitation (convergent validity of the formative\n")
  cat("   HOCs not established).\n")
}

## --- Objective-indicator convergent check for CVCP -------------------------
if ("OBJ1" %in% names(df2)) {
  sub <- !is.na(df2$OBJ1)
  cvcp_s <- as.data.frame(m2$construct_scores)$CVCP
  cac_s  <- as.data.frame(m2$construct_scores)$CAC
  cat(sprintf("\nObjective subsample n = %d\n", sum(sub)))
  print(cor(cbind(CVCP = cvcp_s[sub],
                  loss_ratio = df2$OBJ1[sub],
                  byprod_val = df2$OBJ2_val[sub],
                  price_ratio = df2$OBJ3[sub]),
            use = "pairwise"))
  cat(sprintf("CAC mean, records subsample %.3f vs full sample %.3f",
              mean(cac_s[sub]), mean(cac_s)))
  cat("  <- the check is itself conditional; report this gap.\n")
}

## ===========================================================================
## STEP 5  COMMON METHOD BIAS
## ===========================================================================

## (a) Full collinearity: regress every construct on a random dummy, VIF < 3.3
cs <- as.data.frame(m2$construct_scores)
set.seed(99); cs$RND <- rnorm(nrow(cs))
fc <- sapply(setdiff(names(cs), "RND"), function(v) {
  o <- setdiff(names(cs), c("RND", v))
  1 / (1 - summary(lm(as.formula(paste(v, "~", paste(o, collapse = "+"))),
                      data = cs))$r.squared)
})
cat("\nFull collinearity VIF (all must be < 3.3):\n"); print(round(fc, 3))
w(as.data.frame(fc), "T14_full_collinearity_VIF.csv")

## (b) Marker correlations - should be near zero
df2$MK <- rowMeans(df2[, MARKER])
mk_cor <- cor(df2$MK, cs[, c("CAC","CIT","CGQ","CVCI","CVCP")])
cat("\nMarker (colour blue) correlations with focal constructs:\n"); print(round(mk_cor, 3))
w(as.data.frame(mk_cor), "T14_marker_correlations.csv")

## (c) MLMV correction: add the marker as a predictor of every endogenous
##     construct and compare. Substantive conclusions must not change.
mm2m <- append(mm2, constructs(composite("MK", multi_items("MK", 1:3), weights = mode_A)))
sm2m <- relationships(
  paths(from = c("CAC", CTRL, "MK"),                       to = "CIT"),
  paths(from = c("CIT","CAC","CGQ","CIT*CGQ", CTRL, "MK"), to = "CVCI"),
  paths(from = c("CVCI","CIT", CTRL, "MK"),                to = "CVCP")
)
m2m <- estimate_pls(df2, mm2m, sm2m, inner_weights = path_weighting)
cat("\nPaths WITHOUT vs WITH marker correction (compare, report both):\n")
cmp <- cbind(uncorrected = c(CAC_CIT   = s2$paths["CAC","CIT"],
                             CIT_CVCI  = s2$paths["CIT","CVCI"],
                             INT_CVCI  = s2$paths["CIT*CGQ","CVCI"],
                             CVCI_CVCP = s2$paths["CVCI","CVCP"],
                             CIT_CVCP  = s2$paths["CIT","CVCP"]),
             corrected  = c(summary(m2m)$paths["CAC","CIT"],
                            summary(m2m)$paths["CIT","CVCI"],
                            summary(m2m)$paths["CIT*CGQ","CVCI"],
                            summary(m2m)$paths["CVCI","CVCP"],
                            summary(m2m)$paths["CIT","CVCP"]))
print(round(cmp, 4)); w(as.data.frame(cmp), "T14_MLMV_comparison.csv")

## NOTE: Harman's single-factor test is deliberately NOT run (pre-specified).

## ===========================================================================
## STEP 6  BOOTSTRAP: PATHS, CIs, HYPOTHESIS TESTS
## ===========================================================================

boot <- bootstrap_model(seminr_model = m2, nboot = NBOOT, cores = CORES)
sb   <- summary(boot, alpha = 0.05)

w(sb$bootstrapped_paths,   "T15_bootstrapped_paths.csv")
w(sb$bootstrapped_weights, "T12_bootstrapped_weights.csv")
if (!is.null(sb$bootstrapped_HTMT)) w(sb$bootstrapped_HTMT, "T13_htmt_CIs.csv")

H <- data.frame(
  hypothesis = c("H1","H2","H3","H4","H5","H6a","H6b"),
  path = c("CAC->CIT","CIT->CVCI","CVCI->CVCP","CAC->CVCI",
           "CIT->CVCP","CGQ->CVCI","CIT*CGQ->CVCI"),
  expected = c("+","+","+","+","approx 0 / ns","+","+"),
  stringsAsFactors = FALSE)
key <- c("CAC  ->  CIT","CIT  ->  CVCI","CVCI  ->  CVCP","CAC  ->  CVCI",
         "CIT  ->  CVCP","CGQ  ->  CVCI","CIT*CGQ  ->  CVCI")
rn <- rownames(sb$bootstrapped_paths)
H$row <- sapply(key, function(k) { i <- grep(gsub(" ", "", k),
                gsub(" ", "", rn), fixed = TRUE); if (length(i)) rn[i[1]] else NA })
print(sb$bootstrapped_paths)
cat("\n>>> Map the rows above onto Table 15 by hand if the auto-match is empty:\n")
print(H)

cat("\n*** FAILURE CONDITIONS (Section 4.4) - check and report honestly ***\n")
cat(" 1. CIT*CGQ null while CIT and CGQ positive -> additive bundle; contribution FAILS\n")
cat(" 2. CIT->CVCP strong and positive -> information-economics account favoured\n")
cat(" 3. CAC->CIT null or negative -> framework inverted\n")
cat("Report each whichever way it falls. Do not reframe a null as partial support.\n")

## ===========================================================================
## STEP 7  SIMPLE SLOPES AND JOHNSON-NEYMAN
## ===========================================================================
## Slope of CIT on CVCI at a given CGQ = b2 + b6b * CGQ.
## CIs come from the bootstrap replicates of b2 and b6b jointly, which
## correctly propagates their covariance.

bp <- boot$boot_paths                       # array: [from, to, replicate]
r_cit <- grep("^CIT$",     dimnames(bp)[[1]])
r_int <- grep("CIT\\*CGQ", dimnames(bp)[[1]])
c_cvci <- grep("^CVCI$",   dimnames(bp)[[2]])
b2v <- bp[r_cit, c_cvci, ]
b6v <- bp[r_int, c_cvci, ]

grid <- seq(-3, 3, by = 0.05)
slopes <- do.call(rbind, lapply(grid, function(g) {
  s <- b2v + b6v * g
  data.frame(CGQ_z = g,
             slope = mean(s),
             lo = quantile(s, .025, names = FALSE),
             hi = quantile(s, .975, names = FALSE))
}))
slopes$significant <- slopes$lo > 0 | slopes$hi < 0
w(slopes, "T18_simple_slopes_grid.csv")

cat("\nSimple slopes of CIT -> CVCI at CGQ = -1SD, mean, +1SD:\n")
print(round(slopes[slopes$CGQ_z %in% c(-1, 0, 1), ], 4))

ns <- slopes[!slopes$significant, "CGQ_z"]
if (length(ns) && length(ns) < nrow(slopes)) {
  jn <- max(ns)
  cgq_mean <- mean(cgq_raw); cgq_sd <- sd(cgq_raw)
  cat(sprintf("\n*** JOHNSON-NEYMAN POINT: CGQ_z = %.3f  (raw scale = %.2f on 1-7)\n",
              jn, cgq_mean + jn * cgq_sd))
  cat(sprintf("    Below this governance level the transparency->integration\n"))
  cat(sprintf("    relationship is not distinguishable from zero.\n"))
  cat(sprintf("    %.1f%% of the sample sits below it.\n",
              100 * mean(scale(cgq_raw)[, 1] < jn)))
  cat("    THIS IS THE PAPER'S HEADLINE PRACTICAL OUTPUT - put it in the abstract.\n")
} else if (all(slopes$significant)) {
  cat("\nSlope significant across the observed CGQ range: governance AMPLIFIES\n")
  cat("rather than GATES. Soften the section 8 and 11 claims accordingly\n")
  cat("(see Table A13, pattern 2).\n")
} else {
  cat("\nSlope never significant: see failure condition 1.\n")
}

pdf(file.path(OUT, "F5_johnson_neyman.pdf"), width = 7, height = 5)
plot(slopes$CGQ_z, slopes$slope, type = "l", lwd = 2, ylim = range(slopes[, c("lo","hi")]),
     xlab = "Circular governance quality (standardised)",
     ylab = "Slope of circular information transparency on integration")
polygon(c(slopes$CGQ_z, rev(slopes$CGQ_z)), c(slopes$lo, rev(slopes$hi)),
        col = rgb(0, 0, 0, .12), border = NA)
abline(h = 0, lty = 2)
dev.off()

## ===========================================================================
## STEP 8  MEDIATION, MODERATED MEDIATION, CONDITIONAL INDIRECT EFFECTS
## ===========================================================================
## Criterion is the indirect effect's CI. A significant TOTAL effect is NOT required.

cat("\n--- H7: CAC -> CIT -> CVCI ---\n")
print(specific_effect_significance(boot, from = "CAC", through = "CIT",
                                   to = "CVCI", alpha = 0.05))
cat("\n--- H8: CIT -> CVCI -> CVCP ---\n")
print(specific_effect_significance(boot, from = "CIT", through = "CVCI",
                                   to = "CVCP", alpha = 0.05))
cat("\n--- H9: CAC -> CIT -> CVCI -> CVCP ---\n")
print(specific_effect_significance(boot, from = "CAC", through = c("CIT","CVCI"),
                                   to = "CVCP", alpha = 0.05))

## Index of moderated mediation = b1 * b6b * b3, and conditional indirect
## effects of CAC on CVCP at levels of CGQ = b1 * (b2 + b6b*CGQ) * b3
r_cac <- grep("^CAC$",  dimnames(bp)[[1]]); c_cit  <- grep("^CIT$",  dimnames(bp)[[2]])
r_cvci <- grep("^CVCI$", dimnames(bp)[[1]]); c_cvcp <- grep("^CVCP$", dimnames(bp)[[2]])
b1v <- bp[r_cac, c_cit, ]
b3v <- bp[r_cvci, c_cvcp, ]

idx <- b1v * b6v * b3v
cat(sprintf("\n*** INDEX OF MODERATED MEDIATION = %.4f  [%.4f, %.4f]\n",
            mean(idx), quantile(idx, .025), quantile(idx, .975)))

cond <- do.call(rbind, lapply(c(-1, 0, 1), function(g) {
  e <- b1v * (b2v + b6v * g) * b3v
  data.frame(CGQ_level = c("-1 SD","mean","+1 SD")[match(g, c(-1,0,1))],
             effect = mean(e),
             lo = quantile(e, .025, names = FALSE),
             hi = quantile(e, .975, names = FALSE),
             significant = quantile(e, .025) > 0 | quantile(e, .975) < 0)
}))
cat("\nConditional indirect effect of CAC on CVCP at levels of governance:\n")
print(round(cond[, 2:4], 4)); print(cond$significant)
w(cond, "T19_conditional_indirect_effects.csv")
cat("\nTHEORETICAL CLAIM: the -1 SD effect should NOT be distinguishable from zero.\n")
cat("This is the central empirical quantity in the paper.\n")

## ===========================================================================
## STEP 9  PREDICTIVE ASSESSMENT AND SPECIFICATION COMPARISON
## ===========================================================================

pp <- predict_pls(model = m2, technique = predict_DA, noFolds = 10, reps = 10)
sp <- summary(pp)
print(sp)
w(sp$PLS_out_of_sample, "T16_plspredict_PLS_RMSE.csv")
w(sp$LM_out_of_sample,  "T16_plspredict_LM_RMSE.csv")
cat("\nQ2predict > 0 required for CIT, CVCI, CVCP.\n")
cat("PLS RMSE should be below the LM benchmark for the majority of indicators.\n")

## Prediction-oriented comparison against the two REJECTED specifications.
## This converts the a-priori argument in section 4.3 into an empirical result.
## Do not skip it: it is a distinctive contribution.

# Alternative 1: four-link serial chain (CAC -> CIT -> CGQ -> CVCI -> CVCP)
sm_alt1 <- relationships(
  paths(from = c("CAC", CTRL), to = "CIT"),
  paths(from = "CIT",          to = "CGQ"),
  paths(from = c("CGQ", CTRL), to = "CVCI"),
  paths(from = c("CVCI", CTRL), to = "CVCP")
)
mm_noint <- constructs(
  composite("CAC",  c("CAC_MEA","CAC_COST","CAC_VAL"),   weights = mode_B),
  composite("CVCP", c("CVCP_ECO","CVCP_ENV","CVCP_SOC"), weights = mode_B),
  composite("CIT",  multi_items("CIT",  1:5), weights = mode_A),
  composite("CGQ",  multi_items("CGQ",  1:6), weights = mode_A),
  composite("CVCI", multi_items("CVCI", 1:6), weights = mode_A),
  composite("DTC",  multi_items("DTC",  1:3), weights = mode_A),
  composite("IS",   multi_items("IS",   1:3), weights = mode_A),
  composite("SIZE_ln", single_item("SIZE_ln")), composite("AGE_ln", single_item("AGE_ln")),
  composite("VOL_ln",  single_item("VOL_ln")), composite("EDU",    single_item("EDU")),
  composite("AFF",     single_item("AFF"))
)
m_alt1 <- estimate_pls(df2, mm_noint, sm_alt1, inner_weights = path_weighting)

# Alternative 2: parallel capabilities, transparency omitted
sm_alt2 <- relationships(
  paths(from = c("CAC","CGQ", CTRL), to = "CVCI"),
  paths(from = c("CVCI", CTRL),      to = "CVCP")
)
m_alt2 <- estimate_pls(df2, mm_noint, sm_alt2, inner_weights = path_weighting)

spec <- data.frame(
  model = c("Adopted (3-link + interaction)", "Alt 1 (4-link serial)",
            "Alt 2 (parallel capabilities)"),
  R2_CVCI = c(s2$paths["R^2","CVCI"], summary(m_alt1)$paths["R^2","CVCI"],
              summary(m_alt2)$paths["R^2","CVCI"]),
  R2_CVCP = c(s2$paths["R^2","CVCP"], summary(m_alt1)$paths["R^2","CVCP"],
              summary(m_alt2)$paths["R^2","CVCP"]))
print(spec); w(spec, "T20_specification_comparison.csv")
cat("\nAdd Q2predict and CVPAT per model to complete Table 20.\n")

## ===========================================================================
## STEP 10  MULTI-GROUP ANALYSIS
## ===========================================================================
## Establish measurement invariance (MICOM) FIRST. An MGA reported without
## MICOM will be challenged. seminr's MICOM is less complete than SmartPLS's:
## run this step in SmartPLS and state which software produced which result.
##
## DO NOT run the producer-vs-processor comparison: with ~70 processors it
## needs beta >= 0.30 to be detectable. The manuscript states it will not be
## conducted and why. Honour that.

if (nrow(df2) >= 350) {
  for (g in list(list(v = "AFF",  cond = df2$AFF == 1,      lbl = "PO member vs not"),
                 list(v = "SIZE", cond = df2$SIZE_ln > median(df2$SIZE_ln),
                      lbl = "large vs small"))) {
    if (min(sum(g$cond), sum(!g$cond)) >= 100) {
      cat(sprintf("\n--- MGA: %s (n = %d / %d) ---\n", g$lbl,
                  sum(g$cond), sum(!g$cond)))
      try(print(summary(estimate_pls_mga(m2, condition = g$cond))))
    } else {
      cat(sprintf("\nSkipping MGA %s: smallest group n = %d (< 100)\n",
                  g$lbl, min(sum(g$cond), sum(!g$cond))))
    }
  }
} else cat("\nn < 350: MGA under-powered. Report the reason rather than omitting silently.\n")

## ===========================================================================
## STEP 11  ROBUSTNESS BATTERY
## ===========================================================================

focal_of <- function(m) {
  p <- summary(m)$paths
  c(CIT_CVCI = p["CIT","CVCI"], INT_CVCI = p["CIT*CGQ","CVCI"],
    CAC_CIT = p["CAC","CIT"], CVCI_CVCP = p["CVCI","CVCP"],
    CIT_CVCP = p["CIT","CVCP"])
}
refit <- function(d, label) {
  out <- try(focal_of(estimate_pls(d, mm2, sm2, inner_weights = path_weighting)),
             silent = TRUE)
  if (inherits(out, "try-error")) return(setNames(rep(NA, 5), names(focal_of(m2))))
  cat(sprintf("  %-42s done\n", label)); out
}

cat("\n--- Robustness battery ---\n")
rb <- rbind(
  `0 Baseline`                          = focal_of(m2),
  `1 Excl. multivariate outliers`       = refit(df2[!df2$FLAG_OUTLIER, ], "excl outliers"),
  `2 Excl. longstring + fast`           = refit(df2[!(df2$FLAG_LONGSTRING | df2$FLAG_FAST), ], "excl careless"),
  `6 MLMV marker-corrected`             = c(summary(m2m)$paths["CIT","CVCI"],
                                            summary(m2m)$paths["CIT*CGQ","CVCI"],
                                            summary(m2m)$paths["CAC","CIT"],
                                            summary(m2m)$paths["CVCI","CVCP"],
                                            summary(m2m)$paths["CIT","CVCP"])
)
# check 4: drop the controls
sm_noctrl <- relationships(
  paths(from = "CAC",                          to = "CIT"),
  paths(from = c("CIT","CAC","CGQ","CIT*CGQ"), to = "CVCI"),
  paths(from = c("CVCI","CIT"),                to = "CVCP"))
rb <- rbind(rb, `4 No controls` =
  focal_of(estimate_pls(df2, mm2, sm_noctrl, inner_weights = path_weighting)))

# check 7: CVCP as three separate outcomes (dimensional asymmetry)
mm_dim <- append(mm2, constructs(
  composite("ECO", single_item("CVCP_ECO")),
  composite("ENV", single_item("CVCP_ENV")),
  composite("SOC", single_item("CVCP_SOC"))))
sm_dim <- relationships(
  paths(from = c("CAC", CTRL),                       to = "CIT"),
  paths(from = c("CIT","CAC","CGQ","CIT*CGQ", CTRL), to = "CVCI"),
  paths(from = c("CVCI","CIT", CTRL),                to = c("ECO","ENV","SOC")))
m_dim <- estimate_pls(df2, mm_dim, sm_dim, inner_weights = path_weighting)
cat("\nCheck 7 - CVCI -> each CVCP dimension separately:\n")
print(round(summary(m_dim)$paths["CVCI", c("ECO","ENV","SOC")], 4))
cat("If SOC is markedly weaker, that is a FINDING about who captures circular\n")
cat("value, not a measurement failure. See Table A13.\n")

# check 8: product-indicator interaction instead of two-stage
mm_pi <- constructs(
  composite("CAC",  c("CAC_MEA","CAC_COST","CAC_VAL"),   weights = mode_B),
  composite("CVCP", c("CVCP_ECO","CVCP_ENV","CVCP_SOC"), weights = mode_B),
  composite("CIT",  multi_items("CIT",  1:5), weights = mode_A),
  composite("CGQ",  multi_items("CGQ",  1:6), weights = mode_A),
  composite("CVCI", multi_items("CVCI", 1:6), weights = mode_A),
  composite("DTC",  multi_items("DTC",  1:3), weights = mode_A),
  composite("IS",   multi_items("IS",   1:3), weights = mode_A),
  composite("SIZE_ln", single_item("SIZE_ln")), composite("AGE_ln", single_item("AGE_ln")),
  composite("VOL_ln",  single_item("VOL_ln")), composite("EDU",    single_item("EDU")),
  composite("AFF",     single_item("AFF")),
  interaction_term(iv = "CIT", moderator = "CGQ", method = product_indicator))
rb <- rbind(rb, `8 Product-indicator interaction` =
  focal_of(estimate_pls(df2, mm_pi, sm2, inner_weights = path_weighting)))

# check 9: consistent PLS
rb <- rbind(rb, `9 PLSc` = tryCatch(
  focal_of(estimate_pls(df2, mm2, sm2, inner_weights = path_weighting,
                        measurement_mode = NULL)),
  error = function(e) setNames(rep(NA, 5), colnames(rb))))

print(round(rb, 4)); w(round(rb, 4), "T22_robustness_battery.csv")
cat("\nIf any check reverses a conclusion it belongs in the MAIN TEXT,\n")
cat("not the supplement.\n")

# check 11: enumerator effects
if ("ENUM" %in% names(df2)) {
  cat("\nEnumerator ICC by construct (high values -> report and control):\n")
  for (v in c("CAC","CIT","CGQ","CVCI","CVCP")) {
    a <- anova(lm(cs[[v]] ~ factor(df2$ENUM)))
    cat(sprintf("  %-5s eta2 = %.3f  p = %.4f\n", v,
                a[1,2]/sum(a[,2]), a[1,5]))
  }
}

## ===========================================================================
## ENDOGENEITY: GAUSSIAN COPULA
## ===========================================================================
## Valid ONLY if the suspected endogenous regressor is non-normal. Test first.
cop <- function(x) qnorm(stats::ecdf(x)(x) * (length(x) - 1) / length(x))
for (v in c("CAC","CIT","CVCI")) {
  kt <- ks.test(scale(cs[[v]]), "pnorm")
  cat(sprintf("\n%s: KS p = %.4f %s\n", v, kt$p.value,
      ifelse(kt$p.value < 0.05, "(non-normal: copula valid)",
             "(normal: copula NOT valid, do not use)")))
}
cs$c_CIT <- cop(cs$CIT)
cat("\nCopula-augmented regression for CVCI (copula term should be ns):\n")
print(summary(lm(CVCI ~ CIT + CAC + CGQ + c_CIT, data = cs))$coefficients)

cat("\n\n=== Done. Outputs in ./results ===\n")
cat("Remaining in SmartPLS: MICOM + permutation MGA (step 10), CVPAT,\n")
cat("and the CB-SEM check on the reflective portion (protocol section 11).\n")
