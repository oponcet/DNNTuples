import ROOT
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------
# input files
# -------------------------------------------------

file_WL = "/uscms_data/d3/oponcet1/VBS/CMSSW_15_0_10/src/DeepNTuples/Ntupler/test/output_WL_numEvent1000.root"
file_WT = "/uscms_data/d3/oponcet1/VBS/CMSSW_15_0_10/src/DeepNTuples/Ntupler/test/output_WT_numEvent1000.root"

# -------------------------------------------------
# load ROOT trees
# -------------------------------------------------

df_WL = ROOT.RDataFrame("deepntuplizer/tree", file_WL)
df_WT = ROOT.RDataFrame("deepntuplizer/tree", file_WT)

# load variables
vars_to_load = ["fj_ptheta", "fj_zj"]

arr_WL = df_WL.AsNumpy(vars_to_load)
arr_WT = df_WT.AsNumpy(vars_to_load)

# convert to numpy
wl_ptheta = np.array(arr_WL["fj_ptheta"])
wt_ptheta = np.array(arr_WT["fj_ptheta"])

wl_zj = np.array(arr_WL["fj_zj"])
wt_zj = np.array(arr_WT["fj_zj"])

# -------------------------------------------------
# cleaning
# -------------------------------------------------

def clean(arr):
    arr = arr[np.isfinite(arr)]
    arr = arr[(arr >= 0) & (arr <= 1)]
    return arr

wl_ptheta = clean(wl_ptheta)
wt_ptheta = clean(wt_ptheta)

wl_zj = clean(wl_zj)
wt_zj = clean(wt_zj)

# -------------------------------------------------
# helper function
# -------------------------------------------------

def make_histograms(var_wl, var_wt, bins=50, range_=(0,1)):

    counts_wl, edges = np.histogram(
        var_wl,
        bins=bins,
        range=range_
    )

    counts_wt, _ = np.histogram(
        var_wt,
        bins=bins,
        range=range_
    )

    Nwl = np.sum(counts_wl)
    Nwt = np.sum(counts_wt)

    # normalized histograms
    h_wl = counts_wl / Nwl
    h_wt = counts_wt / Nwt

    # poisson uncertainties
    err_wl = np.sqrt(counts_wl) / Nwl
    err_wt = np.sqrt(counts_wt) / Nwt

    # ratio
    ratio = np.divide(
        h_wl,
        h_wt,
        out=np.zeros_like(h_wl, dtype=float),
        where=h_wt != 0
    )

    # ratio uncertainty
    err_ratio = np.zeros_like(ratio)

    mask = (h_wl > 0) & (h_wt > 0)

    err_ratio[mask] = ratio[mask] * np.sqrt(
        (err_wl[mask] / h_wl[mask])**2 +
        (err_wt[mask] / h_wt[mask])**2
    )

    centers = 0.5 * (edges[:-1] + edges[1:])
    bin_width = edges[1] - edges[0]

    return (
        centers,
        bin_width,
        h_wl,
        h_wt,
        err_wl,
        err_wt,
        ratio,
        err_ratio
    )

# -------------------------------------------------
# plotting function
# -------------------------------------------------

def make_plot(
    variable_name,
    xlabel,
    var_wl,
    var_wt
):

    (
        centers,
        bin_width,
        h_wl,
        h_wt,
        err_wl,
        err_wt,
        ratio,
        err_ratio
    ) = make_histograms(var_wl, var_wt)

    # -------------------------------------------------
    # figure
    # -------------------------------------------------

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(7,6),
        sharex=True,
        gridspec_kw={"height_ratios":[3,1]}
    )

    # -------------------------------------------------
    # upper panel
    # -------------------------------------------------

    ax1.fill_between(
        centers,
        h_wl,
        step="mid",
        alpha=0.35,
        color="dodgerblue"
    )

    ax1.fill_between(
        centers,
        h_wt,
        step="mid",
        alpha=0.30,
        color="mediumpurple"
    )

    ax1.step(
        centers,
        h_wl,
        where="mid",
        linewidth=1.8,
        color="dodgerblue",
        label=r"$W_L$"
    )

    ax1.step(
        centers,
        h_wt,
        where="mid",
        linewidth=1.8,
        color="mediumpurple",
        label=r"$W_T$"
    )

    # uncertainties
    ax1.errorbar(
        centers,
        h_wl,
        yerr=err_wl,
        xerr=bin_width/2,
        fmt="none",
        ecolor="dodgerblue",
        linewidth=1
    )

    ax1.errorbar(
        centers,
        h_wt,
        yerr=err_wt,
        xerr=bin_width/2,
        fmt="none",
        ecolor="mediumpurple",
        linewidth=1
    )

    # cosmetics
    ax1.set_ylabel(
        "Normalized events",
        fontsize=13
    )

    ax1.set_ylim(bottom=0)

    ax1.legend(
        frameon=False,
        fontsize=12,
        loc="upper right"
    )

    ax1.grid(alpha=0.25)

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
        xerr=bin_width/2,
        fmt="o",
        markersize=4,
        color="black",
        linewidth=1
    )

    ax2.set_xlabel(
        xlabel,
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
        f"{variable_name}_WL_vs_WT_ratio.png",
        dpi=250
    )

    plt.close()

# -------------------------------------------------
# make plots
# -------------------------------------------------

make_plot(
    variable_name="ptheta",
    xlabel=r"$p_{\theta}$",
    var_wl=wl_ptheta,
    var_wt=wt_ptheta
)

make_plot(
    variable_name="zj",
    xlabel=r"$z_j$",
    var_wl=wl_zj,
    var_wt=wt_zj
)

print("Plots saved:")
print(" - ptheta_WL_vs_WT_ratio.png")
print(" - zj_WL_vs_WT_ratio.png")