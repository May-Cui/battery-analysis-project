from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy import interpolate

# Define standard column aliases
T = 'Test_Time(s)'
I = 'Current(A)'
Qc = 'Charge_Capacity(Ah)'
Qd = 'Discharge_Capacity(Ah)'
V = 'Voltage_sm (V)'
dqdv = 'dQ/dV (computed from preprocessed V) (Ah/V)'
dvdq = 'dV/dQ (computed from preprocessed V) (V/Ah)'


def build_cycle_file_map(base_path):
    """
    Scan raw folder structure and build a mapping from folder number to .xlsx file path.

    Parameters:
        base_path (Path): Path to the raw dataset directory (e.g. '03-CONSTANT CURRENT protocol_Cycles 0 to 1000')

    Returns:
        dict[int, Path]: Mapping from folder number (e.g. 0, 1, 2...) to its .xlsx file path.
    """
    cycle_file_map = {}

    for folder_path in sorted(base_path.glob("Cycle *"), key=lambda p: int(p.name.split()[-1])):
        if folder_path.is_dir():
            folder_no = int(folder_path.name.replace("Cycle ", ""))
            xlsx_files = list(folder_path.glob("*.xlsx"))

            if not xlsx_files:
                print(f"[Warning] No .xlsx file found in {folder_path}")
                continue

            cycle_file_map[folder_no] = xlsx_files[0]

    return cycle_file_map


def read(folder_no, cycle_file_map):
    """
    Read the .xlsx file corresponding to a given folder number.

    Parameters:
        folder_no (int): The numeric folder number (e.g. 0, 1, 2, ...)
        cycle_file_map (dict): Mapping from folder number to file path (from build_cycle_file_map)

    Returns:
        pd.DataFrame: The loaded Excel file as a DataFrame
    """
    if folder_no not in cycle_file_map:
        raise ValueError(f"Folder {folder_no} not found in map.")

    return pd.read_excel(cycle_file_map[folder_no])


def smooth(df, col, window, polyorder, out_col='Voltage_sm (V)'):
    df[out_col] = savgol_filter(df[col], window_length=window, polyorder=polyorder)
    return df

def separate_charge_discharge(cycle_df, cycle_no):
    """
    Separate charge and discharge segments from a cycle dataframe.

    Parameters:
        cycle_df (pd.DataFrame): Raw cycle data
        cycle_no (int): Cycle index (used for warnings)

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (charge_df, discharge_df)
    """
    # Filter charge segment
    charge_df = cycle_df[cycle_df[I] > 0].copy()
    charge_df = charge_df[[I, T, V, Qc, dvdq, dqdv]].dropna(subset=[I, T, V, Qc]).reset_index(drop=True)
    charge_df = charge_df[charge_df[Qc] > 0].reset_index(drop=True)

    # Filter discharge segment
    discharge_df = cycle_df[cycle_df[I] < 0].copy()
    discharge_df = discharge_df[[I, T, V, Qd, dvdq, dqdv]].dropna(subset=[I, T, V, Qd]).reset_index(drop=True)
    discharge_df = discharge_df[discharge_df[Qd] > 0].reset_index(drop=True)

    # Optional warnings
    if charge_df.empty:
        print(f"[Cycle {cycle_no}] Warning: No charge data found.")
    if discharge_df.empty:
        print(f"[Cycle {cycle_no}] Warning: No discharge data found.")

    return charge_df, discharge_df

def separate_valid_cycles(df, folder_no, min_seg_length, min_v_variation):
    """
    Identify valid cycles based on minimum segment length and voltage variation.

    Parameters:
        df (pd.DataFrame): Full dataframe containing multiple cycles
        folder_no (int): Folder number where the data originated
        min_seg_length (int): Minimum number of rows for charge/discharge segment to be valid
        min_v_variation (int): Minimum number of unique voltage values required

    Returns:
        pd.DataFrame: Each row contains 'folder_no', 'cycle_no', 'charge_df', 'discharge_df'
    """
    valid_data = []

    for cycle_no, cycle_df in df.groupby("Cycle_Index"):
        charge_df, discharge_df = separate_charge_discharge(cycle_df, cycle_no)

        if (
            charge_df.empty or discharge_df.empty or
            len(charge_df) < min_seg_length or len(discharge_df) < min_seg_length or
            charge_df[V].nunique() < min_v_variation or discharge_df[V].nunique() < min_v_variation
        ):
            continue

        valid_data.append({
            "folder_no": folder_no,
            "cycle_no": cycle_no,
            "charge_df": charge_df,
            "discharge_df": discharge_df
        })

    return pd.DataFrame(valid_data)

