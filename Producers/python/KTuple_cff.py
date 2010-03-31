import FWCore.ParameterSet.Config as cms

kappaTupleDefaultsBlock = cms.PSet(
	verbose = cms.int32(0),
	active = cms.vstring("Metadata"),

	Metadata = cms.PSet(
		genSource = cms.InputTag("generator"),

		l1Source = cms.InputTag("gtDigis"),
		hltSource = cms.InputTag("TriggerResults::HLT"),
		hltFilter = cms.string("^HLT_(((L1|Di|Double|Triple|Quad)?(Jet)+(Ave)?|MET)[0-9]*|Activity_.*|.*(Bias|BSC).*)$"),

		noiseHCAL = cms.InputTag("hcalnoise"),
	),

	Muons = cms.PSet(
		manual = cms.VInputTag(),

		whitelist = cms.vstring("recoMuons_muons"),
		blacklist = cms.vstring(),

		rename = cms.vstring(),
		rename_whitelist= cms.vstring(),
		rename_blacklist = cms.vstring(),

		maxN = cms.int32(-1),
		minPt = cms.double(-1),
		maxEta = cms.double(-1),
	),

	Tracks = cms.PSet(
		manual = cms.VInputTag(),

		whitelist = cms.vstring("recoTracks_generalTracks"),
		blacklist = cms.vstring(),

		rename = cms.vstring(),
		rename_whitelist= cms.vstring(),
		rename_blacklist = cms.vstring(),

		maxN = cms.int32(-1),
		minPt = cms.double(-1),
		maxEta = cms.double(-1),
	),

	LV = cms.PSet(
		manual = cms.VInputTag(),

		whitelist = cms.vstring("reco.*Jets_.*Jet"),
		blacklist = cms.vstring(),

		rename = cms.vstring(
			"JetPlusTrack(.*) => $1JPT",
			"(antikt)|(kt)|(siscone)|(iterativecone)|(icone)|(ak)([0-9]*) => (?1AK)(?2KT)(?3SC)(?4IC)(?5IC)(?6AK)$7",
			"((L2)(L3)?|(ZSP)(Jet)?)CorJet(..[0-9]*)(PF)?(JPT)?(Calo)? => $6(?3L3:(?2L2))(?4L0)(?7PF)(?8JPT)Jets",
		),
		rename_whitelist= cms.vstring(),
		rename_blacklist = cms.vstring(),

		maxN = cms.int32(-1),
		minPt = cms.double(-1),
		maxEta = cms.double(-1),
	),

	Tower = cms.PSet(
		manual = cms.VInputTag(),

		whitelist = cms.vstring("towerMaker"),
		blacklist = cms.vstring(),

		rename = cms.vstring("towerMaker => towers"),
		rename_whitelist = cms.vstring(),
		rename_blacklist = cms.vstring(),

		srcPVs = cms.InputTag("offlinePrimaryVertices"),

		maxN = cms.int32(-1),
		minPt = cms.double(-1),
		maxEta = cms.double(-1),
	),

	MET = cms.PSet(
		manual = cms.VInputTag(),

		whitelist = cms.vstring("reco.*MET"),
		blacklist = cms.vstring(),

		rename = cms.vstring(
			"(gen)?(pf)?(ht)?met => (?1Gen:Calo)MET(?2PF)(?3HT)",
		),
		rename_whitelist = cms.vstring("^(Calo|Gen)MET"),
		rename_blacklist = cms.vstring(),
	),
)
