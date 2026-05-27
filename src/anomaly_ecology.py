# anomaly_ecology.py
"""
COUPLED ANOMALY ECOLOGY AUDITOR
==============================
Direct implementation of Section 10: Coupled anomaly ecology.
Analyzes functional groups (Halogens, Nitriles, Boron) and their synergy:
- Nitriles: zero exploratory access, maximal rigidity, suppressed restructuring.
- Halogens: elevated scaffold participation, entropy-rich corridor, lowered proton dominance.
- Boron: moderate mediator, reduced proton burden, constrained scaffold.
- Boron-Halogen Coupling: Synergy index ~ 3.2. Suppresses exploratory liberation, amplifies organized localization.
"""

from typing import Dict, Any, Tuple
from src.ontology_layers import Layer0MolecularGraph

class AnomalyEcologyAuditor:
    """
    Anomaly Ecology Auditor.
    Quantifies spectroscopic behaviors of functional groups.
    Computes synergy indices and verifies coupled anomalies.
    """
    @staticmethod
    def audit_anomaly(molecule: Layer0MolecularGraph) -> Dict[str, Any]:
        """
        Analyzes the molecule and returns its anomaly profile and synergy indices.
        """
        scaffold_participation = 1.0  # base
        rigidity_index = 1.0          # base
        exploration_capability = 1.0   # base
        proton_dominance = 1.0        # base
        
        anomalies_detected = []
        
        # 1. Nitrile effect (Section 10)
        # Suppressed restructuring, zero exploratory access, maximal rigidity
        if molecule.is_nitrile:
            scaffold_participation += 0.5
            rigidity_index += 5.0 # Max rigidity
            exploration_capability = 0.0 # Zero exploratory access
            proton_dominance -= 0.3
            anomalies_detected.append("Nitrile_Protected_Sector")
            
        # 2. Halogen effect (Section 10)
        # Elevated scaffold participation, entropy-rich corridor, lowered proton dominance, broad topology spread
        if molecule.has_halogen:
            scaffold_participation += 1.5 # Elevated scaffold
            rigidity_index -= 0.2
            exploration_capability += 0.5
            proton_dominance -= 0.4 # Lowered proton dominance
            anomalies_detected.append("Halogen_Destabilizing_Sector")
            
        # 3. Boron effect (Section 10)
        # Moderate mediator, reduced proton burden, constrained scaffold, localized restructuring
        if molecule.has_boron:
            scaffold_participation += 0.4
            rigidity_index += 0.1
            exploration_capability += 0.2
            proton_dominance -= 0.2
            anomalies_detected.append("Boron_Mediator_Sector")
            
        # 4. Boron-Halogen Coupling (Section 10)
        # Synergy Index ~ 3.2. Suppresses exploratory liberation, amplifies organized localization
        synergy_index = 1.0
        if molecule.has_boron and molecule.has_halogen:
            synergy_index = 3.2 # Direct physical invariant observed in Stage_X2
            # Coupling behavior
            exploration_capability = 0.1 # Suppresses exploratory liberation
            scaffold_participation += 2.0 # Amplifies organized localization
            anomalies_detected.append("Coupled_Boron_Halogen_Synergy")
            
        return {
            "smiles": molecule.smiles,
            "anomalies_detected": anomalies_detected,
            "scaffold_participation": scaffold_participation,
            "rigidity_index": rigidity_index,
            "exploration_capability": exploration_capability,
            "proton_dominance": proton_dominance,
            "synergy_index": synergy_index,
            "is_nitrile_protected": molecule.is_nitrile,
            "is_coupled_synergy_active": (molecule.has_boron and molecule.has_halogen)
        }