def select_valid_cycle(folder_no, cycle_file_map, min_seg_length, min_v_variation):
    """
    Load one folder, identify valid cycles, and store full dataframe for later use.
    Also prints valid cycle numbers for quick visual reference.

    Parameters:
        folder_no (int): Folder number to load
        min_seg_length (int): Minimum number of points in a valid segment
        min_v_variation (int): Minimum number of unique voltage values

    Returns:
        pd.DataFrame: Raw dataframe from the selected folder
    """
    df = read(folder_no, cycle_file_map)
    valid_df = separate_valid_cycles(df, folder_no, min_seg_length, min_v_variation)

    print(f"[✓] Valid cycles in folder {folder_no}:")
    for c in valid_df['cycle_no'].unique():
        print(f"  - Cycle {c}")

    _last_folder['df'] = df
    _last_folder['folder_no'] = folder_no

    return df


def preprocess_segment(df, q_col, no_points, window, polyorder):
    """
    Interpolate and smooth voltage with respect to capacity.
    Other columns are truncated to shortest shared length.
    """
    x = df[q_col]
    x_shifted = x - x.min()  # starting point for interpolation must be 0

    v, i, t = df[V], df[I], df[T]
    dVdQ, dQdV = df[dvdq], df[dqdv]

    x_shifted, v = map(np.array, (x_shifted, v))
    _, idx = np.unique(x_shifted, return_index=True)
    x_shifted, v = x_shifted[idx], v[idx]

    f_v = interpolate.interp1d(x_shifted, v, kind='cubic', fill_value="extrapolate")
    z = np.linspace(x_shifted.min(), x_shifted.max(), no_points)

    v_interp = f_v(z)

    # Make sure discharge curve is decreasing, charge is increasing
    q_interp = z if q_col == Qc else z[::-1]  # set direction of capacity
    v_interp = v_interp if q_col == Qc else v_interp[::-1]  # accordingly set direction of voltage

    min_len = min(len(q_interp), len(v_interp), len(t), len(i), len(dVdQ), len(dQdV))

    result = pd.DataFrame({
        T: t.tolist()[:min_len],
        I: i.tolist()[:min_len],
        q_col: q_interp[:min_len],
        "Interpolated Voltage (V)": v_interp[:min_len],
        dvdq: dVdQ.tolist()[:min_len],
        dqdv: dQdV.tolist()[:min_len]
    })

    return smooth(result, "Interpolated Voltage (V)", window, polyorder, out_col="Voltage_sm (V)")

def preprocess_single(charge_df, discharge_df, no_points, window, polyorder):
    """
    Preprocess charge/discharge segments for one cycle.
    """
    c = preprocess_segment(charge_df, Qc, no_points, window, polyorder)
    d = preprocess_segment(discharge_df, Qd, no_points, window, polyorder)
    return c, d

def process_all(df, folder_no, min_seg_length, min_v_variation,
                no_points, window, polyorder, type='preprocess'):
    """
    Apply preprocessing or smoothing to all valid cycles in a folder.

    type: 'preprocess', 'smooth', or 'pre_for_integrate'
    """
    processed = []
    valid_df = separate_valid_cycles(df, folder_no, min_seg_length, min_v_variation)

    for _, row in valid_df.iterrows():
        if type == 'preprocess':
            c, d = preprocess_single(row["charge_df"], row["discharge_df"],
                                     no_points, window, polyorder)
        elif type == 'smooth':
            c, d = smooth_single_for_gradient(row["charge_df"], row["discharge_df"],
                                              window, polyorder)
        elif type == 'pre_for_integrate':
            c, d = smooth_single_for_integrate_i(row["charge_df"], row["discharge_df"],
                                                 window, polyorder)
        else:
            raise ValueError(f"Invalid type: {type}")

        processed.append({
            "folder_no": folder_no,
            "cycle_no": row["cycle_no"],
            "df_charge": c,
            "df_discharge": d
        })

    return processed

def _make_title(kind, folder_no, cycle_no, process):
    return f"{kind} from Folder {folder_no}, Cycle {cycle_no} [{process}]"

