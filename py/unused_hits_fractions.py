from ROOT import *
from samplesInit import elec_new, muon_new, dijet_new, ttbar_new, elec_file_new

elec_bg_count = 87578
elec_sig_count = 98978
muon_bg_count = 98393
muon_sig_count = 92499
dijet_bg_count = 16525
ttbar_bg_count = 2117592
var = ''
cut = ''

#var += '(sumpttracksd0lowercut + sumpttracksd0uppercut) / jetroi_et'
# cut += '(sumpttracksd0lowercut + sumpttracksd0uppercut) / jetroi_et <= 0.3 && '

var += 'track_scthits:track_pixhits'
cut += '1==1'#track_d0 < 1'

lgd = TLegend(0.15, 0.65, 0.4, 0.85)
lgd.SetTextSize(0.033)

elec_new.Draw(var + ' >> elec_bg_uncut', 'jetroimatched == -1')
elec_new.Draw(var + ' >> elec_sig_uncut', 'jetroimatched != -1')
muon_new.Draw(var + ' >> muon_bg_uncut', 'jetroimatched == -1')
muon_new.Draw(var + ' >> muon_sig_uncut', 'jetroimatched != -1')
dijet_new.Draw(var + ' >> dijet_bg_uncut')
ttbar_new.Draw(var + ' >> ttbar_bg_uncut')

elec_new.Draw(var + ' >> elec_bg', cut + '&& jetroimatched == -1', '')
elec_new.Draw(var + ' >> elec_sig', cut + '&& jetroimatched != -1', 'same')
muon_new.Draw(var + ' >> muon_bg', cut + '&& jetroimatched == -1', 'same')
muon_new.Draw(var + ' >> muon_sig', cut + '&& jetroimatched != -1', 'same')
dijet_new.Draw(var + ' >> dijet_bg', cut, 'same')
ttbar_new.Draw(var + ' >> ttbar_bg', cut, 'same')

elec_bg = elec_file_new.elec_bg
elec_sig = elec_file_new.elec_sig
elec_bg.SetLineColor(2)
elec_sig.SetLineColor(4)
elec_bg.Scale(1 / elec_file_new.elec_bg_uncut.Integral())
elec_sig.Scale(1 / elec_file_new.elec_sig_uncut.Integral())
lgd.AddEntry(elec_bg, "elec bg " + str(elec_bg.GetEntries() / elec_bg_count), 'l')
lgd.AddEntry(elec_sig, "elec sig " + str(elec_sig.GetEntries() / elec_sig_count), 'l')

muon_bg = elec_file_new.muon_bg
muon_sig = elec_file_new.muon_sig
muon_bg.SetLineColor(1)
muon_sig.SetLineColor(6)
muon_bg.Scale(1 / elec_file_new.muon_bg_uncut.Integral())
muon_sig.Scale(1 / elec_file_new.muon_sig_uncut.Integral())
lgd.AddEntry(muon_bg, "muon bg " + str(muon_bg.GetEntries() / muon_bg_count), 'l')
lgd.AddEntry(muon_sig, "muon sig " + str(muon_sig.GetEntries() / muon_sig_count), 'l')

dijet_bg = elec_file_new.dijet_bg
dijet_bg.SetLineColor(3)
lgd.AddEntry(dijet_bg, "dijet bg " + str(dijet_bg.GetEntries() / dijet_bg_count), 'l')
dijet_bg.Scale(1 / elec_file_new.dijet_bg_uncut.Integral())

ttbar_bg = elec_file_new.ttbar_bg
ttbar_bg.SetLineColor(8)
lgd.AddEntry(ttbar_bg, "ttbar bg " + str(ttbar_bg.GetEntries() / ttbar_bg_count), 'l')
ttbar_bg.Scale(1 / elec_file_new.ttbar_bg_uncut.Integral())

lgd.Draw()

print 'elec total filtered: {0}'.format((elec_bg.GetEntries() + elec_sig.GetEntries()) / (elec_sig_count + elec_bg_count))
print 'muon total filtered: {0}'.format((muon_bg.GetEntries() + muon_sig.GetEntries()) / (muon_sig_count + muon_bg_count))
