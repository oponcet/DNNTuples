import ROOT
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------
# input files
# -------------------------------------------------

file_WL = "/uscms_data/d3/oponcet1/VBS/CMSSW_15_0_10/src/DeepNTuples/Ntupler/test/output_WL_numEvent10000.root"
file_WT = "/uscms_data/d3/oponcet1/VBS/CMSSW_15_0_10/src/DeepNTuples/Ntupler/test/output_WT_numEvent10000.root"

# -------------------------------------------------
# load ROOT trees
# -------------------------------------------------

df_WL = ROOT.RDataFrame("deepntuplizer/tree", file_WL)
df_WT = ROOT.RDataFrame("deepntuplizer/tree", file_WT)

wl = np.array(df_WL.AsNumpy(["fj_ptheta"])["fj_ptheta"])
wt = np.array(df_WT.AsNumpy(["fj_ptheta"])["fj_ptheta"])

# -------------------------------------------------
# cleaning
# -------------------------------------------------

wl = wl[np.isfinite(wl)]
wt = wt[np.isfinite(wt)]

wl = wl[(wl >= 0) & (wl <= 1)]
wt = wt[(wt >= 0) & (wt <= 1)]

# -------------------------------------------------
# histograms
# -------------------------------------------------

bins = 50
range_ = (0, 1)

counts_wl, edges = np.histogram(
    wl,
    bins=bins,
    range=range_
)

counts_wt, _ = np.histogram(
    wt,
    bins=bins,
    range=range_
)

# total events
Nwl = np.sum(counts_wl)
Nwt = np.sum(counts_wt)

# normalized histograms
h_wl = counts_wl / Nwl
h_wt = counts_wt / Nwt

# poisson uncertainties
err_wl = np.sqrt(counts_wl) / Nwl
err_wt = np.sqrt(counts_wt) / Nwt

# -------------------------------------------------
# ratio WL / WT
# -------------------------------------------------

ratio = np.divide(
    h_wl,
    h_wt,
    out=np.zeros_like(h_wl, dtype=float),
    where=h_wt != 0
)

# uncertainty propagation
err_ratio = np.zeros_like(ratio)

mask = (h_wl > 0) & (h_wt > 0)

err_ratio[mask] = ratio[mask] * np.sqrt(
    (err_wl[mask] / h_wl[mask])**2 +
    (err_wt[mask] / h_wt[mask])**2
)

# -------------------------------------------------
# binning
# -------------------------------------------------

centers = 0.5 * (edges[:-1] + edges[1:])
bin_width = edges[1] - edges[0]

# -------------------------------------------------
# figure
# -------------------------------------------------

fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]}
)

# -------------------------------------------------
# upper panel
# -------------------------------------------------

# filled histograms
ax1.fill_between(
    centers,
    h_wl,
    step="mid",
    alpha=0.35,
    color="skyblue"
)

ax1.fill_between(
    centers,
    h_wt,
    step="mid",
    alpha=0.30,
    color="orange"
)

# outlines
ax1.step(
    centers,
    h_wl,
    where="mid",
    linewidth=1.8,
    color="blue",
    label=r"$W_L$"
)

ax1.step(
    centers,
    h_wt,
    where="mid",
    linewidth=1.8,
    color="darkorange",
    label=r"$W_T$"
)

# uncertainties WL
ax1.errorbar(
    centers,
    h_wl,
    yerr=err_wl,
    xerr=bin_width / 2,
    fmt="none",
    ecolor="blue",
    linewidth=1
)

# uncertainties WT
ax1.errorbar(
    centers,
    h_wt,
    yerr=err_wt,
    xerr=bin_width / 2,
    fmt="none",
    ecolor="darkorange",
    linewidth=1
)

# cosmetics
ax1.set_ylabel(
    "Normalized events",
    fontsize=13
)

# remove white space at bottom
ax1.set_ylim(bottom=0)

ax1.legend(
    frameon=False,
    fontsize=12,
    loc="upper right"
)

ax1.grid(alpha=0.25)

# ax1.text(
#     0.02,
#     0.93,
#     r"$\bf{CMS}$ Simulation",
#     transform=ax1.transAxes,
#     fontsize=13
# )

# -------------------------------------------------
# ratio panel
# -------------------------------------------------

ax2.axhline(
    1.0,
    color="black",
    linestyle="--",
    linewidth=1
)

ax2.errorbar(
    centers,
    ratio,
    yerr=err_ratio,
    xerr=bin_width / 2,
    fmt="o",
    markersize=4,
    color="black",
    linewidth=1
)

ax2.set_xlabel(
    r"$p_{\theta}$",
    fontsize=14
)

ax2.set_ylabel(
    "WL/WT",
    fontsize=11
)

ax2.set_ylim(0, 2)

ax2.grid(alpha=0.25)

# ticks
ax1.tick_params(
    direction="in",
    top=True,
    right=True
)

ax2.tick_params(
    direction="in",
    top=True,
    right=True
)

# -------------------------------------------------

plt.tight_layout()

plt.savefig(
    "ptheta_WL_vs_WT_ratio.png",
    dpi=250
)

