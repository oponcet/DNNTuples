#!/bin/bash -xe

WORKAREA=$1
INPUTFILES=$2
TRAINARG=$3
LOWLVLARG=$4
EOSPATH=$5
BRANCHNAME="Wpol_tagger"
TAGGER=$6

CMSRUNARGS="${TRAINARG} ${LOWLVLARG}"

WORKDIR=$(pwd)

if [ "${TAGGER}" == "WT" ]; then
    CFG=DeepNtuplizerAK8WT.py
    OUTFILE=output_WT.root
elif [ "${TAGGER}" == "WL" ]; then
    CFG=DeepNtuplizerAK8WL.py
    OUTFILE=output_WL.root
else
    echo "Unknown TAGGER=${TAGGER}"
    exit 1
fi

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc12

CMSSWVER="CMSSW_15_0_10"

########################################
# CMSSW SETUP (FIX: avoid duplicate rel if sandbox reused)
########################################

if [ ! -d "${CMSSWVER}/src" ]; then
    cmsrel ${CMSSWVER}
fi

cd ${CMSSWVER}/src
cmsenv

# ensure repo not re-cloned
if [ ! -d DeepNTuples ]; then
    git clone https://github.com/oponcet/DNNTuples.git DeepNTuples -b ${BRANCHNAME}
fi

scram b -j 4

cd ${WORKDIR}

########################################
# PARSE FILE LIST (CONDOR SAFE)
########################################

INPUTFILES=$(echo "${INPUTFILES}" | tr -d '\n\r')
IFS=',' read -ra FILES <<< "${INPUTFILES}"

echo "Number of input files = ${#FILES[@]}"

idx=0
outputs=()

########################################
# LOOP OVER FILES
########################################

for infile in "${FILES[@]}"; do

    echo "Processing: ${infile}"

    INPUTLOCAL=$(basename "${infile}")

    # input expected from Condor transfer_input_files
    if [ ! -f "${INPUTLOCAL}" ]; then
        echo "ERROR missing file: ${INPUTLOCAL}"
        ls -lh
        exit 100
    fi

    cmsRun \
    ${CMSSWVER}/src/DeepNTuples/Ntupler/test/${CFG} \
    inputFiles="file:${INPUTLOCAL}" \
    ${CMSRUNARGS} \
    2>&1 | tee cmsRun_${TAGGER}_${idx}.log

    CMS_STATUS=${PIPESTATUS[0]}

    if [ ${CMS_STATUS} -ne 0 ]; then
        echo "cmsRun failed on ${INPUTLOCAL}"
        tail -100 cmsRun_${TAGGER}_${idx}.log
        exit ${CMS_STATUS}
    fi

    if [ ! -f "${OUTFILE}" ]; then
    echo "missing ${OUTFILE}"
    exit 101
    fi

    mv "${OUTFILE}" dnntuple_raw_${TAGGER}_${idx}.root

    idx=$((idx+1))

done

########################################
# MERGE
########################################

# echo "Merging outputs..."

# if [ ${#outputs[@]} -eq 1 ]; then
#     mv "${outputs[0]}" dnntuple.root
# else
#     hadd -fk dnntuple.root "${outputs[@]}"
# fi

########################################
# EOS OUTPUT (with minimal robustness)
########################################

# if [ -n "${EOSPATH}" ]; then
#     echo "Copying to EOS: ${EOSPATH}"

#     xrdcp -f dnntuple.root "${EOSPATH}"
#     XRDCODE=$?

#     if [ ${XRDCODE} -ne 0 ]; then
#         echo "ERROR xrdcp failed"
#         exit ${XRDCODE}
#     fi
# fi

echo "DONE"