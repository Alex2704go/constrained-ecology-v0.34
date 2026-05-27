# transfer_topology.py
"""
TRANSFER TOPOLOGY AND RESTRUCTURING ROUTING
=============================================
Direct implementation of Section 3 (Same-molecule transfer topology)
and Section 7 (Dual-route restructuring / Route bifurcation).
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from src.ontology_layers import Layer0MolecularGraph, Layer1Observability

class SameMoleculeTransferTopology:
    """
    Same-Molecule Transfer Topology (Section 3).
    Models the phenomenon that under solvent transfer, the underlying chemical topology
    remains invariant, but the observability routing reorganizes strongly.
    Preference: localize adaptation inside proton layers, preserve carbon bookkeeping scaffolds.
    """
    @staticmethod
    def audit_transfer_reorganization(
        molecule: Layer0MolecularGraph,
        shifts_solvent_1: Dict[str, float], # node_id -> chemical shift in CDCl3
        shifts_solvent_2: Dict[str, float], # node_id -> chemical shift in DMSO-d6
        detector_roles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates shift differences across solvents and maps adaptation burden
        to prove that systems localize adaptation inside 1H while preserving 13C.
        """
        proton_deviations = []
        carbon_deviations = []
        nodes_audit = []
        
        for node_id in shifts_solvent_1.keys():
            if node_id not in shifts_solvent_2:
                continue
            
            s1 = shifts_solvent_1[node_id]
            s2 = shifts_solvent_2[node_id]
            deviation = abs(s1 - s2)
            
            # Identify nucleus type based on node_id naming convention (e.g., 'H_' or 'C_')
            is_proton = "H" in node_id or node_id.startswith("H_") or any(ch in node_id for ch in ["_H", "H"])
            # Carbon check
            is_carbon = "C" in node_id and not is_proton
            
            role = "unknown"
            if is_proton:
                proton_deviations.append(deviation)
                role = "adaptive_front"
            elif is_carbon:
                carbon_deviations.append(deviation)
                role = "bookkeeping_scaffold"
                
            nodes_audit.append({
                "node_id": node_id,
                "shift_solv1": s1,
                "shift_solv2": s2,
                "deviation": deviation,
                "designated_role": role
            })
            
        mean_h_dev = np.mean(proton_deviations) if proton_deviations else 0.0
        mean_c_dev = np.mean(carbon_deviations) if carbon_deviations else 0.0
        
        # Theorem verification: adaptation localized in H, scaffold C preserved
        # Since 13C shifts have a larger scale, we normalize by nominal range (1H scale ~ 10 ppm, 13C ~ 200 ppm)
        normalized_h_dev = mean_h_dev / 10.0
        normalized_c_dev = mean_c_dev / 200.0
        
        is_scaffold_preserved = normalized_c_dev < normalized_h_dev
        
        return {
            "mean_proton_deviation": mean_h_dev,
            "mean_carbon_deviation": mean_c_dev,
            "normalized_proton_deviation": normalized_h_dev,
            "normalized_carbon_deviation": normalized_c_dev,
            "is_scaffold_preserved": bool(is_scaffold_preserved),
            "nodes_audit": nodes_audit,
            "theorem_status": "PASSED: Adaptation localized in proton front, bookkeeping scaffold preserved." if is_scaffold_preserved else "FAILED"
        }


class DualRouteRestructuring:
    """
    Dual-Route Restructuring (Section 7).
    Exploratory restructuring bifurcates into:
    A. Localization Route (~81%): High adaptation gap, high proton burden, high topology cost.
    B. Scaffold Route (~10%): Negative adaptation gap, low proton burden, lower topology cost.
    Ensures route coexistence is suppressed (dead-zone near small positive gaps).
    """
    def __init__(self, adaptation_gap: float, proton_burden: float, topology_cost: float):
        self.adaptation_gap = adaptation_gap
        self.proton_burden = proton_burden
        self.topology_cost = topology_cost

    def classify_restructuring_route(self) -> Dict[str, Any]:
        """
        Classifies the restructuring routing state based on physical observables.
        Enforces dead-zone suppression (Section 8).
        """
        # Dead-zone verification: small positive gaps are suppressed
        is_in_dead_zone = 0.0 < self.adaptation_gap < 5.0
        
        if is_in_dead_zone:
            return {
                "route": "SUPPRESSED_DEAD_ZONE",
                "properties": ["route_coexistence_forbidden", "high_frustration"],
                "probability": 0.0,
                "adaptation_gap": self.adaptation_gap,
                "description": "Route coexistence is aggressively suppressed. System maintains organizational purity."
            }
            
        # Route A: Localization Route
        if self.adaptation_gap >= 5.0 and self.proton_burden > 3.0 and self.topology_cost >= 50.0:
            return {
                "route": "Route_A_Localization",
                "properties": ["huge_adaptation_gap", "high_proton_burden", "high_topology_cost", "coherent_organized_restructuring"],
                "probability": 0.81,
                "adaptation_gap": self.adaptation_gap,
                "description": "Canalized localization-driven exploratory access."
            }
            
        # Route B: Scaffold Route
        if self.adaptation_gap < 0.0 and self.proton_burden <= 3.0:
            return {
                "route": "Route_B_Scaffold",
                "properties": ["negative_adaptation_gap", "low_proton_burden", "lower_topology_cost", "entropy_rich_restructuring"],
                "probability": 0.10,
                "adaptation_gap": self.adaptation_gap,
                "description": "Bookkeeping-mediated exploratory access."
            }
            
        # Mismatched/Unassigned route (sparse frustrated pockets)
        return {
            "route": "Sparse_Frustrated_Coexistence_Pocket",
            "properties": ["non_continuous_bridge", "unstable_regime"],
            "probability": 0.09,
            "adaptation_gap": self.adaptation_gap,
            "description": "Frustrated coexistence pocket, not a continuous bridge."
        }
