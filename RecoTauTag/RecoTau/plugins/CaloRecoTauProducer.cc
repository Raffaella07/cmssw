/* class CaloRecoTauProducer
 * EDProducer of the CaloTauCollection, starting from the CaloTauTagInfoCollection, 
 * authors: Simone Gennai (simone.gennai@cern.ch), Ludovic Houchu (Ludovic.Houchu@cern.ch)
 */

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/TauReco/interface/CaloTauTagInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "RecoTauTag/RecoTau/interface/CaloRecoTauAlgorithm.h"

#include "DataFormats/DetId/interface/DetIdCollection.h"

#include "CLHEP/Random/RandGauss.h"

#include <FWCore/ParameterSet/interface/ConfigurationDescriptions.h>
#include <FWCore/ParameterSet/interface/ParameterSetDescription.h>

#include <memory>

using namespace reco;
using namespace edm;
using namespace std;

class CaloRecoTauProducer : public EDProducer {
 public:
  explicit CaloRecoTauProducer(const edm::ParameterSet& iConfig);
  ~CaloRecoTauProducer() override;
  void produce(edm::Event&,const edm::EventSetup&) override;
  static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
 private:
  edm::InputTag CaloRecoTauTagInfoProducer_;
  edm::InputTag PVProducer_;
  double smearedPVsigmaX_;
  double smearedPVsigmaY_;
  double smearedPVsigmaZ_;
  double JetMinPt_;
  CaloRecoTauAlgorithm* CaloRecoTauAlgo_;
};

CaloRecoTauProducer::CaloRecoTauProducer(const edm::ParameterSet& iConfig){
  CaloRecoTauTagInfoProducer_  = iConfig.getParameter<edm::InputTag>("CaloRecoTauTagInfoProducer");
  PVProducer_                  = iConfig.getParameter<edm::InputTag>("PVProducer");
  smearedPVsigmaX_             = iConfig.getParameter<double>("smearedPVsigmaX");
  smearedPVsigmaY_             = iConfig.getParameter<double>("smearedPVsigmaY");
  smearedPVsigmaZ_             = iConfig.getParameter<double>("smearedPVsigmaZ");	
  JetMinPt_                    = iConfig.getParameter<double>("JetPtMin");
  CaloRecoTauAlgo_=new CaloRecoTauAlgorithm(iConfig);
  produces<CaloTauCollection>();
  produces<DetIdCollection>();
}
CaloRecoTauProducer::~CaloRecoTauProducer(){
  delete CaloRecoTauAlgo_;
}
  
void CaloRecoTauProducer::produce(edm::Event& iEvent,const edm::EventSetup& iSetup){

  auto resultCaloTau = std::make_unique<CaloTauCollection>();
  auto selectedDetIds = std::make_unique<DetIdCollection>();
 
  edm::ESHandle<TransientTrackBuilder> myTransientTrackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",myTransientTrackBuilder);
  CaloRecoTauAlgo_->setTransientTrackBuilder(myTransientTrackBuilder.product());
  
  edm::ESHandle<MagneticField> myMF;
  iSetup.get<IdealMagneticFieldRecord>().get(myMF);
  CaloRecoTauAlgo_->setMagneticField(myMF.product());
    
  // query a rec/sim PV
  edm::Handle<VertexCollection> thePVs;
  iEvent.getByLabel(PVProducer_,thePVs);
  const VertexCollection vertCollection=*(thePVs.product());
  Vertex thePV;
  if(!vertCollection.empty()) thePV=*(vertCollection.begin());
  else{
    Vertex::Error SimPVError;
    SimPVError(0,0)=smearedPVsigmaX_*smearedPVsigmaX_;
    SimPVError(1,1)=smearedPVsigmaY_*smearedPVsigmaY_;
    SimPVError(2,2)=smearedPVsigmaZ_*smearedPVsigmaZ_;
    Vertex::Point SimPVPoint(CLHEP::RandGauss::shoot(0.,smearedPVsigmaX_),  
			     CLHEP::RandGauss::shoot(0.,smearedPVsigmaY_),  
			     CLHEP::RandGauss::shoot(0.,smearedPVsigmaZ_));
    thePV=Vertex(SimPVPoint,SimPVError,1,1,1);    
  }
  
  edm::Handle<CaloTauTagInfoCollection> theCaloTauTagInfoCollection;
  iEvent.getByLabel(CaloRecoTauTagInfoProducer_,theCaloTauTagInfoCollection);
  int iinfo=0;
  for(CaloTauTagInfoCollection::const_iterator i_info=theCaloTauTagInfoCollection->begin();i_info!=theCaloTauTagInfoCollection->end();i_info++) { 
    if(i_info->jetRef()->pt()>JetMinPt_){ 
      CaloTau myCaloTau=CaloRecoTauAlgo_->buildCaloTau(iEvent,iSetup,Ref<CaloTauTagInfoCollection>(theCaloTauTagInfoCollection,iinfo),thePV);
      resultCaloTau->push_back(myCaloTau);
    }
    ++iinfo;
  }
  for(unsigned int i =0;i<CaloRecoTauAlgo_->mySelectedDetId_.size();i++)
    selectedDetIds->push_back(CaloRecoTauAlgo_->mySelectedDetId_[i]);


   iEvent.put(std::move(resultCaloTau));
   iEvent.put(std::move(selectedDetIds));
}

