#!/usr/bin/env bash

# Exit on error, print commands
set -ex

# for mass_cut in 6500 6750 7000 7250 7500 7750 8000 8250
# do
#     python3 diquark/analysis.py -c "diquark/config/New_Features/ATLAS_136_${mass_cut}_32j_5f.yaml"
# done

# python3 diquark/analysis.py -c "diquark/config/New_Features/ATLAS_136_7500_6j_5f.yaml"

python3 diquark/analysis.py -c "diquark/config/New_Features/ATLAS_136_7500_32j_5f.yaml"
