#!/usr/bin/env python3
"""
Plot propagation delay vs. N for the T-topology RC transmission-line model.

Reads Spectre measurement text files from text_files/ and produces plots
saved into images/.

Data files:
  - measurements_tpd_when_VTH_63percent_VDD.txt  (threshold = 0.632 VDD)
  - measurements_tpd_when_VTH_50percent_VDD.txt  (threshold = 0.5   VDD)

Theoretical references:
  - Elmore delay  RC/2 = 50 ps                    (for 0.632 VDD)
  - 0.693 × RC/2 = 34.66 ps                       (for 0.5   VDD, lumped)
"""

import re
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ─── Helpers ────────────────────────────────────────────────────────────────────

def parse_spectre_measurements(filepath):
    """
    Parse a Spectre measurement text file and return a dict {N: tpd_ps}.
    """
    data = {}
    current_n = None
    dir_pattern = re.compile(r'_N(\d+)\.raw')
    tpd_pattern = re.compile(r'tpd\s+=\s+([\d.eE+\-]+)')

    with open(filepath, 'r') as f:
        for line in f:
            m_dir = dir_pattern.search(line)
            if m_dir:
                current_n = int(m_dir.group(1))

            m_tpd = tpd_pattern.search(line)
            if m_tpd and current_n is not None:
                tpd_seconds = float(m_tpd.group(1))
                tpd_ps = tpd_seconds * 1e12
                data[current_n] = tpd_ps
                current_n = None

    return data


def sorted_data(data_dict):
    """Return sorted (N_array, tpd_array) from a {N: tpd} dict."""
    ns = sorted(data_dict.keys())
    return np.array(ns), np.array([data_dict[n] for n in ns])


# ─── Configuration ──────────────────────────────────────────────────────────────

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR     = os.path.join(SCRIPT_DIR, 'text_files')
IMG_DIR      = os.path.join(SCRIPT_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

FILE_63  = os.path.join(TEXT_DIR, 'measurements_tpd_when_VTH_63percent_VDD.txt')
FILE_50  = os.path.join(TEXT_DIR, 'measurements_tpd_when_VTH_50percent_VDD.txt')

# Theoretical constants
RC       = 100.0    # ps
ELMORE   = RC / 2   # 50 ps
LUMPED_50 = 0.6931 * ELMORE  # ≈ 34.66 ps

# ─── Parse data ─────────────────────────────────────────────────────────────────

data_63 = parse_spectre_measurements(FILE_63)
data_50 = parse_spectre_measurements(FILE_50)

N_63, tpd_63 = sorted_data(data_63)
N_50, tpd_50 = sorted_data(data_50)

# ─── Plot style setup ──────────────────────────────────────────────────────────

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'legend.fontsize': 10.5,
    'figure.dpi': 200,
    'savefig.dpi': 300,
    'axes.grid': True,
    'grid.alpha': 0.35,
    'grid.linestyle': '--',
})

COLORS = {
    '63':       '#1b9e77',   # teal
    '50':       '#d95f02',   # orange
    'elmore':   '#7570b3',   # purple
    'lumped50': '#e7298a',   # magenta
}

# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 1 — T-model delay at 0.632 VDD
# ═══════════════════════════════════════════════════════════════════════════════

fig1, ax1 = plt.subplots(figsize=(8, 5))

ax1.plot(N_63, tpd_63, 'o-', color=COLORS['63'], linewidth=2, markersize=7,
         label=r'T-model  $t_{pd}$ @ 0.632 $V_{DD}$')
ax1.axhline(ELMORE, color=COLORS['elmore'], linestyle='--', linewidth=1.5,
            label=f'Elmore delay  RC/2 = {ELMORE:.0f} ps')

for n, t in zip(N_63, tpd_63):
    ax1.annotate(f'{t:.2f}', (n, t), textcoords='offset points',
                 xytext=(0, 10), ha='center', fontsize=8, color=COLORS['63'])

