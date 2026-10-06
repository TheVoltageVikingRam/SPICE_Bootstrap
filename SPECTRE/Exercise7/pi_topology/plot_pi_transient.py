#!/usr/bin/env python3
"""
Plot transient V(in) and V(out) waveforms for pi-topology RC transmission line.

Reads the Virtuoso VCSV export from csv_files/ containing V(in) once and
V(out) for N=1..10 (exported in order from Virtuoso).

Generates a single publication-quality plot showing V(in) and all 10 V(out)
traces, saved into images/.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import MultipleLocator

# ─── Parse VCSV ─────────────────────────────────────────────────────────────────

def parse_vcsv(filepath, n_traces=11):
    """
    Parse a Virtuoso CSV (.vcsv) file.

    The file has 6 header lines, then data rows with 2*n_traces columns:
        t0, V0, t1, V1, ..., t10, V10

    Each trace has its own time axis (from separate Spectre runs).
    Empty/whitespace-only fields are skipped.

    Returns a list of n_traces elements, each a dict with 'time' and 'voltage'
    numpy arrays.
    """
    traces = [{'time': [], 'voltage': []} for _ in range(n_traces)]

    with open(filepath, 'r') as f:
        for _ in range(6):          # skip header
            next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            for i in range(n_traces):
                t_idx = 2 * i
                v_idx = 2 * i + 1
                if t_idx < len(parts) and v_idx < len(parts):
                    t_str = parts[t_idx].strip()
                    v_str = parts[v_idx].strip()
                    if t_str and v_str:
                        try:
                            traces[i]['time'].append(float(t_str))
                            traces[i]['voltage'].append(float(v_str))
                        except ValueError:
                            pass

    for tr in traces:
        tr['time'] = np.array(tr['time'])
        tr['voltage'] = np.array(tr['voltage'])

    return traces


# ─── Configuration ──────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR    = os.path.join(SCRIPT_DIR, 'csv_files')
IMG_DIR    = os.path.join(SCRIPT_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

# Use the 63.2% file (waveform is the same; threshold only affects measurement)
VCSV_FILE = os.path.join(CSV_DIR, 'csv_plot_in_vs_out_vth_63_2percent_vdd.vcsv')

VDD = 0.8   # V

# ─── Parse ──────────────────────────────────────────────────────────────────────

print("Parsing VCSV file ...")
traces = parse_vcsv(VCSV_FILE)
print(f"  V(in): {len(traces[0]['time'])} points")
for i in range(1, 11):
    print(f"  V(out) N={i}: {len(traces[i]['time'])} points")

# ─── Plot style ─────────────────────────────────────────────────────────────────

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 15,
    'axes.labelsize': 13,
    'legend.fontsize': 9,
    'figure.dpi': 200,
    'savefig.dpi': 300,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linestyle': ':',
})

# ─── Color map for N=1..10 ──────────────────────────────────────────────────────

# Use a perceptually distinct colormap
cmap = cm.get_cmap('tab10', 10)

# ═══════════════════════════════════════════════════════════════════════════════
# Transient waveform plot — zoom into first 100 ps (the interesting part)
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(10, 6.5))

# --- Plot V(in) ---
t_in = traces[0]['time'] * 1e12          # convert to ps
v_in = traces[0]['voltage']
mask_in = t_in <= 100
ax.plot(t_in[mask_in], v_in[mask_in],
        color='black', linewidth=2.2, linestyle='-',
        label='V(in)', zorder=12)

# --- Plot V(out) for N=1..10 ---
line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--']
markers     = ['o', 's', '^', 'D', 'v', 'p', 'h', '*', 'X', 'P']

for i in range(1, 11):
    t_out = traces[i]['time'] * 1e12
    v_out = traces[i]['voltage']
    mask = t_out <= 100

    # Subsample markers so they don't overlap
    t_masked = t_out[mask]
    v_masked = v_out[mask]

    ax.plot(t_masked, v_masked,
            color=cmap(i - 1),
            linewidth=1.4,
            linestyle=line_styles[(i - 1) % len(line_styles)],
            marker=markers[(i - 1) % len(markers)],
            markevery=max(1, len(t_masked) // 12),
            markersize=5,
            alpha=0.85,
            label=f'V(out)  N={i}',
            zorder=10 - i)

# --- Threshold reference lines ---
ax.axhline(0.632 * VDD, color='dodgerblue', linestyle='--', linewidth=1.2,
           alpha=0.7, label=f'0.632 VDD = {0.632*VDD:.4f} V')
ax.axhline(0.5 * VDD, color='darkorange', linestyle='--', linewidth=1.2,
           alpha=0.7, label=f'0.5 VDD = {0.5*VDD:.1f} V')

# --- Theoretical RC step response: Vs(1 - e^(-t/tau)), tau = RC/2 = 50 ps ---
tau = 50.0   # ps  (Elmore delay = RC/2)
t_theory = np.linspace(0, 100, 500)  # ps
v_theory = VDD * (1.0 - np.exp(-t_theory / tau))
ax.plot(t_theory, v_theory,
        color='#2ca02c', linewidth=2.5, linestyle='-',
        marker='d', markersize=5, markevery=40,
        alpha=0.9, zorder=11,
        label=r'$V_s(1 - e^{-t/\tau})$,  $\tau = RC/2 = 50$ ps')

# --- Axis formatting ---
ax.set_xlabel('Time  (ps)')
ax.set_ylabel('Voltage  (V)')
ax.set_title(r'Transient Simulation for $\pi$-Segment TX-Line  (N = 1 ... 10)')
ax.set_xlim(0, 100)
ax.set_ylim(-0.02, VDD + 0.05)
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(0.1))

# Legend outside bottom or inside with small font
ax.legend(loc='center right', fontsize=8.5, framealpha=0.92,
          ncol=1, borderpad=0.6)

fig.tight_layout()
outpath = os.path.join(IMG_DIR, 'pi_transient_vin_vout_N1_to_N10.png')
fig.savefig(outpath, bbox_inches='tight')
print(f"\nSaved: {outpath}")

plt.close('all')
print("Done -- pi transient plot generated.")
