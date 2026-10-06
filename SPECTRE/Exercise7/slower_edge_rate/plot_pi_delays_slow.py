#!/usr/bin/env python3
"""
Plot propagation delay vs. N for the π-topology RC transmission-line model (slow edge).

Reads Spectre measurement text files and produces a plot saved into images/.

Data files:
  - pi_based_slower_edge_63_2vdd_400ps_tr.txt   (threshold = 0.632 VDD)
  - pi_based_slower_edge_50vdd_400ps_tr.txt (threshold = 0.5   VDD)
"""

import re
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def parse_spectre_measurements(filepath):
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
                tpd_ps = tpd_seconds * 1e12          # convert to ps
                data[current_n] = tpd_ps
                current_n = None

    return data

def sorted_data(data_dict):
    ns = sorted(data_dict.keys())
    return np.array(ns), np.array([data_dict[n] for n in ns])

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
IMG_DIR      = os.path.join(SCRIPT_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

FILE_63  = os.path.join(SCRIPT_DIR, 'pi_based_slower_edge_63_2vdd_400ps_tr.txt')
FILE_50  = os.path.join(SCRIPT_DIR, 'pi_based_slower_edge_50vdd_400ps_tr.txt')

RC       = 100.0    # ps
ELMORE   = RC / 2   # 50 ps

data_63 = parse_spectre_measurements(FILE_63)
data_50 = parse_spectre_measurements(FILE_50)

N_63, tpd_63 = sorted_data(data_63)
N_50, tpd_50 = sorted_data(data_50)

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
    '63':       '#1b9e77',
    '50':       '#d95f02',
    'elmore':   '#7570b3',
}

fig, ax = plt.subplots(figsize=(9, 5.5))

ax.plot(N_63, tpd_63, 'o-', color=COLORS['63'], linewidth=2, markersize=8,
         label=r'$\pi$-model @ 0.632 $V_{DD}$')
ax.plot(N_50, tpd_50, 'x--', color=COLORS['50'], linewidth=2, markersize=8,
         label=r'$\pi$-model @ 0.5 $V_{DD}$')

ax.axhline(ELMORE, color=COLORS['elmore'], linestyle='--', linewidth=1.5,
            label=f'Elmore (RC/2) = {ELMORE:.0f} ps')

ax.set_xlabel('Number of sections  N')
ax.set_ylabel('Propagation delay  $t_{pd}$  (ps)')
ax.set_title(r'$\pi$-Model : Propagation Delay vs N (Slow Edge $t_r=400$ps)')
ax.set_xticks(range(1, 11))
ax.set_xlim(0.5, 10.5)

ax.set_ylim(49.0, 50.5)

ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.legend(loc='lower right', framealpha=0.9)

fig.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'pi_tpd_vs_N_slow_edge.png'))
print(f"Saved: {os.path.join(IMG_DIR, 'pi_tpd_vs_N_slow_edge.png')}")

plt.close('all')
print("\nDone -- pi-topology slow edge plot saved to images/")
