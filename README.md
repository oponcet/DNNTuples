# DNNTuplesAK8

## Setup
```bash
cmsrel CMSSW_15_0_10
cd CMSSW_15_0_10/src
cmsenv

# clone this repo into "DeepNTuples" directory
git clone git@github.com:colizz/DNNTuples.git DeepNTuples -b dev-haa-nanov15

scram b -j8
```

<!-- 
## Submit jobs via CRAB

**Step 0**: switch to the crab production directory and set up grid proxy, CRAB environment, etc.

```bash
cd $CMSSW_BASE/src/DeepNTuples/Ntupler/run
# set up grid proxy
voms-proxy-init -rfc -voms cms --valid 168:00
# set up CRAB env (must be done after cmsenv)
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

**Step 1**: use the `crab.py` script to submit the CRAB jobs:

`python crab.py --set-input-dataset -p ../test/DeepNtuplizerAK8.py --site T2_CH_CERN -o /store/user/$USER/DeepNtuples/[version] -t DeepNtuplesAK8-[version] --no-publication -i [ABC].conf -s FileBased -n 5 --work-area crab_projects_[ABC] --send-external [--input_files JEC.db] --dryrun`

These command will perform a "dryrun" to print out the CRAB configuration files. Please check everything is correct (e.g., the output path, version number, requested number of cores, etc.) before submitting the actual jobs. To actually submit the jobs to CRAB, just remove the `--dryrun` option at the end.

**[Note] For the QCD samples use `-n 1 --max-units 20` to run one file per job, and limit the total files per job to 20.**


**Step 2**: check job status

The status of the CRAB jobs can be checked with:

```bash
./crab.py --status --work-area crab_projects_[ABC]
```

Note that this will also resubmit failed jobs automatically.

The crab dashboard can also be used to get a quick overview of the job status:
`https://dashb-cms-job.cern.ch/dashboard/templates/task-analysis`

More options of this `crab.py` script can be found with:

```bash
./crab.py -h
``` -->

## DeepNtuplizerAK8RePuppi — Summary

- Reads **MiniAOD** and processes **AK8 jets (R = 0.8)**
- Recomputes **PUPPI weights** and **reclusters jets + MET**
- Uses updated **PF candidates (`packedPFCandidatesRePuppi`)** as ML inputs
- *(Optional)* runs **advanced jet taggers** (ParticleNet, Transformer, etc.)
- Builds **gen-level AK8 jets** (with/without neutrinos, with SoftDrop)
- Performs **reco–gen matching** (ΔR = 0.8) for truth association
- Produces a **flat ROOT ntuple** via `DeepNtuplizer`

### Ntuple content

- Jet kinematics and substructure
- Tagger scores (ParticleNet, GlobalParticleTransformer, etc.)
- PF candidate low-level features *(optional)*
- Matched gen-jet information

### Usage

- Designed for **deep learning training/inference**
- Optimized for **boosted object tagging** (W/Z/H/top)
- Runs **interactively on a single MiniAOD file**



