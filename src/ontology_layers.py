# ontology_layers.py
"""
ONTOLOGY LAYERS — DEFINITIONS AND REPRESENTATIONS
===================================================
Direct implementation of:
Layer 0 - Molecular Graph Substrate (SMILES, rings, conjugation, hetero-atoms)
Layer 1 - Constrained Observability Organization (Detector Asymmetry, 1H vs 13C roles)
Layer 2 - Representation Ecology (Detector Grammar, Solvents, Formatting)
"""

import re
from typing import Dict, List, Any, Tuple

class Layer0MolecularGraph:
    """
    Layer0 — Molecular Graph Substrate.
    Processes the raw structural grammar (SMILES) into stable graph observables:
    conjugation, ring ecology, branching, and heteroatom organization.
    """
    def __init__(self, smiles: str):
        self.smiles = smiles
        self.ring_count, self.is_fused = self._audit_ring_ecology()
        self.is_conjugated = self._audit_conjugation()
        self.hetero_atoms = self._audit_hetero_organization()
        self.is_nitrile = "C#N" in smiles or "N#C" in smiles or "CN" in smiles # Nitrile group indicator
        self.has_boron = "B" in smiles
        self.has_halogen = any(h in smiles for h in ["F", "Cl", "Br", "I"])
        
    def _audit_ring_ecology(self) -> Tuple[int, bool]:
        """
        Analyzes ring structures from SMILES representation.
        Numbers in SMILES indicate ring closures (e.g. c1ccccc1).
        """
        ring_numbers = re.findall(r'\d', self.smiles)
        unique_rings = set(ring_numbers)
        ring_count = len(unique_rings)
        # If the same ring number appears multiple times or we have multiple overlapping rings,
        # it suggests fused or complex rings.
        is_fused = ring_count >= 2 and len(ring_numbers) > 2 * ring_count
        return ring_count, is_fused

    def _audit_conjugation(self) -> bool:
        """
        Aromatic atoms in SMILES are typically represented as lowercase letters
        (c, n, o, s). Double bonds are '='.
        """
        has_aromatic_atoms = any(c in self.smiles for c in ['c', 'n', 'o', 's'])
        has_double_bonds = '=' in self.smiles
        return has_aromatic_atoms or has_double_bonds

    def _audit_hetero_organization(self) -> Dict[str, int]:
        """
        Counts the occurrence of heteroelements in the SMILES string.
        """
        counts = {
            "F": self.smiles.count("F"),
            "Cl": self.smiles.count("Cl"),
            "Br": self.smiles.count("Br"),
            "I": self.smiles.count("I"),
            "B": self.smiles.count("B"),
            "N": self.smiles.count("N") + self.smiles.count("n"),
            "O": self.smiles.count("O") + self.smiles.count("o"),
            "P": self.smiles.count("P"),
            "Si": self.smiles.count("Si")
        }
        return {k: v for k, v in counts.items() if v > 0}

    def get_graph_density_score(self) -> float:
        """
        Computes the graph-level complexity density score.
        Enriched in ring-rich, conjugated, fused systems.
        """
        score = 1.0
        if self.ring_count > 0:
            score += self.ring_count * 1.5
        if self.is_fused:
            score += 3.0
        if self.is_conjugated:
            score += 2.0
        # Add hetero organization weight
        score += len(self.hetero_atoms) * 0.5
        return score


