from ROOT import *
from samplesInit import *

# mg = TMultiGraph()
#
# for tree in [elec]:#, muon]:
#     g = TGraph()
#     pointCount = 0
#     for event in tree:
#         if len(event.dv_X) == 0:
#             continue
#         for lspIndex in range(len(event.dv_X)):
#             x = event.dv_X[lspIndex] - event.vx_LSP[lspIndex]
#             y = event.dv_Y[lspIndex] - event.vy_LSP[lspIndex]
#             if (abs(x) <= 300 and abs(y) <= 300):
#                 g.SetPoint(pointCount, x, y)
#             pointCount += 1
#     g.SetMarkerColor(2 if tree == elec else 4)
#     g.GetXaxis().SetRangeUser(-300, 300)
#     mg.Add(g)
#
# mg.Draw('ap col')
# mg.GetXaxis().SetTitle('dv_x')
# mg.GetYaxis().SetTitle('dv_y')

x = 'dv_Y - vy_LSP'
y = 'dv_X - vx_LSP'
muon.Draw('%s:%s' % (x, y), 'abs(%s) <= 500 && abs(%s) <= 500' % (x, y), 'surf')
