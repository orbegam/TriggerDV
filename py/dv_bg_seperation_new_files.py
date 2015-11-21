from samplesInit import elec_new, muon_new, dijet_new

signal_data = []
bg_data = []

for namedTree in [elec_new, muon_new]:
    for event in namedTree.tree:
        isSignal = event.jetroimatched != -1

