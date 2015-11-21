from ROOT import *
from samplesInit import elec_new, elec_file_new

xLayer = "track_blayer"
yLayer = "track_pixhits"
cut = "track_d0 < 1"

elec_new.Draw('{1}:{0} >> elec_sig'.format(xLayer, yLayer), cut + ' && track_matched != -1', 'box')
elec_sig = elec_file_new.elec_sig
elec_sig.Scale(1 / elec_sig.Integral())
elec_sig.SetLineColor(1)

elec_new.Draw('{1}:{0} >> elec_bg'.format(xLayer, yLayer), cut + ' && track_matched == -1', 'box')
elec_bg = elec_file_new.elec_bg
integral = elec_bg.Integral()
print integral
elec_bg.Scale(1 / integral)
elec_bg.SetLineColor(2)

elec_sig.Draw("box")
elec_bg.Draw("box same")
