import pandas as pd

cross_sections_file_path = 'diquark_cross-sections_bkg_atlas.csv'

# Read the cross-sections CSV file
df = pd.read_csv(cross_sections_file_path, sep=',', header=None, skiprows=3)

# Delete unneeded rows and columns
df = df.truncate(after=31, axis='index')
df = df.truncate(after=11, axis='columns')

# Relabel the remaining columns
mass_cuts = [
    '5500',
    '6000',
    #'6250',
    '6500',
    '6750',
    '7000',
    '7250',
    '7500',
    '7750',
    '8000',
    '8250',
]
df.columns = [
    'id',
    'process',
    *mass_cuts
]

# Get rid of the "b.##" column and instead index rows by process
df = df.drop(columns=['id'])
df = df.set_index('process')

for mass_cut in mass_cuts:
    cross_sections = df[mass_cut]

    cross_sections = cross_sections.str.replace(',', '.')
    cross_sections[cross_sections == '-'] = '0'

    cross_sections = pd.to_numeric(cross_sections)

    print(f"CROSS_SECTION_ATLAS_136_{mass_cut} =", "{")
    for process, section in cross_sections.items():
        print(f"    'BKG:{process}': {section:.3E},")

    print("}")
