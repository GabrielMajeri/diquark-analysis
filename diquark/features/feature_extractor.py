from math import comb
import numpy as np
import awkward as ak
from itertools import combinations

class FeatureExtractor:
    def __init__(self, n_jets: int):
        self.n_jets = n_jets
        self.feature_names = self._generate_feature_names()

    def _generate_feature_names(self) -> list[str]:
        statistics = ("min", "mean", "max")
        features = [
            "jet_multiplicity",
            "combined_invariant_mass",
            "sphericity",
            "aplanarity",
            "centrality",
            "total_energy",
            "total_transverse_momentum",
            *(f"chi2_{i}_{s}" for s in statistics for i in range(1, 4)),
            "2jet_invariant_mass_mean",
            "2jet_invariant_mass_stddev",
            "3jet_invariant_mass_mean",
            "3jet_invariant_mass_stddev",
            "6jet_invariant_mass_mean",
            "6jet_invariant_mass_stddev",
        ]

        return features

    def _pad_jets_array(self, array: ak.Array):
        padded = ak.pad_none(array, self.n_jets, clip=True)
        filled = ak.fill_none(padded, 0.0)
        return filled.to_numpy()

    def _n_jet_invariant_mass(self, energy, p_x, p_y, p_z, n):
        combination_indices = ak.unzip(ak.argcombinations(energy, n=n))
        return np.sqrt(
            sum(energy[combination_indices[i]] for i in range(n)) ** 2 -
            sum(p_x[combination_indices[i]] for i in range(n)) ** 2 -
            sum(p_y[combination_indices[i]] for i in range(n)) ** 2 -
            sum(p_z[combination_indices[i]] for i in range(n)) ** 2
        )

    def compute_all(self, data: ak.Array) -> dict[str, np.ndarray]:
        num_jets = data['Jet'].to_numpy()

        # Extract jet 4-vector components
        p_T = data['Jet/Jet.PT']
        eta = data['Jet/Jet.Eta']
        phi = data['Jet/Jet.Phi']

        # Compute components in Cartesian coordinates
        p_x = p_T * np.cos(phi)
        p_y = p_T * np.sin(phi)
        p_z = p_T * np.sinh(eta)

        # Compute jet energy
        energy = p_T * np.cosh(eta)

        p_x_np = self._pad_jets_array(p_x)
        p_y_np = self._pad_jets_array(p_y)
        p_z_np = self._pad_jets_array(p_z)
        energy_np = self._pad_jets_array(energy)

        momenta = np.moveaxis(np.stack((p_x_np, p_y_np, p_z_np)), 0, -1)
        total = (momenta * momenta).sum(axis=-1).sum(axis=-1)

        non_zero_jets = num_jets > 0

        S = np.zeros((len(data[non_zero_jets]), 3, 3))
        for i in range(3):
            for j in range(3):
                S[:, i, j] = np.vecdot(momenta[non_zero_jets, :, i], momenta[non_zero_jets, :, j]) / total[non_zero_jets]

        eigenvalues = np.linalg.eigvalsh(S)

        eigenvalues = np.sort(eigenvalues, axis=-1)
        lambda_2 = eigenvalues[:, 1]
        lambda_3 = eigenvalues[:, 0]

        sphericity = np.full_like(num_jets, np.nan, dtype=np.float64)
        aplanarity = np.full_like(num_jets, np.nan, dtype=np.float64)

        sphericity[non_zero_jets] = 3/2 * (lambda_2 + lambda_3)
        aplanarity[non_zero_jets] = 3/2 * lambda_3

        total_energy = ak.sum(energy, axis=-1).to_numpy()
        H_T = ak.sum(p_T, axis=-1).to_numpy()
        centrality = H_T / total_energy

        combined_invariant_mass = np.sqrt(
            energy_np.sum(axis=-1) ** 2
            - p_x_np.sum(axis=-1) ** 2
            - p_y_np.sum(axis=-1) ** 2
            - p_z_np.sum(axis=-1) ** 2
        )

        m2j = self._n_jet_invariant_mass(energy, p_x, p_y, p_z, n=2)
        m3j = self._n_jet_invariant_mass(energy, p_x, p_y, p_z, n=3)
        m6j = self._n_jet_invariant_mass(energy, p_x, p_y, p_z, n=6)

        m_W = 80.3692
        sigma_W = 20

        m_chi = 2000
        sigma_chi = 2/100 * m_chi

        m_S = 8000
        sigma_S = 100

        chi2_first_component = ((m2j - m_W) / sigma_W) ** 2
        chi2_second_component = ((m3j - m_chi) / sigma_chi) ** 2
        chi2_third_component = ((m6j - m_S) / sigma_S) ** 2

        features = {
            "jet_multiplicity": num_jets,
            "combined_invariant_mass": combined_invariant_mass,
            "sphericity": sphericity,
            "aplanarity": aplanarity,
            "centrality": centrality,
            "total_energy": total_energy,
            "total_transverse_momentum": H_T,
            "chi2_1_min": ak.min(chi2_first_component, axis=-1).to_numpy(),
            "chi2_1_mean": ak.mean(chi2_first_component, axis=-1).to_numpy(),
            "chi2_1_max": ak.max(chi2_first_component, axis=-1).to_numpy(),
            "chi2_2_min": ak.min(chi2_second_component, axis=-1).to_numpy(),
            "chi2_2_mean": ak.mean(chi2_second_component, axis=-1).to_numpy(),
            "chi2_2_max": ak.max(chi2_second_component, axis=-1).to_numpy(),
            "chi2_3_min": ak.min(chi2_third_component, axis=-1).to_numpy(),
            "chi2_3_mean": ak.mean(chi2_third_component, axis=-1).to_numpy(),
            "chi2_3_max": ak.max(chi2_third_component, axis=-1).to_numpy(),
            "m2j_mean": ak.nanmean(m2j, axis=-1).to_numpy(),
            "m2j_std": ak.nanstd(m2j, axis=-1).to_numpy(),
            "m3j_mean": ak.nanmean(m3j, axis=-1).to_numpy(),
            "m3j_std": ak.nanstd(m3j, axis=-1).to_numpy(),
            "m6j_mean": ak.nanmean(m6j, axis=-1).to_numpy(),
            "m6j_std": ak.nanstd(m6j, axis=-1).to_numpy(),
        }

        return features


