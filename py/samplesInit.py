from ROOT import *
from collections import namedtuple

NamedTree = namedtuple('NamedTree', ['tree', 'name'])

# Background
dijet_file = TFile(r'C:\Orb\School\ATLAS\Data\rpvmcplustrigger_dijetJF17_129160.root')
ttbar_file = TFile(r'C:\Orb\School\ATLAS\Data\rpvmcplustrigger_ttbar_110401.root')
# Signal
muon_file = TFile(r'C:\Orb\School\ATLAS\Data\rpvmcplustrigger_muon_177568.root')
elec_file = TFile(r'C:\Orb\School\ATLAS\Data\rpvmcplustrigger_elec_202882.root')

dijet = dijet_file.RPVMCInfoTree
ttbar = ttbar_file.RPVMCInfoTree
muon = muon_file.RPVMCInfoTree
elec = elec_file.RPVMCInfoTree

# Background
dijet_file_new = TFile(r'C:\Orb\School\ATLAS\Data\TriggerRun2_samples\rpvmcplustrigger_dijetJF17_129160_v1_20150924.root')
ttbar_file_new = TFile(r"C:\Orb\School\ATLAS\Data\TriggerRun2_samples\rpvmcplustrigger_ttbar_110401_v1_20150924.root")
# Signal
muon_file_new = TFile(r'C:\Orb\School\ATLAS\Data\TriggerRun2_samples\rpvmcplustrigger_muon_177568_v1_20150924.root')
elec_file_new = TFile(r'C:\Orb\School\ATLAS\Data\TriggerRun2_samples\rpvmcplustrigger_elec_202882_v1_20150924.root')

dijet_new = dijet_file_new.RPVMCInfoTree
ttbar_new = ttbar_file_new.RPVMCInfoTree
muon_new = muon_file_new.RPVMCInfoTree
elec_new = elec_file_new.RPVMCInfoTree
