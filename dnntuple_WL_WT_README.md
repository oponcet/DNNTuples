# Contenu de dnntuple_WL.root et dnntuple_WT.root

Ntuples DNNTuples (AK8 fat jets, VBS W→qq boosté) pour le tagger de polarisation du W (WL vs WT), au format attendu par GloParT.

## Production

| | WL | WT |
|---|---|---|
| Sample | VBSWLWLToJets_5f_LO_FXFX_Boost_Run3Summer23 | VBSWTWTToJets_5f_LO_FXFX_Boost_1_Run3Summer23 |
| Fichiers MiniAOD | 22 | 22 |
| Jets (entrées du tree) | 5960 | 7168 |
| Jets avec `fj_isW==1` | 4190 | 3633 |
| Branches | 223 | 223 (identiques à WL) |
| Config cmsRun | `Ntupler/test/DeepNtuplizerAK8WL.py` | `Ntupler/test/DeepNtuplizerAK8WT.py` |

- Options : `isTrainSample=0 addLowLevel=1` (`addLowLevel=1` est nécessaire pour les branches cpf/npf/sv).
- Code : branche `Wpol_tagger` (base `dev-haa-nanov15` + labels WT/WL + variables de polarisation), commit `48f863a`.
- Soumission : `condor/submit_wL.jdl`, `condor/submit_wT.jdl` (1 job par sample, boucle sur les 22 fichiers). Sorties brutes `dnntuple_raw_{WL,WT}_{0..21}.root`, mergées avec `hadd` en `dnntuple_{WL,WT}.root`.
- Structure : un seul TTree, `deepntuplizer/tree`, **1 entrée = 1 fat jet AK8** (slimmedJetsAK8, Puppi, R=0.8, pT > 150 GeV, |eta| < 2.4). Sélection effective : pT de 200 à ~2300 GeV, médiane ~300 GeV.
- Les branches `vector<float>` ont une longueur variable par jet (nombre de constituants). Pour GloParT, tronquer/padder à 90 (cpf), 60 (npf), 10 (sv), triés par pT (cpf/npf) ou par significance de dxy (sv).

## Labels WT / WL et variables de polarisation