ax1.set_xlabel('Number of sections  N')
ax1.set_ylabel('Propagation delay  $t_{pd}$  (ps)')
ax1.set_title(r'T-Model :  Propagation Delay vs N  (threshold = 0.632 $V_{DD}$)')
ax1.set_xticks(N_63)
ax1.set_xlim(0.5, 10.5)
ax1.set_ylim(48.5, 51.0)
ax1.xaxis.set_minor_locator(MultipleLocator(1))
ax1.legend(loc='upper right', framealpha=0.9)

fig1.tight_layout()
fig1.savefig(os.path.join(IMG_DIR, 'T_tpd_vs_N_632VDD.png'))
print(f"Saved: {os.path.join(IMG_DIR, 'T_tpd_vs_N_632VDD.png')}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 2 — T-model delay at 0.5 VDD
# ═══════════════════════════════════════════════════════════════════════════════

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.plot(N_50, tpd_50, 's-', color=COLORS['50'], linewidth=2, markersize=7,
         label=r'T-model  $t_{pd}$ @ 0.5 $V_{DD}$')
ax2.axhline(LUMPED_50, color=COLORS['lumped50'], linestyle='--', linewidth=1.5,
            label=f'Lumped RC prediction  0.693·RC/2 = {LUMPED_50:.2f} ps')

for n, t in zip(N_50, tpd_50):
    ax2.annotate(f'{t:.2f}', (n, t), textcoords='offset points',
                 xytext=(0, 10), ha='center', fontsize=8, color=COLORS['50'])

ax2.set_xlabel('Number of sections  N')
ax2.set_ylabel('Propagation delay  $t_{pd}$  (ps)')
ax2.set_title(r'T-Model :  Propagation Delay vs N  (threshold = 0.5 $V_{DD}$)')
ax2.set_xticks(N_50)
ax2.set_xlim(0.5, 10.5)
ax2.set_ylim(33.5, 39.0)
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.legend(loc='lower right', framealpha=0.9)

fig2.tight_layout()
fig2.savefig(os.path.join(IMG_DIR, 'T_tpd_vs_N_50VDD.png'))
print(f"Saved: {os.path.join(IMG_DIR, 'T_tpd_vs_N_50VDD.png')}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 3 — T-model: both thresholds combined
# ═══════════════════════════════════════════════════════════════════════════════

fig3, ax3 = plt.subplots(figsize=(9, 5.5))

ax3.plot(N_63, tpd_63, 'o-', color=COLORS['63'], linewidth=2, markersize=7,
         label=r'T-model @ 0.632 $V_{DD}$')
ax3.plot(N_50, tpd_50, 's-', color=COLORS['50'], linewidth=2, markersize=7,
         label=r'T-model @ 0.5 $V_{DD}$')

ax3.axhline(ELMORE, color=COLORS['elmore'], linestyle='--', linewidth=1.5,
            label=f'Elmore (RC/2) = {ELMORE:.0f} ps')
ax3.axhline(LUMPED_50, color=COLORS['lumped50'], linestyle=':', linewidth=1.5,
            label=f'0.693·RC/2 = {LUMPED_50:.2f} ps')

ax3.set_xlabel('Number of sections  N')
ax3.set_ylabel('Propagation delay  $t_{pd}$  (ps)')
ax3.set_title(r'T-Model :  Propagation Delay vs N  (both thresholds)')
ax3.set_xticks(range(1, 11))
ax3.set_xlim(0.5, 10.5)
ax3.set_ylim(33.0, 52.0)
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.legend(loc='center right', framealpha=0.9)

fig3.tight_layout()
fig3.savefig(os.path.join(IMG_DIR, 'T_tpd_vs_N_both_thresholds.png'))
print(f"Saved: {os.path.join(IMG_DIR, 'T_tpd_vs_N_both_thresholds.png')}")

plt.close('all')
print("\nDone — all T-topology plots saved to images/")
