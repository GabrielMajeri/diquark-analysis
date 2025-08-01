from math import comb
import numpy as np
import awkward as ak

class FeatureExtractor:
    def __init__(self, n_jets: int):
        self.n_jets = n_jets
        self.feature_names = self._generate_feature_names()

    def _flattened_feature_names(self, name: str) -> list[str]:
        return [
            f"{name}_min",
            f"{name}_mean",
            f"{name}_stddev",
            f"{name}_max",
        ]

    def _generate_feature_names(self) -> list[str]:
        return [
            "jet_multiplicity",
            *self._flattened_feature_names("p_T"),
            *self._flattened_feature_names("eta"),
            *self._flattened_feature_names("phi"),
            *self._flattened_feature_names("delta_r"),
            "sphericity",
            "aplanarity",
            "centrality",
            "total_energy",
            "total_p_T",
            "combined_invariant_mass",
            *self._flattened_feature_names("m2j"),
            *self._flattened_feature_names("m3j"),
            *self._flattened_feature_names("m6j"),
            *self._flattened_feature_names("vector_sum_p_T_2j"),
            *self._flattened_feature_names("vector_sum_p_T_3j"),
            *self._flattened_feature_names("vector_sum_p_T_6j"),
            "n_jet_pairs_near_w_mass",
            *self._flattened_feature_names("chi2_first_component"),
            *self._flattened_feature_names("chi2_second_component"),
            *self._flattened_feature_names("chi2_third_component"),
        ]

    def _pad_jet_array(self, array: ak.Array):
        padded = ak.pad_none(array, self.n_jets, clip=True)
        filled = ak.fill_none(padded, 0.0)
        return filled.to_numpy()

    def event_shape_eigenvalues(self, mask: np.ndarray, p_x: ak.Array, p_y: ak.Array, p_z: ak.Array):
        p_x_np = self._pad_jet_array(p_x)
        p_y_np = self._pad_jet_array(p_y)
        p_z_np = self._pad_jet_array(p_z)

        momenta = np.stack((p_x_np, p_y_np, p_z_np))
        momenta = np.moveaxis(momenta, 0, -1)
        total = (momenta * momenta).sum(axis=-1).sum(axis=-1)

        S = np.zeros((mask.sum(), 3, 3))
        for i in range(3):
            for j in range(3):
                S[:, i, j] = np.vecdot(momenta[mask, :, i], momenta[mask, :, j]) / total[mask]

        eigenvalues = np.linalg.eigvalsh(S)
        eigenvalues = np.sort(eigenvalues, axis=-1)

        return eigenvalues

    def jet_multiplicity(self, data: ak.Array) -> np.ndarray:
        return ak.to_numpy(data["Jet"])

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

    def combined_invariant_mass(self, p_x: ak.Array, p_y: ak.Array, p_z: ak.Array, total_energy: np.ndarray) -> np.ndarray:
        p_x_total = ak.sum(p_x, axis=-1).to_numpy()
        p_y_total = ak.sum(p_y, axis=-1).to_numpy()
        p_z_total = ak.sum(p_z, axis=-1).to_numpy()

        total_mass_squared = total_energy**2 - p_x_total**2 - p_y_total**2 - p_z_total**2

        mass = np.sqrt(
            total_mass_squared,
            out=np.zeros_like(total_energy, dtype=np.float64),
            where=total_mass_squared >= 0
        )
        return np.nan_to_num(mass)

    def n_jet_invariant_mass(self, p_x: ak.Array, p_y: ak.Array, p_z: ak.Array, E: ak.Array, k: int) -> np.ndarray:
        combination_indices = ak.unzip(ak.argcombinations(E, n=k))

        raw_masses = np.sqrt(
            sum(E[combination_indices[i]] for i in range(k)) ** 2 -
            sum(p_x[combination_indices[i]] for i in range(k)) ** 2 -
            sum(p_y[combination_indices[i]] for i in range(k)) ** 2 -
            sum(p_z[combination_indices[i]] for i in range(k)) ** 2
        )

        return np.nan_to_num(raw_masses)

    def n_jet_vector_sum_pt(self, p_x: ak.Array, p_y: ak.Array, k: int) -> np.ndarray:
        combination_indices = ak.unzip(ak.argcombinations(p_x, n=k))

        raw_vector_sum_pts = np.sqrt(
            sum(p_x[combination_indices[i]] for i in range(k)) ** 2 +
            sum(p_y[combination_indices[i]] for i in range(k)) ** 2
        )

        return np.nan_to_num(raw_vector_sum_pts)

    def flatten_feature(self, name: str, data: ak.Array) -> dict:
        return {
            f"{name}_min": ak.min(data, axis=-1, mask_identity=True).to_numpy().filled(0.0),
            f"{name}_mean": ak.mean(data, axis=-1, mask_identity=True).to_numpy().filled(0.0),
            f"{name}_stddev": ak.std(data, axis=-1, mask_identity=True).to_numpy().filled(0.0),
            f"{name}_max": ak.max(data, axis=-1, mask_identity=True).to_numpy().filled(0.0),
        }

    def compute_all(self, data: ak.Array) -> dict[str, np.ndarray]:
        features = {}

        num_jets = self.jet_multiplicity(data)
        features["jet_multiplicity"] = num_jets

        non_zero_jets_mask = num_jets > 0

        # Extract jet 4-vector components
        p_T = data["Jet/Jet.PT"]
        eta = data["Jet/Jet.Eta"]
        phi = data["Jet/Jet.Phi"]

        features |= self.flatten_feature("p_T", p_T)
        features |= self.flatten_feature("eta", eta)
        features |= self.flatten_feature("phi", phi)

        delta_r = self.delta_r(self._pad_jet_array(eta), self._pad_jet_array(phi), self._pad_jet_array(p_T))
        features |= self.flatten_feature("delta_r", delta_r)

        # Compute components in Cartesian coordinates
        p_x = p_T * np.cos(phi)
        p_y = p_T * np.sin(phi)
        p_z = p_T * np.sinh(eta)

        eigenvalues = self.event_shape_eigenvalues(non_zero_jets_mask, p_x, p_y, p_z)

        # Compute sphericity and aplanarity
        lambda_2 = eigenvalues[:, 1]
        lambda_3 = eigenvalues[:, 0]

        sphericity = np.zeros_like(num_jets, dtype=np.float64)
        aplanarity = np.zeros_like(num_jets, dtype=np.float64)

        sphericity[non_zero_jets_mask] = 3/2 * (lambda_2 + lambda_3)
        aplanarity[non_zero_jets_mask] = 3/2 * lambda_3

        features["sphericity"] = sphericity
        features["aplanarity"] = aplanarity

        # Compute jet energy
        energy = p_T * np.cosh(eta)

        # Compute centrality
        total_energy = ak.sum(energy, axis=-1).to_numpy()
        total_p_T = ak.sum(p_T, axis=-1).to_numpy()
        centrality = np.divide(
            total_p_T, total_energy,
            out=np.zeros_like(total_energy, dtype=np.float64),
            where=total_energy > 0,
        )

        features["centrality"] = centrality

        features["total_energy"] = total_energy
        features["total_p_T"] = total_p_T

        combined_invariant_mass = self.combined_invariant_mass(p_x, p_y, p_z, total_energy)
        features["combined_invariant_mass"] = combined_invariant_mass

        m2j = self.n_jet_invariant_mass(p_x, p_y, p_z, energy, k=2)
        m3j = self.n_jet_invariant_mass(p_x, p_y, p_z, energy, k=3)
        m6j = self.n_jet_invariant_mass(p_x, p_y, p_z, energy, k=6)

        vector_sum_p_T_2j = self.n_jet_vector_sum_pt(p_x, p_y, k=2)
        vector_sum_p_T_3j = self.n_jet_vector_sum_pt(p_x, p_y, k=3)
        vector_sum_p_T_6j = self.n_jet_vector_sum_pt(p_x, p_y, k=6)

        features |= self.flatten_feature("m2j", m2j)
        features |= self.flatten_feature("m3j", m3j)
        features |= self.flatten_feature("m6j", m6j)

        features |= self.flatten_feature("vector_sum_p_T_2j", vector_sum_p_T_2j)
        features |= self.flatten_feature("vector_sum_p_T_3j", vector_sum_p_T_3j)
        features |= self.flatten_feature("vector_sum_p_T_6j", vector_sum_p_T_6j)

        # Compute combined features
        features["n_jet_pairs_near_w_mass"] = ak.sum((m2j >= 60) & (m2j <= 100), axis=-1)

        # Compute \chi^2 score with known-mass particles
        m_W = 80.3692
        sigma_W = 20

        m_chi = 2000
        sigma_chi = 2/100 * m_chi

        m_S = 8000
        sigma_S = 100

        chi2_first_component = ((m2j - m_W) / sigma_W) ** 2
        chi2_second_component = ((m3j - m_chi) / sigma_chi) ** 2
        chi2_third_component = ((m6j - m_S) / sigma_S) ** 2

        features |= self.flatten_feature("chi2_first_component", chi2_first_component)
        features |= self.flatten_feature("chi2_second_component", chi2_second_component)
        features |= self.flatten_feature("chi2_third_component", chi2_third_component)

        return features