class OldFeatureExtractor:
    def __init__(self, n_jets: int):
        self.n_jets = n_jets
        self.feature_names = self._generate_feature_names()

    def _generate_feature_names(self) -> list[str]:
        basic_features = [
            "jet_multiplicity",
            *[f"leading_jet_pt_{i+1}" for i in range(self.n_jets)],
            *[f"leading_jet_eta_{i+1}" for i in range(self.n_jets)],
            *[f"leading_jet_phi_{i+1}" for i in range(self.n_jets)],
            *[f"delta_r_{i+1}_{j+1}" for i in range(self.n_jets) for j in range(i+1, self.n_jets)],
            # Don't include this in feature names list,
            # since it's dropped before doing cross-validation.
            #"combined_invariant_mass",
        ]

        for k in [2, 3]:
            n_choose_k = comb(self.n_jets, k)
            basic_features.extend([f"{k}jet_invariant_mass_{i+1}" for i in range(n_choose_k)])
            # basic_features.extend([f"{k}jet_vector_sum_pt_{i+1}" for i in range(n_choose_k)])

        combined_features = [
            "m3j_m6j_ratio",
            "m2j_m6j_ratio",
            "n_jet_pairs_near_w_mass",
            "max_delta_r",
            "smallest_delta_r_mass",
            "max_vector_sum_pt",
        ]

        return basic_features + combined_features

    def _leading_jet_array(self, data: ak.Array, key: str) -> np.ndarray:
        jet_pt_padded = ak.pad_none(data[key], self.n_jets, axis=-1, clip=True)
        return ak.to_numpy(ak.fill_none(jet_pt_padded, 0))

    def jet_multiplicity(self, data: ak.Array) -> np.ndarray:
        return ak.to_numpy(data["Jet"])

    def leading_jet_pt(self, data: ak.Array) -> np.ndarray:
        return self._leading_jet_array(data, "Jet/Jet.PT")

    def leading_jet_eta(self, data: ak.Array) -> np.ndarray:
        return self._leading_jet_array(data, "Jet/Jet.Eta")

    def leading_jet_phi(self, data: ak.Array) -> np.ndarray:
        return self._leading_jet_array(data, "Jet/Jet.Phi")

    def delta_r(self, etas: np.ndarray, phis: np.ndarray, pts: np.ndarray) -> np.ndarray:
        n_events, _ = etas.shape
        n_pairs = self.n_jets * (self.n_jets - 1) // 2

        delta_eta = etas[:, :, None] - etas[:, None, :]
        delta_phi = self._calculate_delta_phi(phis[:, :, None], phis[:, None, :])

        delta_r_matrix = np.sqrt(delta_eta**2 + delta_phi**2)
        delta_r_matrix = np.triu(delta_r_matrix, k=1)

        pts_mask = np.ones((n_events, self.n_jets, self.n_jets), dtype=bool)
        for i in range(n_events):
            np.fill_diagonal(pts_mask[i], 0)
        pts_mask &= pts[:, :, None] * pts[:, None, :] > 0

        delta_r_matrix *= pts_mask
        delta_r_array = delta_r_matrix.reshape(n_events, -1)[:, :n_pairs]

        return delta_r_array

    @staticmethod
    def _calculate_delta_phi(phi1: np.ndarray, phi2: np.ndarray) -> np.ndarray:
        dphi = phi1 - phi2
        dphi = np.where(dphi > np.pi, dphi - 2 * np.pi, dphi)
        dphi = np.where(dphi < -np.pi, dphi + 2 * np.pi, dphi)
        return dphi

    def combined_invariant_mass(self, px: np.ndarray, py: np.ndarray, pz: np.ndarray, E: np.ndarray) -> np.ndarray:
        px_total = np.sum(px, axis=1)
        py_total = np.sum(py, axis=1)
        pz_total = np.sum(pz, axis=1)
        E_total = np.sum(E, axis=1)

        mass = np.sqrt(E_total**2 - px_total**2 - py_total**2 - pz_total**2)
        return mass

    def n_jet_invariant_mass(self, px: np.ndarray, py: np.ndarray, pz: np.ndarray, E: np.ndarray, k: int) -> np.ndarray:
        combination_indices = np.array(list(combinations(range(self.n_jets), k)))

        raw_masses = np.sqrt(
            E[:, combination_indices].sum(axis=-1) ** 2 -
            px[:, combination_indices].sum(axis=-1) ** 2 -
            py[:, combination_indices].sum(axis=-1) ** 2 -
            pz[:, combination_indices].sum(axis=-1) ** 2
        )

        masses = np.nan_to_num(raw_masses)
        sorted_masses = -np.sort(-masses, axis=-1)

        return sorted_masses

    def n_jet_vector_sum_pt(self, px: ak.Array, py: ak.Array, k: int) -> np.ndarray:
        combination_indices = np.array(list(combinations(range(self.n_jets), k)))

        vector_sum_pts = np.sqrt(
            px[:, combination_indices].sum(axis=-1) ** 2 +
            py[:, combination_indices].sum(axis=-1) ** 2
        )
        sorted_vector_sum_pts = -np.sort(-vector_sum_pts, axis=-1)

        return sorted_vector_sum_pts

    def flatten_features(self, features: dict[str, np.ndarray]) -> np.ndarray:
        flat_features = {}
        for feature, values in features.items():
            match values.ndim:
                case 1:
                    flat_features[feature] = values
                case 2:
                    for i in range(values.shape[1]):
                        flat_features[f"{feature}_{i+1}"] = values[:, i]
                case _:
                    raise ValueError(f"Invalid feature shape: {values.shape}")
        return flat_features

    def compute_all(self, data: ak.Array) -> dict[str, np.ndarray]:
        jet_pt = self.leading_jet_pt(data)
        jet_eta = self.leading_jet_eta(data)
        jet_phi = self.leading_jet_phi(data)

        jet_px = jet_pt * np.cos(jet_phi)
        jet_py = jet_pt * np.sin(jet_phi)
        jet_pz = jet_pt * np.sinh(jet_eta)
        jet_E = jet_pt * np.cosh(jet_eta)

        features = {
            "jet_multiplicity": self.jet_multiplicity(data),
            "leading_jet_pt": jet_pt,
            "leading_jet_eta": jet_eta,
            "leading_jet_phi": jet_phi,
            "delta_r": self.delta_r(jet_eta, jet_phi, jet_pt),
            "combined_invariant_mass": self.combined_invariant_mass(
                jet_px, jet_py, jet_pz, jet_E
            ),
        }

        for k in [2, 3]:
            features[f"{k}jet_invariant_mass"] = self.n_jet_invariant_mass(
                jet_px, jet_py, jet_pz, jet_E, k
            )
            features[f"{k}jet_vector_sum_pt"] = self.n_jet_vector_sum_pt(
                jet_px, jet_py, k
            )

        # Compute combined features
        mnj = features["combined_invariant_mass"]
        m3j = features["3jet_invariant_mass"]
        m2j = features["2jet_invariant_mass"]

        features[f"m3j_m{self.n_jets}j_ratio"] = np.divide(
            m3j.mean(axis=1, where=m3j != 0),
            mnj,
            out=np.zeros_like(mnj),
            where=mnj != 0
        )

        features[f"m2j_m{self.n_jets}j_ratio"] = np.divide(
            m2j.mean(axis=1, where=m2j != 0),
            mnj,
            out=np.zeros_like(mnj),
            where=mnj != 0
        )

        features["n_jet_pairs_near_w_mass"] = np.sum((m2j >= 60) & (m2j <= 100), axis=1)
        features["max_delta_r"] = np.max(features["delta_r"], axis=1)

        smallest_delta_r_indices = np.argmin(features["delta_r"], axis=1)
        features["smallest_delta_r_mass"] = np.choose(smallest_delta_r_indices, m2j.T)

        features["max_vector_sum_pt"] = np.max(features["2jet_vector_sum_pt"], axis=1)
        features.pop("3jet_vector_sum_pt")
        features.pop("2jet_vector_sum_pt")

        return self.flatten_features(features)