DeepNTuples/
|-- BTagHelpers
|   |-- BuildFile.xml
|   |-- interface
|   |   |-- FlavorDefinition.h
|   |   `-- TrackInfoBuilder.h
|   `-- src
|       |-- FlavorDefinition.cc
|       `-- TrackInfoBuilder.cc
|-- FatJetHelpers
|   |-- BuildFile.xml
|   |-- data
|   |   `-- DeepBoostedJet
|   |       `-- ak15
|   |           `-- decorrelated
|   |               |-- resnet-symbol.json
|   |               `-- resnet.params
|   |-- interface
|   |   `-- FatJetMatching.h
|   |-- python
|   |   |-- __pycache__
|   |   |   `-- pfDeepBoostedJetPreprocessParamsAK15_cfi.cpython-39.pyc
|   |   `-- pfDeepBoostedJetPreprocessParamsAK15_cfi.py
|   `-- src
|       `-- FatJetMatching.cc
|-- NtupleCommons
|   |-- BuildFile.xml
|   |-- interface
|   |   |-- InfinityCatcher.h
|   |   |-- JetHelper.h
|   |   |-- NtupleBase.h
|   |   |-- TreeData.h
|   |   `-- TreeWriter.h
|   `-- src
|       |-- JetHelper.cc
|       `-- TreeData.cc
|-- Ntupler
|   |-- BuildFile.xml
|   |-- README.md
|   |-- data
|   |   |-- DeepHWW-MD
|   |   |   `-- ak8
|   |   |       `-- V01
|   |   |           |-- README.md
|   |   |           |-- model.onnx
|   |   |           |-- preprocess.json
|   |   |           |-- preprocess_corr.json
|   |   |           `-- preprocess_pnetmass_template.json
|   |   |-- InclParticleTransformer-MD
|   |   |   `-- ak8
|   |   |       |-- V01
|   |   |       |   |-- README.md
|   |   |       |   |-- model.onnx
|   |   |       |   |-- preprocess.json
|   |   |       |   `-- preprocess_corr.json
|   |   |       |-- V02-HidLayer
|   |   |       |   `-- preprocess_corr.json
|   |   |       `-- V03pre1
|   |   |           |-- model_embed.onnx
|   |   |           `-- preprocess_corr.json
|   |   `-- ParticleNet-MD
|   |       `-- ak15
|   |           `-- V02d
|   |               |-- README.md
|   |               |-- particle-net.onnx
|   |               `-- preprocess.json
|   |-- interface
|   |   |-- FatJetInfoFiller.h
|   |   |-- JetInfoFiller.h
|   |   |-- PFCompleteFiller.h
|   |   |-- SVFiller.h
|   |   `-- ScoutFatJetCompleteFiller.h
|   |-- plugins
|   |   |-- BuildFile.xml
|   |   |-- CustomDeepBoostedJetTagInfoProducer.cc
|   |   |-- DeepNtuplizer.cc
|   |   |-- JetMatchingDRAllowEmpty.cc
|   |   |-- PATPackedCandidateUpdater.cc
|   |   `-- ParticleTransformerAK8TagInfoProducer.cc
|   |-- python
|   |   |-- DeepNtuplizer_cfi.py
|   |   |-- __pycache__
|   |   |   |-- DeepNtuplizer_cfi.cpython-39.pyc
|   |   |   `-- jetTools.cpython-39.pyc
|   |   |-- hwwTagger
|   |   |   |-- __pycache__
|   |   |   |   |-- bTaggingCustomUtils.cpython-39.pyc
|   |   |   |   |-- pfMassDecorrelatedDeepHWWV1DiscriminatorsJetTags_cfi.cpython-39.pyc
|   |   |   |   |-- pfMassDecorrelatedDeepHWWV1_cff.cpython-39.pyc
|   |   |   |   |-- pfMassDecorrelatedInclParticleTransformerV1DiscriminatorsJetTags_cfi.cpython-39.pyc
|   |   |   |   |-- pfMassDecorrelatedInclParticleTransformerV1_cff.cpython-39.pyc
|   |   |   |   |-- pfMassDecorrelatedInclParticleTransformerV2DiscriminatorsJetTags_cfi.cpython-39.pyc
|   |   |   |   |-- pfMassDecorrelatedInclParticleTransformerV2_cff.cpython-39.pyc
|   |   |   |   `-- pfMassDecorrelatedInclParticleTransformerV3_cff.cpython-39.pyc
|   |   |   |-- bTaggingCustomUtils.py
|   |   |   |-- pfMassDecorrelatedDeepHWWV1DiscriminatorsJetTags_cfi.py
|   |   |   |-- pfMassDecorrelatedDeepHWWV1_cff.py
|   |   |   |-- pfMassDecorrelatedInclParticleTransformerV1DiscriminatorsJetTags_cfi.py
|   |   |   |-- pfMassDecorrelatedInclParticleTransformerV1_cff.py
|   |   |   |-- pfMassDecorrelatedInclParticleTransformerV2DiscriminatorsJetTags_cfi.py
|   |   |   |-- pfMassDecorrelatedInclParticleTransformerV2_cff.py
|   |   |   `-- pfMassDecorrelatedInclParticleTransformerV3_cff.py
|   |   `-- jetTools.py
|   |-- run
|   |   |-- 2016
|   |   |   |-- BulkGrav.conf
|   |   |   |-- JMAR.conf
|   |   |   |-- Radion.conf
|   |   |   |-- TT.conf
|   |   |   |-- Wprime.conf
|   |   |   |-- Zprime.conf
|   |   |   |-- qcd.conf
|   |   |   `-- ttbar.conf
|   |   |-- 2017
|   |   |   |-- ak15
|   |   |   |   |-- HH4Q.conf
|   |   |   |   |-- qcd-mg.conf
|   |   |   |   `-- signals.conf
|   |   |   `-- ak8
|   |   |       |-- qcd.conf
|   |   |       `-- signals.conf
|   |   |-- 2018
|   |   |   `-- ak15
|   |   |       |-- HH4Q.conf
|   |   |       `-- qcd-flat.conf
|   |   |-- crab.py
|   |   `-- samples
|   |       |-- UL17
|   |       |   `-- ak8
|   |       |       |-- hh4q.conf
|   |       |       |-- qcd.conf
|   |       |       `-- signals.conf
|   |       `-- UL18
|   |           `-- ak8
|   |               |-- hh4q.conf
|   |               |-- qcd.conf
|   |               `-- signals.conf
|   |-- scripts
|   |   `-- install_onnxruntime.sh
|   |-- src
|   |   |-- FatJetInfoFiller.cc
|   |   |-- JetInfoFiller.cc
|   |   |-- PFCompleteFiller.cc
|   |   |-- SVFiller.cc
|   |   `-- ScoutFatJetCompleteFiller.cc
|   `-- test
|       |-- DeepNtuplizerAK8.py
|       |-- DeepNtuplizerAK8RePuppi.py
|       |-- DeepNtuplizerAK8Scout.py
|       `-- output_numEvent100.root
`-- README.md


