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