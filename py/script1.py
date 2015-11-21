from ROOT import *
from samplesInit import elec, muon, ttbar, dijet, elec_file

var = 'dv_Y:dv_X'
cut = ''

dijet.Draw(var + ' >> dijet_ntrack', cut, '')
ttbar.Draw(var + ' >> ttbar_ntrack', cut, 'same')
muon.Draw(var + ' >> muon_ntrack', cut, 'same')
elec.Draw(var + ' >> elec_ntrack', cut, 'same')

dijet_ntrack = elec_file.dijet_ntrack
ttbar_ntrack = elec_file.ttbar_ntrack
muon_ntrack = elec_file.muon_ntrack
elec_ntrack = elec_file.elec_ntrack

dijet_ntrack.SetLineColor(1)
ttbar_ntrack.SetLineColor(2)
muon_ntrack.SetLineColor(3)
elec_ntrack.SetLineColor(4)

lgd = TLegend(0.55, 0.5, 0.95, 0.7)
lgd.SetTextSize(0.033)
lgd.AddEntry(elec_ntrack, "Signal (Electron) " + str(elec_ntrack.GetEntries()), 'l')
lgd.AddEntry(muon_ntrack, "signal (muon) " + str(muon_ntrack.GetEntries()), 'l')
lgd.AddEntry(dijet_ntrack, "Background (dijet) " + str(dijet_ntrack.GetEntries()), 'l')
lgd.AddEntry(ttbar_ntrack, "Background (ttbar) " + str(ttbar_ntrack.GetEntries()), 'l')
lgd.Draw()

dijet_ntrack.Scale(1 / dijet_ntrack.Integral())
ttbar_ntrack.Scale(1 / ttbar_ntrack.Integral())
muon_ntrack.Scale(1 / muon_ntrack.Integral())
elec_ntrack.Scale(1 / elec_ntrack.Integral())