void
CaloRecoTauProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  // caloRecoTauProducer
  edm::ParameterSetDescription desc;
  desc.add<double>("LeadTrack_minPt", 0.5);
  desc.add<double>("MatchingConeSize_min", 0.0);
  desc.add<std::string>("ECALSignalConeSizeFormula", "0.15");
  desc.add<std::string>("TrackerIsolConeMetric", "DR");
  desc.add<std::string>("TrackerSignalConeMetric", "DR");
  desc.add<edm::InputTag>("EBRecHitsSource", edm::InputTag("ecalRecHit","EcalRecHitsEB"));
  desc.add<double>("IsolationTrack_minPt", 1.0);
  desc.add<double>("ECALSignalConeSize_min", 0.0);
  desc.add<double>("ECALRecHit_minEt", 0.5);
  desc.add<std::string>("MatchingConeMetric", "DR");
  desc.add<std::string>("TrackerSignalConeSizeFormula", "0.07");
  desc.add<std::string>("MatchingConeSizeFormula", "0.10");
  desc.add<double>("TrackerIsolConeSize_min", 0.0);
  desc.add<double>("TrackerIsolConeSize_max", 0.6);
  desc.add<double>("TrackerSignalConeSize_max", 0.6);
  desc.add<edm::InputTag>("PVProducer", edm::InputTag("offlinePrimaryVertices"));
  desc.add<edm::InputTag>("ESRecHitsSource", edm::InputTag("ecalPreshowerRecHit","EcalRecHitsES"));
  desc.add<double>("TrackerSignalConeSize_min", 0.0);
  desc.add<double>("ECALIsolConeSize_max", 0.6);
  desc.add<double>("AreaMetric_recoElements_maxabsEta", 2.5);
  desc.add<std::string>("ECALIsolConeMetric", "DR");
  desc.add<std::string>("ECALIsolConeSizeFormula", "0.50");
  desc.add<double>("JetPtMin", 0.0);
  desc.add<edm::InputTag>("EERecHitsSource", edm::InputTag("ecalRecHit","EcalRecHitsEE"));
  desc.add<unsigned int>("IsolationTrack_minHits", 0);
  desc.add<std::string>("ECALSignalConeMetric", "DR");
  desc.add<double>("TrackLeadTrack_maxDZ", 1.0);
  desc.add<double>("Track_minPt", 0.5);
  desc.add<std::string>("TrackerIsolConeSizeFormula", "0.50");
  desc.add<double>("ECALSignalConeSize_max", 0.6);
  desc.add<double>("ECALIsolConeSize_min", 0.0);
  desc.add<bool>("UseTrackLeadTrackDZconstraint", true);
  desc.add<double>("smearedPVsigmaY", 0.0015);
  desc.add<double>("smearedPVsigmaX", 0.0015);
  desc.add<double>("smearedPVsigmaZ", 0.005);
  desc.add<edm::InputTag>("CaloRecoTauTagInfoProducer", edm::InputTag("caloRecoTauTagInfoProducer"));
  desc.add<double>("MatchingConeSize_max", 0.6);
  descriptions.add("caloRecoTauProducer", desc);
}

DEFINE_FWK_MODULE(CaloRecoTauProducer);
