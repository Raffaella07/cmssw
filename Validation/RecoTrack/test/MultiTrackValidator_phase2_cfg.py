import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("MULTITRACKVALIDATOR",eras.Phase2C22I13M9)

# message logger
process.MessageLogger = cms.Service("MessageLogger",
     default = cms.untracked.PSet( limit = cms.untracked.int32(100) )
)


#Adding SimpleMemoryCheck service:
process.SimpleMemoryCheck=cms.Service("SimpleMemoryCheck",
                                   ignoreTotal=cms.untracked.int32(1),
                                   oncePerEventMode=cms.untracked.bool(True)
)

process.Timing = cms.Service("Timing"
    ,summaryOnly = cms.untracked.bool(True)
)

#workaround for CMSSW_14_1_1 in Eos -  https://github.com/cms-sw/cmssw/issues/44369
process.add_(cms.Service("AdaptorConfig", native=cms.untracked.vstring("root")))

# source
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
#source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
source = cms.Source ("PoolSource",fileNames = readFiles)
readFiles.extend( [
    '/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-RECO/140X_mcRun4_realistic_v3_RV239_2026D112-v1/2590000/81fdadea-30d0-41b4-9ee6-9ac448a41433.root'
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-RECO/140X_mcRun4_realistic_v3_RV239_2026D112-v1/2590000/0015b207-eb60-4fa9-8d86-41558ba6b1f4.root',    
              ] )



secFiles.extend( ['/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D112-v1/2590000/604e7bd1-2912-4a67-b71b-01fac24a9eec.root'#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D112-v1/2590000/e4d479d0-c741-4190-90da-22dffbc9d8ff.root'#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/1d28af38-e243-446d-b7db-d876b87e91f8.root'
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/85b16bb3-6e59-4876-82e6-f78149ecefdd.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/c6024c87-95cd-4778-9963-b9beec254cad.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/bcf99057-4d1a-4109-9900-d972db054755.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/410e6a60-67c6-45ec-8d73-c422377c18d5.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/8f94e9b7-9013-4ffa-9a2e-fdca9c7f905e.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/94537748-f45f-4119-be2b-513306f82bf8.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/f67bccaf-81ba-40cd-a1d1-14a5f92027f4.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/e933da09-58f7-41b3-8613-11f58ed9ff97.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/1d28af38-e243-446d-b7db-d876b87e91f8.root',
#'/store/relval/CMSSW_14_1_0_pre3/RelValFourMuExtendedPt1_200/GEN-SIM-DIGI-RAW/140X_mcRun4_realistic_v3_RV239_2026D113-v1/2590000/146977b1-d518-4ca1-adcb-590e482279c7.root',
 ] )
process.source = source
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

### conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T37', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '140X_mcRun4_realistic_v3', '')

### standard includes
process.load('Configuration/StandardSequences/Services_cff')
#process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.Geometry.GeometryExtended2026D112Reco_cff')

### validation-specific includes
process.load("SimTracker.TrackAssociatorProducers.trackAssociatorByHits_cfi")
process.load("SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi")
process.load("SimGeneral.TrackingAnalysis.trackingParticleNumberOfLayersProducer_cff")
process.load("SimTracker.TrackAssociatorProducers.trackAssociatorByChi2_cfi")
process.load("SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi")
process.load("Validation.RecoTrack.cuts_cff")
process.load("Validation.RecoTrack.MultiTrackValidator_cff")
process.load("DQMServices.Components.EDMtoMEConverter_cff")
process.load("Validation.Configuration.postValidation_cff")
process.quickTrackAssociatorByHits.SimToRecoDenominator = 'reco'




########### configuration MultiTrackValidator ########
process.multiTrackValidator.associators = ['quickTrackAssociatorByHits']
#process.cutsRecoTracks.quality = ['','highPurity']
#process.cutsRecoTracks.quality = ['']
process.multiTrackValidator.label = ['cutsRecoTracks']
process.multiTrackValidator.histoProducerAlgoBlock.useLogPt = True
process.multiTrackValidator.histoProducerAlgoBlock.minPt = 0.1
process.multiTrackValidator.histoProducerAlgoBlock.maxPt = 3000.0
process.multiTrackValidator.histoProducerAlgoBlock.nintPt = 40
process.multiTrackValidator.UseAssociators = True


#process.load("Validation.RecoTrack.cuts_cff")
#process.cutsRecoTracks.quality = ['highPurity']
#process.cutsRecoTracks.ptMin    = 0.5
#process.cutsRecoTracks.minHit   = 10
#process.cutsRecoTracks.minRapidity  = -1.0
#process.cutsRecoTracks.maxRapidity  = 1.0

process.quickTrackAssociatorByHits.useClusterTPAssociation = True
process.load("SimTracker.TrackerHitAssociation.tpClusterProducer_cfi")
process.options = cms.untracked.PSet(
    exceptionsToIgnore = cms.untracked.vstring('ProductNotFound')
)
from Validation.RecoTrack.customiseTrackingNtuple import customiseTrackingNtuple
process = customiseTrackingNtuple(process)

process.validation = cms.Sequence(
    process.tpClusterProducer *
    process.quickTrackAssociatorByHits *
    process.trackingParticleNumberOfLayersProducer*
    process.multiTrackValidator*
    process.trackingNtupleSequence
)

# paths
process.val = cms.Path(
      process.cutsRecoTracks
    * process.validation
)

# Output definition
process.DQMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.DQMEventContent.outputCommands,
    fileName = cms.untracked.string('file:MTV_inDQM.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('DQM')
    )
)

process.endjob_step = cms.EndPath(process.endOfProcess)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)



process.schedule = cms.Schedule(
      process.val,process.endjob_step,process.DQMoutput_step
)

process.options = cms.untracked.PSet(
    numberOfThreads = cms.untracked.uint32(8),
    numberOfStreams = cms.untracked.uint32(8),
    wantSummary = cms.untracked.bool(True)
)