def _make_label(kind):
    labels = {
        'dqdv_raw': 'Raw dQ/dV (from dataset)',
        'dvdq_raw': 'Raw dV/dQ (from dataset)',
        'dqdv_sm_grad': 'dQ/dV (gradient from smoothed V)',
        'dvdq_sm_grad': 'dV/dQ (gradient from smoothed V)',
        'dqdv_pre_grad': 'dQ/dV (gradient from interpolated + smoothed V)',
        'dvdq_pre_grad': 'dV/dQ (gradient from interpolated + smoothed V)',
        'integrate_i': 'dQ/dV from I·dt',
        'vq': 'Interpolated + Smoothed V–Q'
    }
    return labels.get(kind, kind)

def plot_preprocessed_qv(df, cycle_no, folder_no,
                         min_seg_length, min_v_variation,
                         no_points, window, polyorder,
                         process, **kwargs):
    processed = process_all(df, folder_no,
                            min_seg_length, min_v_variation,
                            no_points, window, polyorder,
                            type='preprocess')

    for entry in processed:
        if entry['cycle_no'] == cycle_no:
            df_pre = entry['df_charge'] if process == 'charge' else entry['df_discharge']
            q = df_pre[Qc] if process == 'charge' else df_pre[Qd]
            v = df_pre["Voltage_sm (V)"]
            break
    else:
        print(f"[Warning] Cycle {cycle_no} not found.")
        return None

    label = _make_label("vq")
    title = _make_title("Interpolated + Smoothed V–Q", folder_no, cycle_no, process)

    plt.plot(q, v, label=label, **kwargs)
    plt.xlabel("Capacity (Ah)")
    plt.ylabel("Interpolated + Smoothed Voltage (V)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

    return df_pre


def save_monotonic_region_from_segment(df, df_pre,
                                       folder_no, cycle_no, q_min, q_max,
                                       min_seg_length, min_v_variation,
                                       no_points, window, polyorder,
                                       process,
                                       type='smoothed'):
    q_col = Qc if process == 'charge' else Qd

    if type == 'preprocessed':
        region = df_pre[(df_pre[q_col] >= q_min) & (df_pre[q_col] <= q_max)].copy()
        name = f"preprocessed_folder_{folder_no:04d}_cycle_{cycle_no:04d}_{process}.csv"

        raise ValueError(f"Invalid type: {type}")

    region.to_csv(output_data_path / name, index=False)
    print(f"[✓] Saved {type} region to {name}")



def get_mono(kind, folder_no, cycle_no, process):
    if kind in ['preprocessed', 'smoothed']:
        file_name = f"{kind}_folder_{folder_no:04d}_cycle_{cycle_no:04d}_{process}.csv"
    else:
        raise ValueError("kind must be one of 'preprocessed', 'smoothed', or 'pre_for_integrate'")

    full_path = output_data_path / file_name
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {full_path}")

    return pd.read_csv(full_path)


def plot_mono_pre_qv(folder_no, cycle_no, process, **kwargs):
    df = get_mono("preprocessed", folder_no, cycle_no, process)
    q = df[Qc] if process == 'charge' else df[Qd]
    v = df["Voltage_sm (V)"]

    label = _make_label("vq")
    title = _make_title("Interpolated + Smoothed V–Q", folder_no, cycle_no, process)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(q, v, label=label, **kwargs)

    ax.set_xlabel("Capacity (Ah)")
    ax.set_ylabel("Interpolated + Smoothed Voltage (V)")
    ax.set_title(title)
    ax.grid(True)
    ax.legend()

    return fig

def plot_pre_derivative(df_pre, folder_no, cycle_no, process, eps, save=True, **kwargs):
    q_col = Qc if process == 'charge' else Qd
    v = df_pre['Voltage_sm (V)'].to_numpy()
    q = df_pre[q_col].to_numpy()

    sort_idx = np.argsort(q)
    q, v = q[sort_idx], v[sort_idx]

    # Fix direction for discharge
    if process == 'discharge':
        q = q[::-1]
        v = v[::-1]

    dq, dv = np.gradient(q), np.gradient(v)

    valid_dqdv = np.abs(dv) > eps
    valid_dvdq = np.abs(dq) > eps

    dqdv_vals = np.full_like(q, np.nan)
    dvdq_vals = np.full_like(q, np.nan)
    dqdv_vals[valid_dqdv] = dq[valid_dqdv] / dv[valid_dqdv]
    dvdq_vals[valid_dvdq] = dv[valid_dvdq] / dq[valid_dvdq]

    df_pre = df_pre.copy()
    df_pre[q_col], df_pre['Voltage_sm (V)'] = q, v
    df_pre['dQ/dV (computed from preprocessed V) (Ah/V)'] = dqdv_vals
    df_pre['dV/dQ (computed from preprocessed V) (V/Ah)'] = dvdq_vals

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True)
    axes[0].plot(v[valid_dqdv], dqdv_vals[valid_dqdv], label=_make_label('dqdv_pre_grad'), **kwargs)
    axes[1].plot(v[valid_dvdq], dvdq_vals[valid_dvdq], label=_make_label('dvdq_pre_grad'), **kwargs)

    for ax in axes:
        ax.set_xlabel("Voltage (V)")
        ax.grid(True)
        ax.legend()
    axes[0].set_ylabel("dQ/dV (Ah/V)")
    axes[1].set_ylabel("dV/dQ (V/Ah)")
    axes[0].set_title(_make_title('dQ/dV (gradient)', folder_no, cycle_no, process))
    axes[1].set_title(_make_title('dV/dQ (gradient)', folder_no, cycle_no, process))

    plt.tight_layout()
    plt.show()

    if save:
        file_name = f"preprocessed_folder_{folder_no:04d}_cycle_{cycle_no:04d}_{process}.csv"
        df_pre.to_csv(output_data_path / file_name, index=False)
        print(f"[✓] Saved preprocessed file with gradients: {file_name}")

    return df_pre, fig