# DeepNTuples for VBS W Polarization

This repository is a fork of the original DNNTuples framework developed by Colizzi et al. and based on the `dev-haa-nanov15` branch.

The framework has been adapted for studies of Vector Boson Scattering (VBS) with a focus on hadronically decaying boosted W bosons and polarization classification.

Current development targets:

* CMSSW_15_0_10
* Run 3 MiniAOD samples
* LPC EL9 environment
* W longitudinal (WL) vs transverse (WT) polarization studies
* Deep-learning ntuple production for AK8 jets

## Environment Setup

```bash
cd /uscms_data/d3/oponcet1/VBS/

source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsrel CMSSW_15_0_10
cd CMSSW_15_0_10/src

cmsenv
```

Clone the repository:

```bash
git clone git@github.com:oponcet/DNNTuples.git DeepNTuples
cd DeepNTuples
```

Build:

```bash
scram b -j8
```

---

## Local Production

Move to the ntuplizer directory:

```bash
cd $CMSSW_BASE/src/DeepNTuples/Ntupler/test
```

Run on a single MiniAOD file:

### WT samples

```bash
cmsRun DeepNtuplizerAK8WT.py \
    maxEvents=100 \
    isTrainSample=1
```

### WL samples

```bash
cmsRun DeepNtuplizerAK8WL.py \
    maxEvents=100 \
    isTrainSample=1
```

Output:

```text
output_WT.root
output_WL.root
```

---

## LPC Condor Production

Jobs are submitted through HTCondor on LPC.

### Submit WT jobs

```bash
condor_submit condor/submit_wT.jdl
```

### Submit WL jobs

```bash
condor_submit condor/submit_wL.jdl
```

The worker node:

1. Creates a fresh CMSSW_15_0_10 area.
2. Clones the repository.
3. Builds DeepNTuples.
4. Runs the corresponding cmsRun configuration.
5. Copies the output ROOT file to EOS.

---

## W Polarization Extensions

The ntuplizer has been extended with dedicated W-polarization information.

### Sample Flags

Additional configuration flags:

```cpp
bool sample_isWT_ = false;
bool sample_isWL_ = false;
```

These flags identify the generated polarization state of the signal sample.

---

### Polarization Observable: p_theta

The variable

[
p_{\theta}=\frac{|E_1-E_2|}{|\vec{p}_W|}
]

is computed from the two leading W subjets.

Implementation:

```cpp
float dE = std::abs(sj1->energy() - sj2->energy());
float pW_mag = jet.p();

float ptheta = (pW_mag > 0) ? dE / pW_mag : 0.0;

data.fill<float>("fj_ptheta", ptheta);
```

This observable is sensitive to the W helicity through the energy asymmetry of the two decay products.

---

### Polarization Observable: z_j

The variable

[
z_j=\frac{\max(p_{T,1},p_{T,2})}{p_{T,W}}
]

measures the momentum sharing between the two reconstructed subjets.

Implementation:

```cpp
float pt1 = sj1->pt();
float pt2 = sj2->pt();

float leading_pt = std::max(pt1, pt2);
float pTW = jet.pt();

float zj = (pTW > 0) ? leading_pt / pTW : 0.0;

data.fill<float>("fj_zj", zj);
```

This variable is expected to carry information about the polarization state of the parent W boson.

---

## Ntuple Content

The output ROOT tree contains:

* AK8 jet kinematics
* Jet mass and substructure observables
* Deep-learning tagger inputs
* Particle-flow candidate information
* Secondary vertex information
* Generator-level matching
* W-polarization labels
* Polarization-sensitive observables:

  * `fj_ptheta`
  * `fj_zj`

---

## Typical Workflow

1. Produce MiniAOD signal samples.
2. Run DeepNtuplizerAK8WT.py or DeepNtuplizerAK8WL.py.
3. Merge output ROOT files.
4. Train WL vs WT classifiers.
5. Evaluate polarization-sensitive observables and ML performance.
