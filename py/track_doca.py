from ROOT import *
import time
from samplesInit import *
import math


def poca(vD, vL, pL):
    distance = pL.Dot(vD - vL) / pL.Mag2()
    return vL + distance * pL


def doca(vD, vL, pL):
    # TODO: replace this code with something like the algorithm described in:
    # http://mipp-docdb.fnal.gov/cgi-bin/RetrieveFile?docid=415&filename=dca_vert.pdf
    pocaV3 = poca(vD, vL, pL)
    return (pocaV3 - vD).Mag(), pocaV3


def trackToVectors(d0, z0, eta, phi, pt):
    r = TVector3(d0 * math.cos(phi), d0 * math.sin(phi), z0)
    p = TVector3()
    p.SetPtEtaPhi(pt, eta, phi)
    return r, p


def trackCoordsFromEvent(event, trackInd):
    d0 = event.track_d0[trackInd]
    z0 = event.track_z0[trackInd]
    eta = event.track_eta[trackInd]
    phi = event.track_phi[trackInd]
    pt = event.track_pt[trackInd]

    return d0, z0, eta, phi, pt


def genpCoordsFromEvent(event, genpInd):
    x = event.genpfromdv_vx[genpInd]
    y = event.genpfromdv_vy[genpInd]
    z = event.genpfromdv_vz[genpInd]
    eta = event.genpfromdv_eta[genpInd]
    phi = event.genpfromdv_phi[genpInd]
    pt = event.genpfromdv_pt[genpInd]

    return x, y, z, eta, phi, pt


def findClosestGenP(genPs, vertex):
    min_dist = 99999999999
    closestGenP = None
    for coords in genPs:
        gx, gy, gz, geta, gphi, gpt = coords
        distance = math.sqrt((vertex.x() - gx)**2 + (vertex.y() - gy)**2 + (vertex.z() - gz)**2)
        if distance < min_dist:
            min_dist = distance
            closestGenP = coords

    return closestGenP, distance


def DoDoca():
    start = time.time()
    totalRoisSignal = 0
    totalRoisBg = 0
    smallDocaRoisSignal = 0
    smallDocaRoisBg = 0
    for event in elec_new.tree:
        # # save event rois truth information data for later comparison
        # truthDvRois = []
        # if len(event.jetroimatched_pt) > 0:
        #     for roi_index in range(len(event.jetroimatched_pt)):
        #         truthDvRois.append((event.jetroimatched_pt[roi_index], event.jetroimatched_eta[roi_index],
        #                             event.jetroimatched_phi[roi_index]))


        verticesPlot = TGraph()

        # save event track truth information
        genPs = []
        for genp_index in range(event.nTrk1mm):
            genPs.append(genpCoordsFromEvent(event, genp_index))

            # TODO: add all genp vertices to the plot. later add all constructed vertices,
            # and then draw the plot to see if it makes sense.

        for roiInd in range(len(event.tracktoroi_index)):
            # roiDataTuple = (event.jetroi_et[roiInd], event.jetroi_eta[roiInd], event.jetroi_phi[roiInd])
            # roiIsSignal = False
            # if roiDataTuple in truthDvRois:
            #     roiIsSignal = True
            roiHasSmallDocaTrack = False

            roiIsSignal = event.jetroimatched_pt != -1

            if roiIsSignal:
                totalRoisSignal += 1
            else:
                totalRoisBg += 1

            firstTrackInd = event.tracktoroi_index[roiInd]
            trackCount = event.ntracks[roiInd]
            for track1Ind in range(firstTrackInd, firstTrackInd + trackCount):
                # Check only tracks with d0 > 1mm and pt > 2GeV
                if event.track_d0[track1Ind] < 1 or event.track_pt[track1Ind] < 2000:
                    continue

                coords1 = d0, z0, eta, phi, pt = trackCoordsFromEvent(event, track1Ind)
                r1, p1 = trackToVectors(d0, z0, eta, phi, pt)

                for track2Ind in range(firstTrackInd, firstTrackInd + trackCount):
                    # Check only tracks with d0 > 1mm
                    if event.track_d0[track2Ind] < 1:
                        continue

                    coords2 = d02, z02, eta2, phi2, pt2 = trackCoordsFromEvent(event, track2Ind)
                    if coords1 == coords2:
                        continue

                    r2, p2 = trackToVectors(d02, z02, eta2, phi2, pt2)
                    tracksDoca, tracksPoca = doca(r1, r2, p2)

                    closestGenP, distToGenP = findClosestGenP(genPs, tracksPoca)

                    if tracksDoca < 1:
                        roiHasSmallDocaTrack = True
                        print '{1}. tracks: {0}'.format(trackCount, roiIsSignal)
                        print tracksDoca, tracksPoca.x(), tracksPoca.y(), tracksPoca.z()
                        break

                if roiHasSmallDocaTrack:
                    break

            if roiHasSmallDocaTrack:
                if roiIsSignal:
                    smallDocaRoisSignal += 1
                else:
                    smallDocaRoisBg += 1
    print 'Signal: {0} / {1} ({2})'.format(smallDocaRoisSignal, totalRoisSignal,
                                           float(smallDocaRoisSignal) / totalRoisSignal)
    print 'Bg: {0} / {1} ({2})'.format(smallDocaRoisBg, totalRoisBg, float(smallDocaRoisBg) / totalRoisBg)
    print 'elapsed: {0}'.format(time.time() - start)


DoDoca()
