
#ifndef KAPPA_GENJETPRODUCER_H
#define KAPPA_GENJETPRODUCER_H

#include "DataFormats/JetReco/interface/GenJet.h"
#include "PhysicsTools/JetMCUtils/interface/JetMCTag.h"

#include "KBaseMultiLVProducer.h"


class KGenJetProducer : public KBaseMultiLVProducer<edm::View<reco::GenJet>, KGenJets>
{
public:
	KGenJetProducer(const edm::ParameterSet &cfg, TTree *_event_tree, TTree *_lumi_tree) :
		KBaseMultiLVProducer<edm::View<reco::GenJet>, KGenJets>(cfg, _event_tree, _lumi_tree, getLabel())
	{
	}

	static const std::string getLabel() { return "GenJets"; }

	virtual bool onLumi(const edm::LuminosityBlock &lumiBlock, const edm::EventSetup &setup)
	{
		return KBaseMultiLVProducer<edm::View<reco::GenJet>, KGenJets>::onLumi(lumiBlock, setup);
	}

	virtual void fillProduct(const InputType &in, OutputType &out, const std::string &name,
	                         const edm::InputTag *tag, const edm::ParameterSet &pset)
	{
		KBaseMultiLVProducer<edm::View<reco::GenJet>, KGenJets>::fillProduct(in, out, name, tag, pset);
	}

	virtual void fillSingle(const SingleInputType &in, SingleOutputType &out)
	{
		/// momentum:
		copyP4(in, out.p4);
		
		std::string genTauDecayModeString = JetMCTagUtils::genTauDecayMode(in);
		if (genTauDecayModeString == "oneProng0Pi0")
		{
			out.genTauDecayMode = 0;
		}
		else if (genTauDecayModeString == "oneProng1Pi0" || genTauDecayModeString == "oneProng2Pi0")
		{
			out.genTauDecayMode = 1;
		}
		else if (genTauDecayModeString == "threeProng0Pi0")
		{
			out.genTauDecayMode = 2;
		}
		else
		{
			out.genTauDecayMode = -1;
		}
	}
};

#endif