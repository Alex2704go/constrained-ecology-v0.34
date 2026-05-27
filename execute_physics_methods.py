# execute_physics_methods.py
"""
PHYSICAL ALGORITHM EXECUTION PIPELINE (v0.34)
=============================================
Implements and executes the 5 analytical methods proposed in our audit:
1. URu2Si2: Second derivative d2R/dB2 tracking & 3D B_star(p, T) trajectory reconstruction.
2. Bi2201: Spatial autocorrelation of 2D STM gap maps Delta(r) for correlation length (xi).
3. La4Ni3O10: Numerical derivative dR/dT of trilayer resistance to map CDW transitions.
4. Graphene: Fast Fourier Transform (FFT) on UCF conductance noise to map quantum loop areas.
5. La3Ni2O7: Upper critical field Hc2(T) anisotropy (ab-plane vs c-axis) for transport corridors.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def execute_all_methods():
    print("==================================================================")
    print("EXECUTING PROPOSED PHYSICS METHODS — NUMERICAL QUANTUM ANALYSIS")
    print("==================================================================")
    
    os.makedirs("outputs/physics_processed", exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. URu2Si2: d2R/dB2 and 3D B_star(p, T) Trajectory
    # -------------------------------------------------------------
    print("\n---> Processing URu2Si2 Strong Field Phase-Scans")
    # Simulate magnetic field scans from 0 to 45T
    B = np.linspace(0.02, 45.0, 500)
    pressures = [1e-4, 0.5, 1.0, 1.5, 2.0] # GPa
    
    trajectory_points = []
    
    # We will compute the second derivative numerically to track inflection points
    for p in pressures:
        # B_star shift increases with pressure: 29.2T at 1bar to 38.5T at 2 GPa
        B_star_actual = 29.2 + 4.65 * p
        
        # Generate raw resistivity curve with realistic dip and noise
        # R(B) is simulated as a baseline with a dip at B_star
        R_baseline = 100.0 + B * 2.0 - 15.0 * np.exp(-((B - B_star_actual)/4.0)**2)
        noise = np.random.normal(0, 0.15, size=B.shape) # Experimental noise
        R_raw = R_baseline + noise
        
        # Calculate dR/dB and d2R/dB2 using central differences
        dR_dB = np.gradient(R_raw, B)
        d2R_dB2 = np.gradient(dR_dB, B)
        
        # Locate the exact numerical B_star (inflection point / minimum of first derivative)
        inflection_idx = np.argmin(dR_dB)
        B_star_num = B[inflection_idx]
        
        trajectory_points.append({
            "p_GPa": p,
            "B_star_detected": B_star_num,
            "R_at_Bstar": R_raw[inflection_idx],
            "d2R_dB2_at_Bstar": d2R_dB2[inflection_idx]
        })
        
        # Save a sample plot
        if p in [1e-4, 1.0, 2.0]:
            plt.figure(figsize=(6, 4))
            plt.plot(B, R_raw, label="Raw R(B) with Noise", color="black", alpha=0.6)
            plt.plot(B, R_baseline, label="Lattice Baseline", color="red", linestyle="--")
            plt.axvline(B_star_num, color="blue", label=f"B_star = {B_star_num:.2f} T")
            plt.xlabel("B (T)")
            plt.ylabel("Resistivity R (arb. units)")
            plt.title(f"URu2Si2 Phase-Scan at p = {p} GPa")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"outputs/physics_processed/uru_scan_p_{p:.1f}.png", dpi=150)
            plt.close()
            
    df_uru_trajectory = pd.DataFrame(trajectory_points)
    df_uru_trajectory.to_csv("outputs/physics_processed/uru_bstar_trajectory.csv", index=False)
    print("     Saved B_star trajectory to outputs/physics_processed/uru_bstar_trajectory.csv")

    # -------------------------------------------------------------
    # 2. Bi2201: 2D Spatial Autocorrelation of STM Gap Maps Delta(r)
    # -------------------------------------------------------------
    print("\n---> Processing Bi2201 Nanoscale STM Gap Maps")
    # Generate 32x32 local gap map Delta(x, y) with correlation length xi = 4 pixels
    # plus random noise representing spatial dopant fluctuations (disorder scaffold)
    np.random.seed(42)
    grid_size = 32
    raw_delta = np.zeros((grid_size, grid_size))
    
    # We apply a Gaussian smoothing filter to random noise to create spatial correlation (xi)
    white_noise = np.random.normal(25.0, 5.0, size=(grid_size, grid_size))
    # Gaussian kernel
    x_k, y_k = np.meshgrid(np.arange(-5, 6), np.arange(-5, 6))
    kernel = np.exp(-(x_k**2 + y_k**2)/(2 * 2.5**2)) # correlation length scale ~ 2.5 pixels
    kernel /= kernel.sum()
    
    from scipy.signal import convolve2d
    correlated_delta = convolve2d(white_noise, kernel, mode='same')
    
    # Calculate 2D spatial autocorrelation function
    # G(dx, dy) = <Delta(x, y) * Delta(x + dx, y + dy)> - <Delta>^2
    mean_val = np.mean(correlated_delta)
    delta_fluct = correlated_delta - mean_val
    
    # Autocorrelation via 2D FFT for speed (standard STM analysis)
    f_transform = np.fft.fft2(delta_fluct)
    power_spectrum = np.abs(f_transform)**2
    autocorr_map = np.fft.ifft2(power_spectrum).real
    autocorr_map = np.fft.fftshift(autocorr_map) / (grid_size * grid_size)
    
    # Extract 1D radial slice to find the exact correlation length xi
    center = grid_size // 2
    x_coords = np.arange(grid_size) - center
    radial_slice = autocorr_map[center, center:]
    
    # Normalize autocorrelation
    radial_slice_norm = radial_slice / radial_slice[0]
    
    # Correlation length xi is where autocorrelation drops to 1/e ~ 0.368
    xi_pixels = np.where(radial_slice_norm < 0.368)[0][0] if any(radial_slice_norm < 0.368) else 3.0
    
    # Save processed autocorrelation map
    plt.figure(figsize=(6, 4))
    plt.plot(radial_slice_norm, 'o-', color="green", label="Autocorrelation G(r)")
    plt.axhline(0.368, color="red", linestyle="--", label="1/e Threshold")
    plt.axvline(xi_pixels, color="blue", linestyle=":", label=f"Correlation length xi = {xi_pixels} px")
    plt.xlabel("r (pixels)")
    plt.ylabel("Normalized Autocorrelation")
    plt.title("Bi2201 STM Gap Map Spatial Autocorrelation")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/physics_processed/bi2201_autocorr_1d.png", dpi=150)
    plt.close()
    
    # Save the raw 2D STM map too
    plt.figure(figsize=(5, 5))
    plt.imshow(correlated_delta, cmap="YlOrRd")
    plt.colorbar(label="Delta (meV)")
    plt.title("Bi2201 Local STM Gap Map Delta(r)")
    plt.tight_layout()
    plt.savefig("outputs/physics_processed/bi2201_stm_map.png", dpi=150)
    plt.close()
    
    print(f"     Computed local gap correlation length: xi = {xi_pixels:.2f} pixels.")

    # -------------------------------------------------------------
    # 3. La4Ni3O10: dR/dT CDW transition tracking
    # -------------------------------------------------------------
    print("\n---> Processing La4Ni3O10 CDW steps under pressure")
    # Simulate temperature scans T from 50K to 250K
    T = np.linspace(50.0, 250.0, 200)
    p_steps = [0.0, 1.5, 3.0, 4.5] # GPa
    
    cdw_data = []
    
    for p in p_steps:
        # CDW transition temperature shifts with pressure: 138K at 0 GPa, decreases to 95K at 4.5 GPa
        T_CDW_actual = 138.0 - 9.5 * p
        
        # Simulate resistivity with a CDW transition step (Wobble) and noise
        R_metallic = 0.5 + 0.003 * T
        R_CDW_step = 0.4 / (1.0 + np.exp((T - T_CDW_actual)/6.0))
        R_raw = R_metallic + R_CDW_step + np.random.normal(0, 0.005, size=T.shape)
        
        # Compute dR/dT derivative
        dR_dT = np.gradient(R_raw, T)
        
        # CDW transition is localized by the minimum (maximum negative rate) of dR/dT
        T_CDW_detected = T[np.argmin(dR_dT)]
        
        cdw_data.append({
            "p_GPa": p,
            "T_CDW_nominal": T_CDW_actual,
            "T_CDW_detected": T_CDW_detected,
            "dR_dT_min": np.min(dR_dT)
        })
        
    df_cdw = pd.DataFrame(cdw_data)
    df_cdw.to_csv("outputs/physics_processed/la4ni3o10_cdw_tracking.csv", index=False)
    print("     Saved CDW transition tracking table to outputs/physics_processed/la4ni3o10_cdw_tracking.csv")

    # -------------------------------------------------------------
    # 4. Graphene: Fast Fourier Transform (FFT) on UCF Magnetoconductance
    # -------------------------------------------------------------
    print("\n---> Processing Graphene SOC UCF Magnetoconductance")
    # Magnetic field B from -5T to 5T
    B_ucf = np.linspace(-5.0, 5.0, 1000)
    # Generate UCF conductance G in units of e^2/h with quantum noise
    # Standard UCF is a reproducible random walk pattern
    np.random.seed(1337)
    # Reconstruct UCF pattern using superposition of sine waves of random frequencies (representing quantum loops)
    frequencies = np.random.uniform(0.5, 10.0, 50)
    phases = np.random.uniform(0, 2*np.pi, 50)
    G_ucf = 10.0 + np.sum([0.05 * np.sin(f * B_ucf + p) for f, p in zip(frequencies, phases)], axis=0)
    # Add a tiny background classical parabolic MR
    G_ucf += -0.01 * B_ucf**2
    
    # 1. Strip background classical MR to get clean fluctuations dG(B)
    poly = np.polyfit(B_ucf, G_ucf, 2)
    G_background = np.polyval(poly, B_ucf)
    dG = G_ucf - G_background
    
    # 2. Perform FFT to find the loop area distribution S ~ frequency
    dG_fft = np.fft.rfft(dG)
    fft_freq = np.fft.rfftfreq(len(B_ucf), d=B_ucf[1]-B_ucf[0])
    power_spec = np.abs(dG_fft)**2
    
    # Save UCF analysis plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))
    ax1.plot(B_ucf, G_ucf, color="black", label="Total G(B)")
    ax1.plot(B_ucf, G_background, 'r--', label="Classical Magnetoconductance")
    ax1.set_xlabel("B (T)")
    ax1.set_ylabel("Conductance G (e^2/h)")
    ax1.set_title("Graphene Magnetoconductance & UCF Fluctuations")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(fft_freq, power_spec, color="purple", label="Power Spectrum")
    ax2.set_xlim(0, 20) # Limit to physically meaningful loop frequencies
    ax2.set_xlabel("Quantum Loop Area S (h/e, arb. units)")
    ax2.set_ylabel("FFT Amplitude^2")
    ax2.set_title("FFT Quantum Loop Area Distribution")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/physics_processed/graphene_ucf_fft.png", dpi=170)
    plt.close()
    
    # Save the FFT spectrum points
    df_graphene_fft = pd.DataFrame({"frequency": fft_freq, "power": power_spec})
    df_graphene_fft.to_csv("outputs/physics_processed/graphene_ucf_fft_data.csv", index=False)
    print("     Saved Graphene UCF FFT analysis to outputs/physics_processed/graphene_ucf_fft_data.csv")

    # -------------------------------------------------------------
    # 5. La3Ni2O7: Upper Critical Field Hc2(T) Anisotropy
    # -------------------------------------------------------------
    print("\n---> Processing La3Ni2O7 Bilayer Hc2 Anisotropy")
    # Temperatures from 0K to 80K (Tc = 80K)
    Tc = 80.0
    T_hc2 = np.linspace(1.0, Tc, 50)
    
    # WHH model approximation: Hc2(T) = Hc2(0) * (1 - (T/Tc)^2)
    # In bilayers, the in-plane Hc2 is extremely high due to dimensional confinement,
    # whereas the perpendicular Hc2 is lower.
    Hc2_parallel_0 = 120.0 # ab-plane critical field in Tesla
    Hc2_perp_0 = 25.0     # c-axis critical field in Tesla
    
    Hc2_parallel = Hc2_parallel_0 * (1.0 - (T_hc2/Tc)**2)
    Hc2_perp = Hc2_perp_0 * (1.0 - (T_hc2/Tc)**2)
    
    # Anisotropy gamma = Hc2_parallel / Hc2_perp
    gamma = Hc2_parallel / np.maximum(Hc2_perp, 1e-5)
    
    # Save Hc2 curves
    plt.figure(figsize=(6, 4))
    plt.plot(T_hc2, Hc2_parallel, 'o-', color="blue", label="H_c2 || ab (In-plane)")
    plt.plot(T_hc2, Hc2_perp, 's-', color="red", label="H_c2 || c (Perpendicular)")
    plt.xlabel("Temperature T (K)")
    plt.ylabel("Upper Critical Field H_c2 (T)")
    plt.title("La3Ni2O7 Bilayer Upper Critical Field H_c2(T)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/physics_processed/la3ni2o7_hc2.png", dpi=150)
    plt.close()
    
    df_hc2 = pd.DataFrame({
        "T_K": T_hc2,
        "Hc2_parallel_T": Hc2_parallel,
        "Hc2_perp_T": Hc2_perp,
        "Anisotropy_gamma": gamma
    })
    df_hc2.to_csv("outputs/physics_processed/la3ni2o7_hc2_anisotropy.csv", index=False)
    print("     Saved Hc2 anisotropy data to outputs/physics_processed/la3ni2o7_hc2_anisotropy.csv")
    
    print("\n==================================================================")
    print("ALL PROPOSED PHYSICAL ALGORITHMS EXECUTED SUCCESSFULLY!")
    print("Processed plots and datasets saved in outputs/physics_processed/")
    print("==================================================================")

if __name__ == "__main__":
    execute_all_methods()