class Layer1Observability:
    """
    Layer1 — Constrained Observability Organization.
    Implements detector asymmetry, transfer topology, and burden localization.
    """
    def __init__(self, molecule: Layer0MolecularGraph):
        self.molecule = molecule
        self.detector_roles = self._establish_detector_roles()

    def _establish_detector_roles(self) -> Dict[str, Dict[str, Any]]:
        """
        Implements Strong Detector-Role Asymmetry (major result of Section 2):
        - 1H: Adaptive negotiative front, maximal fragmentation, burden carrier.
        - 13C: Bookkeeping scaffold, high rigidity, structural registry.
        - 19F, 11B, 31P, 29Si: Sparse specialist sectors.
        """
        roles = {
            "1H": {
                "role": "Adaptive Negotiative Front",
                "properties": ["maximal_transfer_sensitivity", "maximal_fragmentation", "dominant_burden_migration"],
                "rigidity": 0.2, # low rigidity, high adaptivity
                "exploratory_participation": 0.9
            },
            "13C": {
                "role": "Bookkeeping Scaffold",
                "properties": ["pinned_environment_geometry", "constrained_structural_registry", "high_rigidity"],
                "rigidity": 0.9, # high rigidity, stable scaffold
                "exploratory_participation": 0.1
            }
        }
        
        # Sparse specialist sectors (Section 2)
        for element in ["19F", "11B", "31P", "29Si"]:
            has_elem = False
            if element == "19F" and "F" in self.molecule.hetero_atoms: has_elem = True
            elif element == "11B" and "B" in self.molecule.hetero_atoms: has_elem = True
            elif element == "31P" and "P" in self.molecule.hetero_atoms: has_elem = True
            elif element == "29Si" and "Si" in self.molecule.hetero_atoms: has_elem = True
            
            if has_elem:
                roles[element] = {
                    "role": "Sparse Specialist Sector",
                    "properties": ["selective_observability", "reduced_exploratory_participation", "constrained_corridor_occupation"],
                    "rigidity": 0.6 if element != "11B" else 0.4, # Boron is a moderate mediator
                    "exploratory_participation": 0.3
                }
        return roles


class Layer2Representation:
    """
    Layer2 — Representation Ecology.
    Models detector grammar, solvent transfer effects, baseline errors,
    and formatting fragmentation.
    Handles the critical discipline: Layer 2 effects repeatedly capable of imitating structure.
    """
    def __init__(self, solvent: str):
        self.solvent = solvent
        self.artifacts_profile = self._get_solvent_artifacts()

    def _get_solvent_artifacts(self) -> List[Dict[str, Any]]:
        """
        Defines potential Layer 2 artifacts and noise patterns for different solvents.
        """
        if self.solvent == "CDCl3":
            return [
                {"type": "solvent_residual", "shift": 7.26, "intensity": 5.0, "width": 0.01, "imitates": "1H_aromatic"},
                {"type": "solvent_carbon", "shift": 77.16, "intensity": 3.0, "width": 0.1, "imitates": "13C_scaffold"}
            ]
        elif self.solvent == "DMSO-d6":
            return [
                {"type": "solvent_residual", "shift": 2.50, "intensity": 4.5, "width": 0.02, "imitates": "1H_alkyl"},
                {"type": "water_residual", "shift": 3.33, "intensity": 2.5, "width": 0.05, "imitates": "1H_hydroxyl"},
                {"type": "solvent_carbon", "shift": 39.52, "intensity": 4.0, "width": 0.08, "imitates": "13C_alkyl"}
            ]
        else: # Generic solvent
            return [
                {"type": "baseline_ripple", "shift": 1.0, "intensity": 0.1, "width": 0.5, "imitates": "multiplet_broad_structure"}
            ]

    def filter_layer2_signals(self, raw_peaks: List[Dict[str, Any]], nucleus: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Enforces Critical Discipline: filters out Layer 2 artifacts so they don't imitate Layer 1 structures.
        """
        cleaned_peaks = []
        artifacts = []
        
        for peak in raw_peaks:
            shift = peak["shift"]
            is_artifact = False
            match_reason = ""
            
            for art in self.artifacts_profile:
                # Map nucleus to shift scale (1H is <15ppm, 13C is >20ppm)
                is_carbon_peak = shift > 20.0
                is_carbon_art = "carbon" in art["type"]
                
                if (nucleus == "1H" and not is_carbon_peak and not is_carbon_art) or \
                   (nucleus == "13C" and is_carbon_peak and is_carbon_art):
                    if abs(shift - art["shift"]) <= art["width"] * 1.5:
                        is_artifact = True
                        match_reason = f"Imitative Layer2 Solvent Artifact ({art['type']})"
                        break
            
            if is_artifact:
                artifacts.append({**peak, "filter_reason": match_reason})
            else:
                cleaned_peaks.append(peak)
                
        return cleaned_peaks, artifacts
