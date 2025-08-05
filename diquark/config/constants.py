from pathlib import Path

ATLAS_TOTAL_LUMI = 3000 # fb^-1
CMS_TOTAL_LUMI = 3000 # fb^-1

DATA_KEYS = [
    'BKG:gg_bbbar',
    'BKG:gg_ccbar',
    'BKG:gg_gg',
    'BKG:qqbar_gg',
    'BKG:gg_qqbar',
    'BKG:qg_qg',
    'BKG:qqbar_bbbar',
    'BKG:qqbar_ccbar',
    'BKG:qq_qq',
    'BKG:qqbar_qqbarNew',
    'BKG:qq_hbb_hadronic',
    'BKG:gg_hbb_hadronic',
    'BKG:gg_Hg',
    'BKG:qg_Hq',
    # 'BKG:qqbar_Hg',
    # 'BKG:ff_H',
    # 'BKG:gg_H',
    'BKG:ff_HZ',
    'BKG:ff_HW',
    'BKG:ff_Hff',
    'BKG:ff_Hff2',
    'BKG:gg_Httbar',
    'BKG:qq_Httbar',
    'BKG:qg_Hq',
    'BKG:ffbar_Wgm',
    'BKG:qg_Wj_hadronic',
    'BKG:qqbar_Wj_hadronic',
    'BKG:ff_ZW_bkg',
    'BKG:ff_WW_bkg',
    'BKG:ff_gmZgmZ_bkg',
    'BKG:gg_ttbar_bkg_hadronic',
    'BKG:qq_ttbar_bkg_hadronic',
    'SIG:Suu'
]

DATA_KEYS_CODES = list(range(1, 15)) + list(range(18, 33))

COLOR_DICT = {
    'BKG:gg_bbbar': '#21f0b6',
    'BKG:gg_ccbar': '#b70d61',
    'BKG:gg_gg': '#60d11c',
    'BKG:qqbar_gg': '#922eb1',
    'BKG:gg_qqbar': '#c7e11f',
    'BKG:qg_qg': '#3f16f9',
    'BKG:qqbar_bbbar': '#699023',
    'BKG:qqbar_ccbar': '#fe74fe',
    'BKG:qq_qq': '#02531d',
    'BKG:qqbar_qqbarNew': '#fd6ca0',
    'BKG:qq_hbb_hadronic': '#54d7eb',
    'BKG:gg_hbb_hadronic': '#7c2b2a',
    'BKG:gg_Hg': '#aae3a4',
    'BKG:qg_Hq_loop': '#1e438d',
    # 'BKG:qqbar_Hg': '#f7931e',
    # 'BKG:ff_H': '#7e867b',
    # 'BKG:gg_H': '#b1c8eb',
    'BKG:ff_HZ': '#e8250c',
    'BKG:ff_HW': '#2f937a',
    'BKG:ff_Hff': '#c57c89',
    'BKG:ff_Hff2': '#ebc30e',
    'BKG:gg_Httbar': '#b69cfd',
    'BKG:qq_Httbar': '#e6d3a5',
    'BKG:qg_Hq': '#4787c9',
    'BKG:ffbar_Wgm': "#866609",
    'BKG:qg_Wj_hadronic': '#52ef99',
    'BKG:qqbar_Wj_hadronic': '#1e5c4a',
    'BKG:ff_ZW_bkg': '#a2e0dd',
    'BKG:ff_WW_bkg': '#395f97',
    'BKG:ff_gmZgmZ_bkg': '#f7931e',
    'BKG:gg_ttbar_bkg_hadronic': '#b1c8eb',
    'BKG:qq_ttbar_bkg_hadronic': '#7e867b',
    'BKG:sum': '#FF0000',
    'SIG:Suu': "#000000",
}

### Path dictionaries

BACKGROUNDS_DIR = Path('/data/iduminic/diquark-analysis/full-hadro/bkg/')
SIGNAL_DIR = Path('/data/iduminic/diquark-analysis/full-hadro/sgn/')

BACKGROUNDS_6JETS_DIR = BACKGROUNDS_DIR / '6jets/136/100k'
SIGNAL_ATLAS_136_DIR = SIGNAL_DIR / 'chi-chi/wb-wb/136/yuu-020/m_chi-2000/'

## m_{S_{uu}} = 6.5 TeV
ATLAS_136_6500_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_6500'

