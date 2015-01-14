# κappa {#mainpage}

κappa is the Karlsruhe Package for Physics Analysis.
It is a skimming framework constructed to extract the relevant data
from EDM data sets (RECO, AOD, MINIAOD) and store it in a well-defined
and compact ROOT data format. This full documentation is found
[here](http://www-ekp.physik.uni-karlsruhe.de/~berger/kappa/ "Kappa Doxygen").


Installation
============

Skimming:

setup CMSSW

    cmsrel CMSSW_5_3_14
    cd CMSSW_5_3_14/src
    cmsenv

checkout Kappa

    git clone https://github.com/KappaAnalysis/Kappa.git

compile

    scram b

run

    cmsRun Kappa/Skimming/skim_tutorial_53x.py


The output looks similar to:

    01-Jan-2015 00:00:00 CET  Initiating request to open file file:/path/to/file.root
    01-Jan-2015 00:00:00 CET  Successfully opened file file:/path/to/file.root
    --- Reader                   : Booking "BDT" of type ... if electrons configured
    Electron ID MVA Completed                                until here
    Start Kappa producer KTuple
    Init producer TreeInfo      ... for each configured Kappa producer
    Taking trigger from process HLT (label = TriggerResults)
    Begin processing the 1st record. Run 1, Event 100000, LumiSection 2500 at 01-Jan-2015 00:01:00 CET


Usage and options
-----------------

The Kappa-CMSSW EDProducer has a few options:

- `verbose` (int): Level of verbosity (default: 0)
- `profile` (bool): Enables profiling (default: False)
- `outputFile` (str): Name of the Kappa output file, (e.g. `"kappa.root"`)
- `active` (list): List of object names that should be written out (e.g. `['Electrons']`)

check skim (KappaTools)

- check sizes
- check runtime
- diff skims
- look at distributions

What Kappa does is best summarized in this image:

![Kappa workflow](http://www-ekp.physik.uni-karlsruhe.de/~berger/files/kappa.svg "The Kappa workflow")

Documentation
=============

The objects of the Kappa data formats can be directly printed on standard out.
Here is an example for jets:

    KJet jet;
    KJets jets;
    std::cout << jet;                    // print the relevant members of the object
    std::cout << displayVector(jets);    // print the vector size and all elements.
    std::cout << displayVector(jets, 2); // print the vector size and the first two elements


Producers hierachy
------------------------------

The base classes for all producers follow this hierarchy structure:

- KBaseProducer
  - KBaseProducerWP: With provenance
    - KInfoProducer: Produce general information of the tree (e.g. KEventInfo)
    - KBaseMatchingProducer: Regular expression matching
      - KBaseMultiProducer: Produce objects per event (e.g. KMET)
        - KBaseMultiVectorProducer: Produce lists (`std::vector`) of objects per event (e.g. KVertices)
          - KBaseMultiLVProducer: Produce lists of particles or other Lorentz-vector objects (e.g KElectron)

The data types of member variables are the same as in CMSSW in order to
not loose precision but at the same time not waste space in the skim.
Note: Even if some member functions of CMSSW data formats return an
int or double type, the underlying member variable is only of char,
short or float precision and therefore the latter is used.

[Minimum sizes](http://www.cplusplus.com/doc/tutorial/variables/):
 8 char
16 short, int
32 long
64 long long
32 float
64 double

Boolean values are mostly stored in bitmaps. Strings should not be part
of a data format of the Events tree. In most cases this information can be stored in the Lumis tree.

Naming scheme {#main-naming}
============================

- K<Object> for all physical objects (e.g. KJet)
- in case there are different versions for one object the object for the
  standard use case is called in the most simple way K<Object>.
  More complicated objects can be named "KExtended<Object>".
  Simpler versions are called "KBasic<Objects>" (e.g. KBasicJet).
- K<Object>Summary for summaries of vector quantities (e.g. KVertexSummary).
- K<Tree>Info for general tree information (e.g KEventInfo).
- K<Object>Metadata for objects stored in lumi tree containing
  information about the corresponding object in the event tree

Repository management
---------------------

- **Branches**:
  These branches should be used for most development work:
  - *master*: The stable default version that is recommended for general use
  - *dictchanges*: Commits that change the data format in a backwards incompatible way
  - *development*: Other changes that do not touch the data format
  
  While the merges or commits to the master branch must be thoroughly checked,
  commits pushed to dictchanges or development must compile and should
  be checked to produce reasonable results.

- **Tags**:
  Each new version that is used in a real skim (not every commit on master)
  should get a tag of the form: `Kappa_1_2_3`
  The numbers are increased in this cases:
    - (1) major version: only in rare cases of major changes
    - (2) minor version: in case the data format has changed
    - (3) revision: any other case that needs a tag
  Using `git describe` returns a unique identifier for the current commit
  in the form *last tag*-*commits since then*-*short commit hash*.

Changes in Kappa 2.0 {#main-changes}
====================================

The changes can be seen using this command:
``git log --oneline 71f3f8e..333adc6``
or in the [change log](https://github.com/KappaAnalysis/Kappa/compare/71f3f8e...333adc6).

- **Changes in Lorentz vector definitions**:

  There are two ROOT::Math Lorentz vectors:
  RMFLV and RMDLV in float and double precision.
  And there is now only one Kappa base class: KLV (float precision)
  which is used as base class for all particles.
  This is chosen because the Lorentz vectors in the reco format are
  float precision.
  - Remove unused KLV
  - Rename KDataLV to KLV
  - Remove the LVWrap
  - Rename RMDataLV to RMFLV and RMLV to RMDLV
  
- **Renaming, moving and removing data format classes and producers**:

  Many classes and files are renamed. This is done to consolidate the
  naming following a consistent [naming scheme](#main-naming).  
  These are the commits containing the changes:
  - Rename data format classes and producers ([dbe9b1c]())
  - Update with classes.UP ([91a9b28]())
  - Rename producer headers to match the contained producer class ([a02547e]())
  - Rename object metadata classes ([993b42f]())
  - Rename event and lumi infos
  - Rename KMetadata.h to KInfo.h
  - Move data format definitions (2)
  - Simplify header dependencies
  - Unified naming scheme for branch names
  - Remove KCaloTaus
  - Remove KCandidateProducer

- **Update the data format content**:

  The data format definition is adapted to new needs. The changes are
  done such that it is more flexible for future requirements.
  
  There are no changes in these classes:
  KBasicMET, KDataLumiInfo, KFilterMetadata, KFilterSummary, KGenEventInfo,
  KGenLumiInfo, KEventInfo, KHCALNoiseSummary, KHit, KPileupDensity, KL1Muon,
  KLumiInfo, KMuonTriggerCandidate, KProvenance, KTrackSummary, KVertex,
  KVertexSummary.

  KTriggerObjectMetadata, KTriggerObjects, ,  
  KGenParticle, KGenPhoton, KGenTau, KPFCandidate,  

  - KParticle (new)
  - [KGenEventInfo](https://github.com/KappaAnalysis/Kappa/commit/26b6863) 
  - [KEventInfo](https://github.com/KappaAnalysis/Kappa/commit/2738bb3)
  - [KVertex](https://github.com/KappaAnalysis/Kappa/commit/06f30d4)
  - [KTriggerObject](https://github.com/KappaAnalysis/Kappa/commit/4be2b0f)
  - [KParticle](https://github.com/KappaAnalysis/Kappa/commit/41df988)
  - [KMET](https://github.com/KappaAnalysis/Kappa/commit/845b3e3)
  - [KJets](https://github.com/KappaAnalysis/Kappa/commit/0ba7640)
  - [KBasicJet](https://github.com/KappaAnalysis/Kappa/commit/ab8740d)
  - [KCaloJet](https://github.com/KappaAnalysis/Kappa/commit/93d17b3)
  - [KTrack](https://github.com/KappaAnalysis/Kappa/commit/395bd6a)
  - [KLepton](https://github.com/KappaAnalysis/Kappa/commit/4e91541)
  - [KTau](https://github.com/KappaAnalysis/Kappa/commit/be117c2)
  - [KBasicTau](https://github.com/KappaAnalysis/Kappa/commit/feb768d)
  - [KMuon](https://github.com/KappaAnalysis/Kappa/commit/4173b91)
  - [KElectron](https://github.com/KappaAnalysis/Kappa/commit/b33bbd2)
  - Documentation of all dataformats


- **Changes in the producers**:

- Infrastructure changes:
  - classes is now written in [Markdown]
  - classes.UP also handles LinkDef.h
  - update with new classes.UP

- Implementation of missing debug output for new classes:
  KElectronMetadata, KFilterMetadata, KGenPhoton, KHCALNoiseSummary,
  KJetMetadata, KL1Muon, KLepton, KMuon, KMuonTriggerCandidate,
  KParticle, KPhoton, KTau, KTrack, KTriggerObjects,
  KTriggerObjectMetadata.
- All producers run without extra CMSSW configs
- Add Minimal Kappa config
- Sort Skimming folder



## Important files to look at

### [DataFormats](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats)
Data formats for objects that can be skimmed with Kappa
   * [DataFormats/interface](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/interface)
   * the file names and class names tell you the object it defines according to the [naming scheme](#main-naming)
   * these are the variables and functions you can use in the analysis
       * many classes come with functions that can combine information of the variables
   * [DataFormats/src/classes.UP](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/src/classes.UP)
       * be sure to run classes.UP whenever you change the data format to keep the information for dictionaries in sync
   * [DataFormats/test/KDebug.cpp](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/test/KDebug.cpp)
       * add debug information for all added or changed objects here
       * this will enable you to print out debug info later in the analysis: `cout << muon;`

### [Producers](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Producers)

The actual code that runs while skimming
   * [Producers/interface/README](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Producers/interface/README) (todo: get this up-to-date, perhaps graphically)
      * classes hierarchy of Producers, you should know this when writing producers
      * WP = with provenance
      * some objects exist once per event (KBaseMultiProducers produce them; like beam spot, MET)
      * some objects can exist multiple times per event (KBaseMultiVectorProducers produce them; like primary vertices or hits)
      * some objects can exist multiple times and are Lorentz vectors (KBaseMultiLVProducers produce them; like muons, jets, taus, etc.)
   * [Producers/python/KTuple_cff.py](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Producers/python/KTuple_cff.py)
      * default settings for Kappa and its Producers
      * all those can be changed in your skim config
   * [Producers/src/KTuple.cc](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Producers/src/KTuple.cc)
      * the EDAnalyzer, this is the starting point of processing with Kappa

### [Skimming](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Skimming)
Configuration files. Most of them are outdated – be careful and look at the CMSSW versions and the modification date.

Here, the default settings are overwritten for special analyses and use cases.
   * [Skimming/skim_tutorial_53x.py](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Skimming/skim_tutorial_53x.py)
       * an example config that should run with 5.3.9, it needs some extra packages that should be listed here or in this config, to be done)

## Adding/Changing Objects

### Changing the way some existing object is filled
Just change the producer and recompile.

### Changing the content of an existing object
Recompiling regenerates the dictionaries and makes the new definition available.

### Adding a new object
To add a new object to Kappa, it needs:
  * a data format in [DataFormats/interface](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/interface) (header only, please stick to the [naming scheme](#main-naming).)
      * if it can occur multiple times, a typedef for a std::vector by appending 's' (plural).
  * a producer in [Producers](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Producers) (it makes sense to look at a similar object first)
  * a default config in [Producers/python/KTuple_cff.py](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/Producers/python/KTuple_cff.py)
  * debug output in [DataFormats/test/KDebug.cpp](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/test/KDebug.cpp)
  * an entry in [DataFormats/src/classes](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/src/classes)
      * run [DataFormats/src/classes.UP](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/src/classes.UP) afterwards (from within its directory)
  * the corresponding lines in [DataFormats/test/LinkDef.h](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/DataFormats/test/LinkDef.h)
  * the documentation in [docs/objects.md](https://github.com/KappaAnalysis/Kappa/tree/dictchanges/docs/objects.md)

________________________________________________________________________________

[KIT]:      http://www.ekp.kit.edu "Institut für Experimentelle Kernphysik"
[code]:     https://github.com/KappaAnalysis/Kappa.git "github"
[CMSSW]:    https://github.com/cms-sw/cmssw "CMSSW on github"
[CMS Wiki]: https://twiki.cern.ch/twiki/bin/viewauth/CMS/WebHome "CMS twiki"
[Workbook]: https://twiki.cern.ch/twiki/bin/viewauth/CMS/OnlineWB "CMS Workbook"
[Doxygen]:  http://www.stack.nl/~dimitri/doxygen/index.html "Doxygen"
[Markdown]: http://daringfireball.net/projects/markdown "Markdown"
