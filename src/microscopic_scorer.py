# microscopic_scorer.py
"""
MICROSCOPIC CANDIDATE SCORER
============================
Evaluates and scores 7 candidate microscopic phenomena based on wet-lab observables.
Candidates:
- speciation
- ion pairing
- aggregation state
- cluster opening
- solvation-shell reshaping
- ligand exchange
- conformational gating
"""

from typing import Dict, Any, List

class MicroscopicCandidateScorer:
    """
    Evaluates wet-lab observables against a rigorous multi-variable matrix 
    to pinpoint the most likely microscopic explanation behind the macroscopic behavior.
    """
    @staticmethod
    def evaluate_candidates(
        st_surrogate: float,
        conversion_pct: float,
        induction_period_hr: float,
        dosy_coeff: float, # m^2/s * 10^-10 (smaller = bigger aggregates)
        exotherm_level: str, # 'none', 'mild', 'runaway'
        is_flexible: bool, # from Layer 0 molecular graph
        has_donor_atoms: bool # from Layer 0 (N, O, P, S)
    ) -> List[Dict[str, Any]]:
        """
        Calculates a compatibility score [0.0 - 100.0] for each of the 7 microscopic candidates.
        """
        candidates = {
            "aggregation_state": 0.0,
            "solvation-shell_reshaping": 0.0,
            "speciation": 0.0,
            "cluster_opening": 0.0,
            "ion_pairing": 0.0,
            "ligand_exchange": 0.0,
            "conformational_gating": 0.0
        }
        
        # 1. Aggregation State
        # Highly likely in LATENT_JAMMED, low conversion, high induction period, low DOSY diffusion
        if st_surrogate < 0.10:
            candidates["aggregation_state"] += 40.0
        if dosy_coeff > 0 and dosy_coeff < 1.5:
            candidates["aggregation_state"] += 40.0
        if induction_period_hr > 2.0:
            candidates["aggregation_state"] += 20.0
        if conversion_pct < 10.0:
            candidates["aggregation_state"] += 10.0
            
        # 2. Solvation-Shell Reshaping
        # Promoted by moderate ST_surrogate (Protected/Protected Coherent), mild exotherm, temperature transitions
        if 0.10 <= st_surrogate <= 0.24:
            candidates["solvation-shell_reshaping"] += 30.0
        if exotherm_level == "mild":
            candidates["solvation-shell_reshaping"] += 30.0
        if not is_flexible: # rigid scaffolds often adapt via solvent-shell adjustments
            candidates["solvation-shell_reshaping"] += 20.0
        if conversion_pct > 50.0:
            candidates["solvation-shell_reshaping"] += 20.0
            
        # 3. Speciation (equilibriums)
        # Promoted by PROTECTED_COHERENT zone, excellent yields, high sensitivity to water/additives
        if 0.18 <= st_surrogate <= 0.24:
            candidates["speciation"] += 45.0
        if conversion_pct >= 80.0:
            candidates["speciation"] += 25.0
        if has_donor_atoms: # donor atoms coordinate to form different species
            candidates["speciation"] += 20.0
        if dosy_coeff >= 2.0: # standard, non-aggregated diffusing species
            candidates["speciation"] += 10.0
            
        # 4. Cluster Opening
        # Promoted by BOUNDARY_ZONE and RUNAWAY, high exotherm, sudden loss of selectivity
        if st_surrogate > 0.24:
            candidates["cluster_opening"] += 40.0
        if exotherm_level in ["mild", "runaway"]:
            candidates["cluster_opening"] += 30.0
        if conversion_pct > 40.0 and st_surrogate > 0.33: # runaway conversion to tar
            candidates["cluster_opening"] += 30.0
            
        # 5. Ion Pairing
        # Solvent transfer sensitivity, polar solvents, ionic substrates
        if 0.10 <= st_surrogate <= 0.33:
            candidates["ion_pairing"] += 30.0
        if has_donor_atoms:
            candidates["ion_pairing"] += 30.0
        if exotherm_level == "mild":
            candidates["ion_pairing"] += 20.0
        if dosy_coeff > 1.5 and dosy_coeff < 3.0: # medium sized contact ion pairs
            candidates["ion_pairing"] += 20.0
            
        # 6. Ligand Exchange
        # Promoted by donor atoms (N, O, P, S), moderate temp, active metals
        if has_donor_atoms:
            candidates["ligand_exchange"] += 50.0
        if 0.10 <= st_surrogate <= 0.24:
            candidates["ligand_exchange"] += 30.0
        if conversion_pct > 30.0:
            candidates["ligand_exchange"] += 20.0
            
        # 7. Conformational Gating
        # Flexible chains, temperature-dependent gating, ring-poor graphs
        if is_flexible:
            candidates["conformational_gating"] += 50.0
        if 0.18 <= st_surrogate <= 0.33:
            candidates["conformational_gating"] += 30.0
        if dosy_coeff >= 3.0: # very fast diffusion of small flexible units
            candidates["conformational_gating"] += 20.0
            
        # Normalize and sort candidates
        scored_candidates = []
        for name, score in candidates.items():
            # Constrain to 100 max
            final_score = min(100.0, max(5.0, score))
            scored_candidates.append({
                "candidate": name,
                "score": float(final_score),
                "confidence_level": "High Compatibility" if final_score >= 70.0 else \
                                    ("Moderate Compatibility" if final_score >= 40.0 else "Low Compatibility")
            })
            
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        return scored_candidates
