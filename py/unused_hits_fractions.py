from __future__ import division
from ROOT import *
from samplesInit import elec_new, muon_new, dijet_new, ttbar_new, elec_file_new


def DrawVarCut(var, cut):
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

    lgd = TLegend(0.15, 0.65, 0.4, 0.85)
    lgd.SetTextSize(0.033)

    elec_bg = elec_file_new.elec_bg
    elec_sig = elec_file_new.elec_sig
    elec_bg.SetLineColor(2)
    elec_sig.SetLineColor(4)
    elec_bg.Scale(1 / elec_file_new.elec_bg_uncut.Integral())
    elec_sig.Scale(1 / elec_file_new.elec_sig_uncut.Integral())
    lgd.AddEntry(elec_bg, "elec bg " + str(elec_bg.GetEntries() / elec_file_new.elec_bg_uncut.GetEntries()), 'l')
    lgd.AddEntry(elec_sig, "elec sig " + str(elec_sig.GetEntries() / elec_file_new.elec_sig_uncut.GetEntries()), 'l')

    muon_bg = elec_file_new.muon_bg
    muon_sig = elec_file_new.muon_sig
    muon_bg.SetLineColor(1)
    muon_sig.SetLineColor(6)
    muon_bg.Scale(1 / elec_file_new.muon_bg_uncut.Integral())
    muon_sig.Scale(1 / elec_file_new.muon_sig_uncut.Integral())
    lgd.AddEntry(muon_bg, "muon bg " + str(muon_bg.GetEntries() / elec_file_new.muon_bg_uncut.GetEntries()), 'l')
    lgd.AddEntry(muon_sig, "muon sig " + str(muon_sig.GetEntries() / elec_file_new.muon_sig_uncut.GetEntries()), 'l')

    dijet_bg = elec_file_new.dijet_bg
    dijet_bg.SetLineColor(3)
    lgd.AddEntry(dijet_bg, "dijet bg " + str(dijet_bg.GetEntries() / elec_file_new.dijet_bg_uncut.GetEntries()), 'l')
    dijet_bg.Scale(1 / elec_file_new.dijet_bg_uncut.Integral())

    ttbar_bg = elec_file_new.ttbar_bg
    ttbar_bg.SetLineColor(8)
    lgd.AddEntry(ttbar_bg, "ttbar bg " + str(ttbar_bg.GetEntries() / elec_file_new.ttbar_bg_uncut.GetEntries()), 'l')
    ttbar_bg.Scale(1 / elec_file_new.ttbar_bg_uncut.Integral())

    lgd.Draw()
    return elec_bg, elec_sig, muon_bg, muon_sig


def CalcFilteredFractions(cur_elec_bg, cur_elec_sig, cur_muon_bg, cur_muon_sig):
    filter_elec_bg = cur_elec_bg.GetEntries() / elec_file_new.elec_bg_uncut.GetEntries()
    filter_elec_sig = cur_elec_sig.GetEntries() / elec_file_new.elec_sig_uncut.GetEntries()
    filter_muon_bg = cur_muon_bg.GetEntries() / elec_file_new.muon_bg_uncut.GetEntries()
    filter_muon_sig = cur_muon_sig.GetEntries() / elec_file_new.muon_sig_uncut.GetEntries()

    return filter_elec_bg, filter_elec_sig, filter_muon_bg, filter_muon_sig


def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i


var = '(sumpttracksd0uppercut + sumpttracksd0lowercut) / jetroi_et'
# cut = 'jetroi_unusedhits_trt_fraction > 0.4 && (sumpttracksd0uppercut + sumpttracksd0lowercut) / jetroi_et < 0.3'
cut = '(sumpttracksd0uppercut + sumpttracksd0lowercut) / jetroi_et < 1'
# cut = '1==1'

cur_elec_bg, cur_elec_sig, cur_muon_bg, cur_muon_sig = DrawVarCut(var, cut)
cur_filter_elec_bg, cur_filter_elec_sig, cur_filter_muon_bg, cur_filter_muon_sig = CalcFilteredFractions(cur_elec_bg, cur_elec_sig, cur_muon_bg, cur_muon_sig)

print 'elec total filtered: {0}'.format((cur_elec_bg.GetEntries() + cur_elec_sig.GetEntries()) / (
    elec_file_new.elec_sig_uncut.GetEntries() + elec_file_new.elec_bg_uncut.GetEntries()))
print 'muon total filtered: {0}'.format((cur_muon_bg.GetEntries() + cur_muon_sig.GetEntries()) / (
    elec_file_new.muon_sig_uncut.GetEntries() + elec_file_new.muon_bg_uncut.GetEntries()))


# print 'Cut: {0}'.format(cut)
#
#
# print 'elec bg filtered: {0}'.format(cur_filter_elec_bg)
# print 'elec sig filtered: {0}'.format(cur_filter_elec_sig)
# print 'elec snr: {0}'.format(cur_filter_elec_sig / cur_filter_elec_bg)
# print
# print 'muon bg filtered: {0}'.format(cur_filter_muon_bg)
# print 'muon sig filtered: {0}'.format(cur_filter_muon_sig)
# print 'elec snr: {0}'.format(cur_filter_muon_sig / cur_filter_muon_bg)
# print






