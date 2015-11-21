from ROOT import *
from samplesInit import elec

dvRoi_var = {}
bgRoi_var = {}
count = 0
roi_limit = 1000
for tree in [(elec, 'elec')]:  # , (muon, 'muon'), (dijet, 'dijet'), (ttbar, 'ttbar')]:
    dvRoi_var[tree[1]] = []
    bgRoi_var[tree[1]] = []
    treeName = tree[1]
    for event in tree[0]:
        # truth data tuples list
        truthDvRois = []

        # save event rois truth information data for later comparison
        if len(event.jetroimatched_pt) > 0:
            for roi_index in range(len(event.jetroimatched_pt)):
                truthDvRois.append((event.jetroimatched_pt[roi_index], event.jetroimatched_eta[roi_index],
                                    event.jetroimatched_phi[roi_index]))

        # look for roi data in truth data. If present, roi is signal, else, it is background
        for roi_index in range(len(event.jetroi_et)):
            roiDataTuple = (event.jetroi_et[roi_index], event.jetroi_eta[roi_index], event.jetroi_phi[roi_index])
            if roiDataTuple in truthDvRois:
                cur_var = dvRoi_var
            else:
                cur_var = bgRoi_var

            cur_var[treeName].append((event.ntracks[roi_index], event.jetroi_et[roi_index]))
            # cur_var[treeName].append([])
            # for track_index in range(event.tracktoroi_index[roi_index],
            #                          event.tracktoroi_index[roi_index] + event.ntracks[roi_index]):
            #     cur_var[treeName][len(cur_var[treeName]) - 1].append(event.track_d0[track_index])
            # count += 1
        # if count >= roi_limit:
        #     break

mg = TMultiGraph()

length = min(len(dvRoi_var['elec']), len(bgRoi_var['elec']))
for sigType in [bgRoi_var, dvRoi_var]:
    i = 0
    g = TGraph(length)
    # for roi_index in range(min(len(sigType['elec']), roi_limit)):
    for roi_index in range(length):
        g.SetPoint(roi_index, sigType['elec'][roi_index][0], sigType['elec'][roi_index][1])
        # for d0 in sigType['elec'][roi_index]:
        #     g.SetPoint(i, roi_index, d0)
        #     i += 1

    g.SetMarkerColor(1 if sigType == dvRoi_var else 2)
    g.SetMarkerStyle(2 if sigType == dvRoi_var else 5)
    mg.Add(g)

mg.Draw('ap')
mg.GetXaxis().SetTitle('ntracks')
mg.GetYaxis().SetTitle('jetroi_et')
