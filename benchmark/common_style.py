"""Shared plotting style for all benchmark analysis notebooks.

This module is the single source of truth for the paper figures. Every
notebook (spmv, krylov, stream) imports it so that the exported PDFs share the
same font, palette, sizes, and layout conventions.

Geometry targets the acmart ``sigconf`` double-column layout:
    * single column  ~3.35 in (241 pt)
    * full text width ~7.0 in (506 pt)
"""

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# --- Layout geometry (acmart sigconf) ---------------------------------------
COLW = 3.35      # single-column figure width (inches)
TEXTW = 7.0      # full text width for figure* (inches)

# --- Colorblind-safe palette (Okabe-Ito) -------------------------------------
NATIVE = "#009E73"  # green
SME = "#0072B2"     # blue
SEV = "#D55E00"     # vermillion

MODE_PALETTE = {"Native": NATIVE, "SME": SME, "SME+SEV": SEV}
MODE_PALETTE_2 = {"SME": SME, "SME+SEV": SEV}
MODE_ORDER = ["Native", "SME", "SME+SEV"]
MODE_ORDER_2 = ["SME", "SME+SEV"]


def apply_style():
    """Apply the shared style once at the top of each notebook."""
    sns.set_theme(style="white", font="TeX Gyre Pagella")
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["TeX Gyre Pagella"],
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "figure.constrained_layout.use": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e0e0e0",
        "grid.linewidth": 0.4,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def remove_legend(ax):
    """Remove an axes-level legend if one exists (seaborn skips it when hue == y)."""
    leg = ax.get_legend()
    if leg is not None:
        leg.remove()


def top_legend(fig, ax, ncol=None, anchor=(0.5, 1.0), loc="lower center"):
    """Move an axes-level legend to a single shared legend above the figure."""
    handles, labels = ax.get_legend_handles_labels()
    remove_legend(ax)
    if ncol is None:
        ncol = len(labels)
    return fig.legend(
        handles,
        labels,
        loc=loc,
        ncol=ncol,
        bbox_to_anchor=anchor,
        frameon=False,
    )


def zero_line(ax, color="#999999", lw=0.7, zorder=0):
    """Add a dashed zero reference line to an axis."""
    return ax.axhline(0, color=color, linewidth=lw, linestyle="--", zorder=zorder)