def plot_selected_vq(cycle_no, process='charge',
                     min_seg_length=50, min_v_variation=10,
                     no_points=300, window=11, polyorder=3,
                     **kwargs):
    """
    Plot preprocessed smoothed V–Q curve for a selected cycle.
    Useful for visually choosing the monotonic Q-range for later analysis.

    Uses _last_folder['df'] and _last_folder['folder_no'] as input source.
    """
    df = _last_folder['df']
    folder_no = _last_folder['folder_no']

    plot_preprocessed_qv(
        df=df,
        cycle_no=cycle_no,
        folder_no=folder_no,
        min_seg_length=min_seg_length,
        min_v_variation=min_v_variation,
        no_points=no_points,
        window=window,
        polyorder=polyorder,
        process=process,
        **kwargs
    )


def plot_all_from_qrange(cycle_no, q_min, q_max, process,
                         min_seg_length, min_v_variation,
                         no_points, window, polyorder, eps, save, show, dpi, **kwargs):
    """
    Complete differential analysis pipeline for a single cycle:
    - Plot smoothed V–Q curve
    - Save monotonic regions
    - Reload segments
    - (Optional) Plot and save dQ/dV and dV/dQ from all methods
    """
    df = _last_folder['df']
    folder_no = _last_folder['folder_no']

    # Step 1: Plot V–Q curve and retrieve processed segment
    df_pre = plot_preprocessed_qv(
        df=df,
        cycle_no=cycle_no,
        folder_no=folder_no,
        min_seg_length=min_seg_length,
        min_v_variation=min_v_variation,
        no_points=no_points,
        window=window,
        polyorder=polyorder,
        process=process,
        **kwargs
    )

    # Step 2: Save Q-range regions from all 3 processing types
    for kind in ['preprocessed', 'smoothed', 'pre_for_integrate']:
        save_monotonic_region_from_segment(
            df=df,
            df_pre=df_pre,
            folder_no=folder_no,
            cycle_no=cycle_no,
            q_min=q_min,
            q_max=q_max,
            min_seg_length=min_seg_length,
            min_v_variation=min_v_variation,
            no_points=no_points,
            window=window,
            polyorder=polyorder,
            process=process,
            type=kind
        )

    # Step 3: Reload saved segments
    df_pre_saved = get_mono('preprocessed', folder_no, cycle_no, process)

    # Step 4: Plot all, and save with according names as a list
    figs = []

    fig1 = plot_mono_pre_qv(folder_no, cycle_no, process, **kwargs)
    fname1 = f"QV__F{folder_no}_C{cycle_no}_{process}.png"
    figs.append((fig1, fname1))

    _, fig3 = plot_pre_derivative(df_pre_saved, folder_no, cycle_no, process, eps=eps, **kwargs)
    fname3 = f"Interp_Sm_Derivatives__F{folder_no}_C{cycle_no}_{process}.png"
    figs.append((fig3, fname3))

    # Step 5: Control saving and presenting
    for fig, filename in figs:
        if save:
            full_path = output_plot_path / filename
            fig.savefig(full_path, dpi=dpi, bbox_inches='tight')

        if show:
            plt.show()
