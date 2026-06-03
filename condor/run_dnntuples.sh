#!/bin/bash -xe

WORKAREA=$1
INPUTFILE=$2
CMSRUNARGS=$3
EOSPATH=$4
BRANCHNAME="Wpol_tagger"


WORKDIR=$(pwd)

source /cvmfs/cms.cern.ch/cmsset_default.sh

# IMPORTANT: correct architecture
export SCRAM_ARCH=el9_amd64_gcc12

CMSSWVER="CMSSW_15_0_10"

########################################
# CMSSW SETUP (on worker node)
########################################

cmsrel ${CMSSWVER}
cd ${CMSSWVER}/src
cmsenv

git clone https://github.com/oponcet/DNNTuples.git DeepNTuples -b ${BRANCHNAME}
scram b -j 4

cd ${WORKDIR}

########################################
# INPUT (CONDOR-STAGED FILE)
########################################

INPUTLOCAL=$(basename "${INPUTFILE}")

echo "Input file expected locally:"
ls -lh "${INPUTLOCAL}"

if [ ! -f "${INPUTLOCAL}" ]; then
    echo "ERROR: input file not found in sandbox: ${INPUTLOCAL}"
    exit 100
fi

########################################
# RUN CMSRUN (NO SILENT RETRIES)
########################################

echo "Running cmsRun..."

cmsRun \
    ${CMSSWVER}/src/DeepNTuples/Ntupler/test/DeepNtuplizerAK8WT.py \
    inputFiles="file:${INPUTLOCAL}" \
    ${CMSRUNARGS} \
    2>&1 | tee cmsRun.log

CMS_STATUS=${PIPESTATUS[0]}

echo "cmsRun exit code: ${CMS_STATUS}"

if [ ${CMS_STATUS} -ne 0 ]; then
    echo "cmsRun FAILED"
    tail -200 cmsRun.log
    exit ${CMS_STATUS}
fi

########################################
# OUTPUT HANDLING
########################################

mv output.root dnntuple.root

########################################
# EOS COPY
########################################

if [ -n "$EOSPATH" ]; then
    echo "Copying to EOS: ${EOSPATH}"
    xrdcp -f dnntuple.root "${EOSPATH}"
fi

echo "DONE"