from ROOT import *
from samplesInit import elec_new, muon_new, elec_file_new

var = '(sumpttracksd0uppercut + sumpttracksd0lowercut) / jetroi_et:(dv_X^2 + dv_Y^2 + dv_Z^2)^0.5'
cut = '1==1'

elec_new.Draw(var, cut + '&& jetroimatched == -1')
elec_bg_graph = TGraph(elec_new.GetSelectedRows(), elec_new.GetV2(), elec_new.GetV1())
elec_new.Draw(var, cut + '&& jetroimatched != -1')
elec_sig_graph = TGraph(elec_new.GetSelectedRows(), elec_new.GetV2(), elec_new.GetV1())

muon_new.Draw(var, cut + '&& jetroimatched == -1')
muon_bg_graph = TGraph(muon_new.GetSelectedRows(), muon_new.GetV2(), muon_new.GetV1())
muon_new.Draw(var, cut + '&& jetroimatched != -1')
muon_sig_graph = TGraph(muon_new.GetSelectedRows(), muon_new.GetV2(), muon_new.GetV1())

elec_bg_graph.SetMarkerColor(1)     # black
elec_sig_graph.SetMarkerColor(2)    # red
muon_bg_graph.SetMarkerColor(3)     # green
muon_sig_graph.SetMarkerColor(4)    # blue

for graph in [elec_bg_graph, elec_sig_graph, muon_bg_graph, muon_sig_graph]:
    graph.SetMarkerStyle(2)

mg = TMultiGraph()
mg.Add(elec_bg_graph)
mg.Add(elec_sig_graph)
mg.Add(muon_bg_graph)
mg.Add(muon_sig_graph)

mg.Draw("ap")
