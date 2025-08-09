import functools

import uproot
import awkward as ak

from tqdm.contrib.concurrent import thread_map

from diquark.config.constants import DATA_KEYS, BKG_4JET_DATA_KEYS, BKG_MULTIJET_DATA_KEYS

class DataLoader:

    def __init__(self, path_dict: dict[str, str], index_start=0, index_stop=None):
        self.default_branches = [
            "Jet",
            "Jet/Jet.PT",
            "Jet/Jet.Eta",
            "Jet/Jet.Phi",
            "Jet/Jet.BTag",
            "Particle/Particle.PID",
            "Particle/Particle.Status",
            "Particle/Particle.Mass",
        ]
        self.path_dict = path_dict
        self.index_start = index_start
        self.index_stop = index_stop

    def filter_fbits(self, branches: list[str]) -> list[str]:
        """Filter out branch names containing 'fBits'."""
        return [b for b in branches if "fBits" not in b]

    def read_jet_delphes(self, filename: str, branches: list[str] = None) -> ak.Array:
        """Read a delphes output TTree from a ROOT file into an awkward array."""
        if branches is None:
            branches = self.default_branches

        with uproot.open(filename) as f:
            tree = f["Delphes"]
            branches = self.filter_fbits(branches)
            return tree.arrays(branches, library="ak", entry_start=self.index_start, entry_stop=self.index_stop)

    def lower_cut_suu_mass(self, arr: ak.Array, mass: float) -> ak.Array:
        """Filter out jets with mass less than the given value."""
        mask = (arr["Particle/Particle.PID"] == 9936661) & (arr["Particle/Particle.Status"] == 22)
        masses = arr["Particle/Particle.Mass"][mask].to_numpy()
        print(f"Fraction of events passing mass cut: {(masses >= mass).sum() / len(masses):.2f}")
        return arr[(masses > mass).flatten()]

    def _load_dataset(self, key, mass_cut: float = None):
        arr = self.read_jet_delphes(self.path_dict[key])

        if key.startswith("SIG") and mass_cut is not None:
            arr = self.lower_cut_suu_mass(arr, mass_cut)

        return key, arr

    def load_data(self, mass_cut: float = None) -> dict[str, ak.Array]:
        """Load all datasets specified in DATA_KEYS."""

        # Load the datasets in parallel
        load_dataset = functools.partial(self._load_dataset, mass_cut=mass_cut)
        data_keys = DATA_KEYS + BKG_4JET_DATA_KEYS + BKG_MULTIJET_DATA_KEYS
        datasets = thread_map(load_dataset, data_keys, max_workers=64, desc="Loading data")

        self.datasets = dict(datasets)

        return self.datasets

