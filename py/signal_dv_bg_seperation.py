from ROOT import *
from samplesInit import elec, muon, ttbar, dijet
from time import time

dvRoi_var = {}
bgRoi_var = {}

title = 'IBL hits ( > 0 ) - signal to background ratio'

# Read data from files and sort events into bacground and signal
start = time()
for tree in [(elec, 'elec'), (muon, 'muon')]:#, (ttbar, 'ttbar')]:#, (dijet, 'dijet')]:
    dvRoi_var[tree[1]] = []
    bgRoi_var[tree[1]] = []
    for event in tree[0]:
        # truth data tuples list
        truthDvRois = []

        # save event rois truth information data for later comparison
        if len(event.jetroimatched_pt) > 0:
            for i in range(len(event.jetroimatched_pt)):
                truthDvRois.append((event.jetroimatched_pt[i], event.jetroimatched_eta[i], event.jetroimatched_phi[i]))

        # look for roi data in truth data. If present, roi is signal, else, it is background
        for i in range(len(event.jetroi_et)):
            if (event.jetroi_et[i], event.jetroi_eta[i], event.jetroi_phi[i]) in truthDvRois:
                cur_var = dvRoi_var
            else:
                cur_var = bgRoi_var
            # choose data for histograms here
            if event.track_trthits[i] > 0:
                cur_var[tree[1]].append(event.jetroi_unusedhits_fraction[i])

end = time()
print 'first part: {0}'.format(end - start)
# calculate maximal number of tracks for the histogram scale
# globalMax = max(max(dvRoi_var), max(bgRoi_var))
# sumHist = TH1F('sum_ntracks','', globalMax + 1, 0, globalMax)

# signalType > fileName > ntracks

# fill the bg/signall histograms for each file
start = time()
hists = []
for dataType in [(dvRoi_var, 'signal'), (bgRoi_var, 'bg')]:
    xRoi_var = dataType[0]
    hist_len = max([max(xRoi_var[fileName]) for fileName in xRoi_var.keys() if len(xRoi_var[fileName]) > 0])
    curHist = TH1F(dataType[1], title, hist_len + 1, 0, hist_len)
    for fileName in xRoi_var.keys():
        var_data = xRoi_var[fileName]
        if len(var_data) == 0:
            continue
        # curHist = TH1F('{0} {1}'.format(dataType[1], fileName), title, max(var_data) + 1, 0, max(var_data))
        # sum = 0
        for var in var_data:
            curHist.Fill(var)
            # sum += var
        # curHist.Fill(sum)
        # hists.append(curHist)
    hists.append(curHist)




end = time()
print 'second part: {0}'.format(end - start)

# Draw the histograms
start = time()
lgd = TLegend(0.6, 0.6, 0.9, 0.8)

for i in range(len(hists)):
    curHist = hists[i]
    curHist.SetLineColor(i + 1 if i != 4 else 6)
    curHist.Scale(1 / curHist.Integral())
    curHist.Draw('same')
    lgd.AddEntry(curHist, '{0}: {1}'.format(curHist.GetName(), int(curHist.GetEntries())))

lgd.SetTextSize(0.033)
lgd.Draw()

end = time()
print 'third part: {0}'.format(end - start)

c2 = TCanvas()
c2.cd()
histMax = max([hist.GetNbinsX() for hist in hists])
sbrHist = TH1F('sbr', 'Signal/Bacground ratio - TRT', histMax, 1.0, histMax)
for i in range(1, histMax):
    sigValue = hists[0].GetBinContent(i)
    bgValue = hists[1].GetBinContent(i)
    sbrHist.SetBinContent(i, sigValue/bgValue if bgValue > 0 else 0)

sbrHist.Draw()