| Branche | Type | Description |
|---|---|---|
| `sample_isWL` | int | 1 pour tous les jets du sample WL (le nom du fichier d'entrée contient `WL`), 0 sinon |
| `sample_isWT` | int | 1 pour tous les jets du sample WT, 0 sinon |
| `fj_ptheta` | float | \|E_sj1 − E_sj2\| / \|p_jet\| (asymétrie d'énergie des 2 subjets soft-drop). Vaut -99 si le jet n'a pas 2 subjets (23 jets WL, 73 jets WT) |
| `fj_zj` | float | pT du subjet leader / pT du jet. Vaut -99 si moins de 2 subjets |

Le label de polarisation est porté par `sample_isWL` / `sample_isWT` (par sample), pas par jet : pour l'entraînement, ne garder que les jets avec `fj_isW==1` (W gen-matché hadronique).

## Truth / labels de saveur

`fj_label` est un index dans la liste de labels (mode `isMDTagger=False`) :

| Indices | Labels |
|---|---|
| 0–16 | `Top_*` (bWcs, bWqq, bWc, bWs, bWq, bWev, bWmv, bWtauev, bWtaumv, bWtauhv, Wcs, Wqq, Wev, Wmv, Wtauev, Wtaumv, Wtauhv) |
| 17–29 | `H_*` (bb, cc, ss, qq, bc, bs, cs, gg, ee, mm, tauhtaue, tauhtaum, tauhtauh) |
| 30–36 | `W_*` (cs, qq, ev, mv, tauev, taumv, tauhv) → **30 = W_cs, 31 = W_qq** |
| 37–40 | `Z_*` (bb, cc, ss, qq) |
| 41–45 | `QCD_*` (bb, cc, b, c, others) → 45 = jet non matché |
| 46–50 | labels de fond Haa (prompt, Non_prompt, p_p, p_Np, Np_Np) |

Répartition observée : WL = 2044 (W_cs) + 2146 (W_qq) + 638 (Z_qq) + 657 QCD + reste (labels 46–50) ; WT = 1757 (W_cs) + 1876 (W_qq) + 2057 QCD + reste. Tous les jets ne sont donc pas des W matchés : filtrer sur `fj_isW`.

## Liste complète des branches (223)

### Événement / jet (`jet_*`, 21 branches)
`event_no` (uint), `jet_no` (uint, index du jet dans l'événement), `npv`, `ntrueInt`, `rho`, `jet_pt` (non corrigé), `jet_corr_pt`, `jet_eta`, `jet_phi`, `jet_tightId`, `gen_pt`, `Delta_gen_pt`,
flavour du jet (int) : `isB`, `isBB`, `isC`, `isG`, `isLeptonicB`, `isLeptonicB_C`, `isS`, `isUD`, `isUndefined`.

### Cinématique et labels du fat jet (`fj_*`)
- Cinématique : `fj_pt`, `fj_eta`, `fj_phi`, `fj_mass`, `fj_energy`
- Soft drop : `fj_sdmass`, `fj_sdmass_fromsubjets`, `fj_uncorrsdmass`, `fj_corrsdmass`, `fj_rho`, `fj_n_sdsubjets`
- Substructure : `fj_tau1`, `fj_tau2`, `fj_tau3`, `fj_tau21`, `fj_tau32`, `fj_ptDR`, `fj_relptdiff`, `fj_sdn2`, `fj_doubleb`
- Subjet 1 (`fj_sdsj1_*`) et subjet 2 (`fj_sdsj2_*`) : `pt`, `eta`, `phi`, `mass`, `csv`, `ptD`, `axis1`, `axis2`, `mult`
- Labels truth (int) : `fj_label`, `fj_isTop`, `fj_isW`, `fj_isZ`, `fj_isH2p`, `fj_isHWW`, `fj_isHZZ`, `fj_isQCD`, `fj_isBB`, `fj_isNonBB`, `fj_nbHadrons`, `fj_ncHadrons`
- Polarisation : `fj_ptheta`, `fj_zj`

### Gen-level (pour cos θ*)
- W gen matché : `fj_gen_pt`, `fj_gen_eta`, `fj_gen_phi`, `fj_gen_mass`, `fj_gen_pid` (±24 ⇒ signe/charge du W, 0 si non matché), `fj_gen_deltaR` (ΔR jet–W gen, 999 si non matché)
- Fille 1 du W (quark) : `fj_gendau1_pt`, `_eta`, `_phi`, `_mass`, `_pid`, `_deltaR`
- Fille 2 du W (quark) : `fj_gendau2_pt`, `_eta`, `_phi`, `_mass`, `_pid`, `_deltaR`
- Somme des particules gen dures dans le jet : `fj_genparts_pt`, `_eta`, `_phi`, `_mass` ; `fj_genpart1_pid/pt/deltaR`, `fj_genpart2_pid/pt/deltaR`, `fj_genpart3_pid`, `fj_genpart4_pid`
- Régression jet/masse : `fj_genjet_pt`, `fj_genjet_mass`, `fj_genjet_sdmass`, `fj_genjet_sdmass_sqrt`, `fj_genjet_targetmass`, `fj_genjet_nomu_pt`, `fj_genjet_nomu_mass`, `fj_genjet_nomu_sdmass`, `fj_genOverReco_pt`, `_pt_null`, `_mass`, `_mass_null`, `_sdmass`, `_sdmass_null`, `fj_genOverReco_nomu_pt_null`, `_nomu_mass_null`, `_nomu_sdmass_null`

Non présent : les 2 jets de tagging VBS/VBF (aucune collection AK4 n'est lue), donc pas de cos θ* dans le référentiel du système diboson.

### Flags de sample (int)
`sample_isWL`, `sample_isWT`, `sample_isQCD`, `sample_isTTBar`, `sample_isHVV2DVarMass`, `sample_use_pythia`, `sample_use_herwig`, `sample_use_madgraph`, `sample_useReclusteredJets`

### Constituants chargés + lost tracks : `cpfcandlt_*` (`vector<float>`, 44 branches), compteurs `n_cpfcands`, `n_lts` (int)
- Quadri-vecteur : `px`, `py`, `pz`, `energy`
- Cinématique : `pt_nopuppi`, `pt_log_nopuppi`, `e_log_nopuppi`, `etarel`, `phirel`, `abseta`, `puppiw`, `drminsvin`, `dr_uncorrsj1`, `dr_uncorrsj2`
- Identité : `charge`, `isEl`, `isMu`, `isChargedHad`, `isLostTrack`
- Association vertex / qualité : `VTX_ass`, `fromPV`, `lostInnerHits`, `trackHighPurity`, `normchi2`, `quality`, `hcalFrac`, `hcalFracCalib`
- Impact parameters : `dz`, `dzsig`, `dxy`, `dxysig`
- b-tag track : `btagEtaRel`, `btagPtRel`, `btagPtRatio`, `btagPParRatio`, `btagSip3dVal`, `btagSip3dSig`, `btagJetDistVal`
- Couches de détecteur : `pixelBarrelLayersWithMeasurement`, `pixelEndcapLayersWithMeasurement`, `stripTIBLayersWithMeasurement`, `stripTIDLayersWithMeasurement`, `stripTOBLayersWithMeasurement`, `stripTECLayersWithMeasurement`

### Constituants neutres : `npfcand_*` (`vector<float>`, 18 branches), compteur `n_npfcands` (int)
`px`, `py`, `pz`, `energy`, `pt_nopuppi`, `pt_log_nopuppi`, `e_log_nopuppi`, `etarel`, `phirel`, `abseta`, `puppiw`, `drminsvin`, `dr_uncorrsj1`, `dr_uncorrsj2`, `isGamma`, `isNeutralHad`, `hcalFrac`, `hcalFracCalib`

### Vertex secondaires : `sv_*` (`vector<float>`, 27 branches), compteurs `n_sv` (int), `nsv` (float)
`px`, `py`, `pz`, `energy`, `pt`, `pt_log`, `e_log`, `ptrel`, `ptrel_log`, `erel`, `erel_log`, `mass`, `abseta`, `etarel`, `phirel`, `deltaR`, `ntracks`, `chi2`, `ndf`, `normchi2`, `dxy`, `dxyerr`, `dxysig`, `d3d`, `d3derr`, `d3dsig`, `costhetasvpv`

## Statistiques indicatives (moyenne par jet)

| | WL | WT |
|---|---|---|
| `n_cpfcands` (max) | 26.5 (81) | 23.6 (83) |
| `n_npfcands` (max) | 14.9 (48) | 12.7 (55) |
| `n_sv` (max) | 1.3 (10) | 1.15 (11) |

## Correspondance avec les variables GloParT

Les 86 variables du YAML `ak8_MD_inclv10beta4_ul_manual.yaml` (jet : `jet_tightId`, `jet_no`, `fj_pt`, `fj_sdmass`, `fj_eta`, `fj_phi`, `fj_mass` ; cpf ; npf ; sv) et les infos gen pour cos θ* sont toutes présentes sous les noms exacts attendus. Les masks (`*_mask`) ne sont pas stockés (calculés à partir de la longueur des vecteurs). La sélection du YAML (`fj_label`, `sample_isQCD`, `event_no%7`) est prévue pour le mix QCD/top/Higgs et doit être adaptée pour du VBS pur.

## Lecture rapide

```python
import uproot
t = uproot.open("dnntuple_WL.root")["deepntuplizer/tree"]
a = t.arrays(["fj_pt", "fj_isW", "fj_ptheta", "cpfcandlt_px"], cut="fj_isW==1")
```

ou avec ROOT : `ROOT.RDataFrame("deepntuplizer/tree", "dnntuple_WL.root")` (nécessite `cmsenv`).
