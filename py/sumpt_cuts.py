from ROOT import *
from unused_hits_fractions import *

max_elec_snr = 0
max_elec_jcfCut = 0
max_elec_filter_sig = 0
max_elec_filter_bg = 0

for jcfCut in list(linspace(0, 1, 10)):
    print jcfCut
    cut = 'jetroi_unusedhits_trt_fraction > 0.4 && (sumpttracksd0uppercut + sumpttracksd0lowercut) / jetroi_et < {0}'.format(jcfCut)
    # cut = '(sumpttracksd0uppercut + sumpttracksd0lowercut) / jetroi_et < {0}'.format(jcfCut)
    cur_elec_bg, cur_elec_sig, cur_muon_bg, cur_muon_sig = DrawVarCut(cut)
    cur_filter_elec_bg, cur_filter_elec_sig, cur_filter_muon_bg, cur_filter_muon_sig = CalcFilteredFractions(cur_elec_bg, cur_elec_sig, cur_muon_bg, cur_muon_sig)

    print 'elec total filtered: {0}'.format((cur_elec_bg.GetEntries() + cur_elec_sig.GetEntries()) / (
        elec_file_new.elec_sig_uncut.GetEntries() + elec_file_new.elec_bg_uncut.GetEntries()))
    print 'muon total filtered: {0}'.format((cur_muon_bg.GetEntries() + cur_muon_sig.GetEntries()) / (
        elec_file_new.muon_sig_uncut.GetEntries() + elec_file_new.muon_bg_uncut.GetEntries()))

    if cur_filter_elec_bg == 0:
        cur_elec_snr = 0
    else:
        cur_elec_snr = cur_filter_elec_sig / cur_filter_elec_bg
    if cur_elec_snr > max_elec_snr:
        max_elec_snr = cur_elec_snr
        max_elec_jcfCut = jcfCut
        max_elec_filter_sig = cur_filter_elec_sig
        max_elec_filter_bg = cur_filter_elec_bg


print 'best cut: {0}'.format(max_elec_jcfCut)
print 'best snr: {0}'.format(max_elec_snr)