PATH_DICT_ATLAS_136_6500 = {
    **{
        key: ATLAS_136_6500_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_6500.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_7000_events.root'
}

## m_{S_{uu}} = 6.75 TeV
ATLAS_136_6750_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_6750'

PATH_DICT_ATLAS_136_6750 = {
    **{
        key: ATLAS_136_6750_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_6750.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_7250_events.root'
}

## m_{S_{uu}} = 7.0 TeV
ATLAS_136_7000_BKG_DIR = BACKGROUNDS_6JETS_DIR  / '136_7000'

PATH_DICT_ATLAS_136_7000 = {
    **{
        key: ATLAS_136_7000_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_7000.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_7500_events.root'
}

## m_{S_{uu}} = 7.25 TeV
ATLAS_136_7250_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_7250'

PATH_DICT_ATLAS_136_7250 = {
    **{
        key: ATLAS_136_7250_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_7250.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_7750_events.root'
}

## m_{S_{uu}} = 7.5 TeV
ATLAS_136_7500_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_7500'

PATH_DICT_ATLAS_136_7500 = {
    **{
        key: ATLAS_136_7500_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_7500.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_8000_events.root'
}

## m_{S_{uu}} = 7.75 TeV
ATLAS_136_7750_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_7750'

PATH_DICT_ATLAS_136_7750 = {
    **{
        key: ATLAS_136_7750_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_7750.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_8250.root'
}

## m_{S_{uu}} = 8.0 TeV
ATLAS_136_8000_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_8000'

PATH_DICT_ATLAS_136_8000 = {
    **{
        key: ATLAS_136_8000_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_8000.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_8500.root'
}

## m_{S_{uu}} = 8.25 TeV
ATLAS_136_8250_BKG_DIR = BACKGROUNDS_6JETS_DIR / '136_8250'

PATH_DICT_ATLAS_136_8250 = {
    **{
        key: ATLAS_136_8250_BKG_DIR / f'{DATA_KEYS_CODES[index]:02d}_{key.split(':')[-1]}.cmnd_13600_8250.root'
        for index, key in enumerate(DATA_KEYS)
        if key.startswith('BKG')
    },
    'SIG:Suu': SIGNAL_ATLAS_136_DIR / '136_8750.root'
}

### Cross-sections in femtobarns (fb)

CROSS_SECTION_ATLAS_136_6500 = {
    'BKG:gg_bbbar': 3.491E-02,
    'BKG:gg_ccbar': 3.206E-01,
    'BKG:gg_gg': 3.249E+08,
    'BKG:qqbar_gg': 8.525E+00,
    'BKG:gg_qqbar': 2.742E+00,
    'BKG:qg_qg': 4.618E+09,
    'BKG:qqbar_bbbar': 9.975E-04,
    'BKG:qqbar_ccbar': 1.002E-03,
    'BKG:qq_qq': 1.085E+10,
    'BKG:qqbar_qqbarNew': 3.005E-03,
    'BKG:qq_hbb_hadronic': 3.509E-09,
    'BKG:gg_hbb_hadronic': 3.399E-07,
    'BKG:gg_Hg': 1.359E-02,
    'BKG:qg_Hq': 1.157E-01,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 7.241E-07,
    'BKG:ff_HW': 1.041E-06,
    'BKG:ff_Hff': 2.881E-01,
    'BKG:ff_Hff2': 6.119E-01,
    'BKG:gg_Httbar': 7.088E-06,
    'BKG:qq_Httbar': 6.695E-06,
    'BKG:qg_Hq': 8.029E-09,
    'BKG:ffbar_Wgm': 8.854E-04,
    'BKG:qg_Wj_hadronic': 2.279E-01,
    'BKG:qqbar_Wj_hadronic': 9.876E-02,
    'BKG:ff_ZW_bkg': 4.024E-04,
    'BKG:ff_WW_bkg': 9.666E-04,
    'BKG:ff_gmZgmZ_bkg': 9.065E-05,
    'BKG:gg_ttbar_bkg_hadronic': 5.051E-04,
    'BKG:qq_ttbar_bkg_hadronic': 4.646E-04,
    'SIG:Suu': 1.468E-02
}

CROSS_SECTION_ATLAS_136_6750 = {
    'BKG:gg_bbbar': 1.847E-02,
    'BKG:gg_ccbar': 1.735E-01,
    'BKG:gg_gg': 1.912E+08,
    'BKG:qqbar_gg': 5.207E+00,
    'BKG:gg_qqbar': 1.499E+00,
    'BKG:qg_qg': 3.054E+09,
    'BKG:qqbar_bbbar': 5.411E-04,
    'BKG:qqbar_ccbar': 5.413E-04,
    'BKG:qq_qq': 8.010E+09,
    'BKG:qqbar_qqbarNew': 1.622E-03,
    'BKG:qq_hbb_hadronic': 1.948E-09,
    'BKG:gg_hbb_hadronic': 1.812E-07,
    'BKG:gg_Hg': 7.900E-03,
    'BKG:qg_Hq': 7.526E-02,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 3.910E-07,
    'BKG:ff_HW': 5.306E-07,
    'BKG:ff_Hff': 1.964E-01,
    'BKG:ff_Hff2': 4.054E-01,
    'BKG:gg_Httbar': 3.753E-06,
    'BKG:qq_Httbar': 3.673E-06,
    'BKG:qg_Hq': 4.145E-09,
    'BKG:ffbar_Wgm': 4.993E-04,
    'BKG:qg_Wj_hadronic': 1.387E-01,
    'BKG:qqbar_Wj_hadronic': 5.610E-02,
    'BKG:ff_ZW_bkg': 2.151E-04,
    'BKG:ff_WW_bkg': 5.554E-04,
    'BKG:ff_gmZgmZ_bkg': 5.086E-05,
    'BKG:gg_ttbar_bkg_hadronic': 2.611E-04,
    'BKG:qq_ttbar_bkg_hadronic': 2.519E-04,
    'SIG:Suu': 9.512E-03
}

CROSS_SECTION_ATLAS_136_7000 = {
    'BKG:gg_bbbar': 9.659E-03,
    'BKG:gg_ccbar': 9.270E-02,
    'BKG:gg_gg': 1.110E+08,
    'BKG:qqbar_gg': 3.138E+00,
    'BKG:gg_qqbar': 8.093E-01,
    'BKG:qg_qg': 1.992E+09,
    'BKG:qqbar_bbbar': 2.877E-04,
    'BKG:qqbar_ccbar': 2.892E-04,
    'BKG:qq_qq': 5.813E+09,
    'BKG:qqbar_qqbarNew': 8.690E-04,
    'BKG:qq_hbb_hadronic': 1.051E-09,
    'BKG:gg_hbb_hadronic': 9.468E-08,
    'BKG:gg_Hg': 4.512E-03,
    'BKG:qg_Hq': 4.824E-02,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 2.079E-07,
    'BKG:ff_HW': 2.662E-07,
    'BKG:ff_Hff': 1.320E-01,
    'BKG:ff_Hff2': 2.631E-01,
    'BKG:gg_Httbar': 1.964E-06,
    'BKG:qq_Httbar': 1.983E-06,
    'BKG:qg_Hq': 2.124E-09,
    'BKG:ffbar_Wgm': 2.763E-04,
    'BKG:qg_Wj_hadronic': 8.325E-02,
    'BKG:qqbar_Wj_hadronic': 3.116E-02,
    'BKG:ff_ZW_bkg': 1.127E-04,
    'BKG:ff_WW_bkg': 3.148E-04,
    'BKG:ff_gmZgmZ_bkg': 2.821E-05,
    'BKG:gg_ttbar_bkg_hadronic': 1.336E-04,
    'BKG:qq_ttbar_bkg_hadronic': 1.343E-04,
    'SIG:Suu': 6.125E-03
}

CROSS_SECTION_ATLAS_136_7250 = {
    'BKG:gg_bbbar': 4.989E-03,
    'BKG:gg_ccbar': 4.866E-02,
    'BKG:gg_gg': 6.296E+07,
    'BKG:qqbar_gg': 1.890E+00,
    'BKG:gg_qqbar': 4.296E-01,
    'BKG:qg_qg': 1.280E+09,
    'BKG:qqbar_bbbar': 1.524E-04,
    'BKG:qqbar_ccbar': 1.521E-04,
    'BKG:qq_qq': 4.196E+09,
    'BKG:qqbar_qqbarNew': 4.554E-04,
    'BKG:qq_hbb_hadronic': 5.594E-10,
    'BKG:gg_hbb_hadronic': 4.931E-08,
    'BKG:gg_Hg': 2.544E-03,
    'BKG:qg_Hq': 3.048E-02,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 1.094E-07,
    'BKG:ff_HW': 1.321E-07,
    'BKG:ff_Hff': 8.740E-02,
    'BKG:ff_Hff2': 1.691E-01,
    'BKG:gg_Httbar': 1.017E-06,
    'BKG:qq_Httbar': 1.057E-06,
    'BKG:qg_Hq': 1.083E-09,
    'BKG:ffbar_Wgm': 1.503E-04,
    'BKG:qg_Wj_hadronic': 4.946E-02,
    'BKG:qqbar_Wj_hadronic': 1.700E-02,
    'BKG:ff_ZW_bkg': 5.824E-05,
    'BKG:ff_WW_bkg': 1.761E-04,
    'BKG:ff_gmZgmZ_bkg': 1.544E-05,
    'BKG:gg_ttbar_bkg_hadronic': 6.757E-05,
    'BKG:qq_ttbar_bkg_hadronic': 7.087E-05,
    'SIG:Suu': 3.863E-03
}

CROSS_SECTION_ATLAS_136_7500 = {
    'BKG:gg_bbbar': 2.544E-03,
    'BKG:gg_ccbar': 2.520E-02,
    'BKG:gg_gg': 3.505E+07,
    'BKG:qqbar_gg': 1.111E+00,
    'BKG:gg_qqbar': 2.246E-01,
    'BKG:qg_qg': 8.077E+08,
    'BKG:qqbar_bbbar': 7.885E-05,
    'BKG:qqbar_ccbar': 7.902E-05,
    'BKG:qq_qq': 2.985E+09,
    'BKG:qqbar_qqbarNew': 2.369E-04,
    'BKG:qq_hbb_hadronic': 2.932E-10,
    'BKG:gg_hbb_hadronic': 2.519E-08,
    'BKG:gg_Hg': 1.405E-03,
    'BKG:qg_Hq_loop': 1.895E-02,
    'BKG:qqbar_Hg': 0,
    'BKG:ff_H': 0,
    'BKG:gg_H': 0,
    'BKG:ff_HZ': 5.641E-08,
    'BKG:ff_HW': 6.477E-08,
    'BKG:ff_Hff': 5.714E-02,
    'BKG:ff_Hff2': 1.066E-01,
    'BKG:gg_Httbar': 5.191E-07,
    'BKG:qq_Httbar': 5.557E-07,
    'BKG:qg_Hq': 5.505E-10,
    'BKG:ffbar_Wgm': 7.989E-05,
    'BKG:qg_Wj_hadronic': 2.895E-02,
    'BKG:qqbar_Wj_hadronic': 9.081E-03,
    'BKG:ff_ZW_bkg': 2.958E-05,
    'BKG:ff_WW_bkg': 9.644E-05,
    'BKG:ff_gmZgmZ_bkg': 8.316E-06,
    'BKG:gg_ttbar_bkg_hadronic': 3.372E-05,
    'BKG:qq_ttbar_bkg_hadronic': 3.671E-05,
    'SIG:Suu': 2.406E-03,
}

CROSS_SECTION_ATLAS_136_7750 = {
    'BKG:gg_bbbar': 1.275E-03,
    'BKG:gg_ccbar': 1.275E-02,
    'BKG:gg_gg': 1.899E+07,
    'BKG:qqbar_gg': 6.427E-01,
    'BKG:gg_qqbar': 1.148E-01,
    'BKG:qg_qg': 5.019E+08,
    'BKG:qqbar_bbbar': 4.022E-05,
    'BKG:qqbar_ccbar': 4.026E-05,
    'BKG:qq_qq': 2.094E+09,
    'BKG:qqbar_qqbarNew': 1.205E-04,
    'BKG:qq_hbb_hadronic': 1.525E-10,
    'BKG:gg_hbb_hadronic': 1.274E-08,
    'BKG:gg_Hg': 7.605E-04,
    'BKG:qg_Hq': 1.157E-02,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 2.871E-08,
    'BKG:ff_HW': 3.129E-08,
    'BKG:ff_Hff': 3.659E-02,
    'BKG:ff_Hff2': 6.587E-02,
    'BKG:gg_Httbar': 2.607E-07,
    'BKG:qq_Httbar': 2.860E-07,
    'BKG:qg_Hq': 2.792E-10,
    'BKG:ffbar_Wgm': 4.152E-05,
    'BKG:qg_Wj_hadronic': 1.670E-02,
    'BKG:qqbar_Wj_hadronic': 4.722E-03,
    'BKG:ff_ZW_bkg': 1.470E-05,
    'BKG:ff_WW_bkg': 5.191E-05,
    'BKG:ff_gmZgmZ_bkg': 4.421E-06,
    'BKG:gg_ttbar_bkg_hadronic': 1.662E-05,
    'BKG:qq_ttbar_bkg_hadronic': 1.874E-05,
    'SIG:Suu': 1.469E-03
}

CROSS_SECTION_ATLAS_136_8000 = {
    'BKG:gg_bbbar': 6.281E-04,
    'BKG:gg_ccbar': 6.362E-03,
    'BKG:gg_gg': 1.004E+07,
    'BKG:qqbar_gg': 3.639E-01,
    'BKG:gg_qqbar': 5.715E-02,
    'BKG:qg_qg': 3.058E+08,
    'BKG:qqbar_bbbar': 2.016E-05,
    'BKG:qqbar_ccbar': 2.013E-05,
    'BKG:qq_qq': 1.450E+09,
    'BKG:qqbar_qqbarNew': 6.053E-05,
    'BKG:qq_hbb_hadronic': 7.679E-11,
    'BKG:gg_hbb_hadronic': 6.318E-09,
    'BKG:gg_Hg': 4.014E-04,
    'BKG:qg_Hq': 6.973E-03,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 1.447E-08,
    'BKG:ff_HW': 1.503E-08,
    'BKG:ff_Hff': 2.316E-02,
    'BKG:ff_Hff2': 3.986E-02,
    'BKG:gg_Httbar': 1.287E-07,
    'BKG:qq_Httbar': 1.448E-07,
    'BKG:qg_Hq': 1.411E-10,
    'BKG:ffbar_Wgm': 2.102E-05,
    'BKG:qg_Wj_hadronic': 9.486E-03,
    'BKG:qqbar_Wj_hadronic': 2.401E-03,
    'BKG:ff_ZW_bkg': 7.209E-06,
    'BKG:ff_WW_bkg': 2.738E-05,
    'BKG:ff_gmZgmZ_bkg': 2.298E-06,
    'BKG:gg_ttbar_bkg_hadronic': 8.018E-06,
    'BKG:qq_ttbar_bkg_hadronic': 9.390E-06,
    'SIG:Suu': 8.782E-04
}

CROSS_SECTION_ATLAS_136_8250 = {
    'BKG:gg_bbbar': 3.048E-04,
    'BKG:gg_ccbar': 3.087E-03,
    'BKG:gg_gg': 5.158E+06,
    'BKG:qqbar_gg': 2.010E-01,
    'BKG:gg_qqbar': 2.769E-02,
    'BKG:qg_qg': 1.823E+08,
    'BKG:qqbar_bbbar': 9.899E-06,
    'BKG:qqbar_ccbar': 9.887E-06,
    'BKG:qq_qq': 9.809E+08,
    'BKG:qqbar_qqbarNew': 2.974E-05,
    'BKG:qq_hbb_hadronic': 3.828E-11,
    'BKG:gg_hbb_hadronic': 3.063E-09,
    'BKG:gg_Hg': 2.055E-04,
    'BKG:qg_Hq': 4.081E-03,
    'BKG:qqbar_Hg': 0.000E+00,
    'BKG:ff_H': 0.000E+00,
    'BKG:gg_H': 0.000E+00,
    'BKG:ff_HZ': 7.076E-09,
    'BKG:ff_HW': 7.177E-09,
    'BKG:ff_Hff': 1.432E-02,
    'BKG:ff_Hff2': 2.353E-02,
    'BKG:gg_Httbar': 6.222E-08,
    'BKG:qq_Httbar': 7.170E-08,
    'BKG:qg_Hq': 7.096E-11,
    'BKG:ffbar_Wgm': 1.040E-05,
    'BKG:qg_Wj_hadronic': 5.273E-03,
    'BKG:qqbar_Wj_hadronic': 1.189E-03,
    'BKG:ff_ZW_bkg': 3.483E-06,
    'BKG:ff_WW_bkg': 1.424E-05,
    'BKG:ff_gmZgmZ_bkg': 1.176E-06,
    'BKG:gg_ttbar_bkg_hadronic': 3.812E-06,
    'BKG:qq_ttbar_bkg_hadronic': 4.603E-06,
    'SIG:Suu': 5.148E-04
}
