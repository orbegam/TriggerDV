//
// This tutorials demonstrate how to store and restore simple vectors
// in a TTree
//

#include <vector>

#include "TFile.h"
#include "TTree.h"
#include "TSystem.h"

#ifdef __MAKECINT__
#pragma link C++ class vector<float>+;
#endif

void read(char *filename, char *friend_name)
{

   TFile *f = TFile::Open(filename, "update");
   // TFile *frnd_f = TFile::Open(friend_name, "recreate");

   if (!f) { return; }

   TTree *t; f->GetObject("RPVMCInfoTree",t);
   // TTree *frnd_t = new TTree("RPVMCFriend","Track matching tree");

   // jetroimatched
   std::vector<int> *jrmV = 0;
   TBranch *jrmB = 0;
   t->SetBranchAddress("jetroimatched", &jrmV, &jrmB);
   
   // track2roi_index
   std::vector<int> *track2roiV = 0;
   TBranch *track2roiB = 0;
   t->SetBranchAddress("tracktoroi_index", &track2roiV, &track2roiB);
   
   // track_d0 (just to see the length of it)
   std::vector<float> *track_d0V = 0;
   TBranch *track_d0B = 0;
   t->SetBranchAddress("track_d0", &track_d0V, &track_d0B);
   
   // track_matched - new branch
   std::vector<int> *track_matchedV = 0;
   TBranch *track_matchedB = t->Branch("track_matched", &track_matchedV);

   for (Int_t i = 0; i < 1; i++) {
      Long64_t event = t->LoadTree(i);

      jrmB->GetEntry(event);
      track2roiB->GetEntry(event);
      track_d0B->GetEntry(event);

      UInt_t roi_ind;
      for (roi_ind = 0; roi_ind < jrmV->size() - 1; ++roi_ind) {
         int tracksInRoi = track2roiV->at(roi_ind + 1) - track2roiV->at(roi_ind);
         printf("%d\n", tracksInRoi);
         for (int track_ind = 0; track_ind < tracksInRoi; track_ind++) {
            track_matchedV->push_back(jrmV->at(roi_ind));
         }
      }

      // handle last roi seperately
      for (int track_ind = 0; track_ind < track_d0V->size() - track2roiV->at(roi_ind); track_ind++) {
         track_matchedV->push_back(jrmV->at(roi_ind));
      }

      track_matchedB.Fill();
   }

   // Since we passed the address of a local variable we need
   // to remove it.
   t->Write();
   t->ResetBranchAddresses();
   f->Close();
   // frnd_f->cd();
   // frnd_t->Write();
   // frnd_f->Close();
}


void track_labeling()
{
   //write();
   read("C:\\orb\\School\\ATLAS\\Data\\TriggerRun2_samples\\rpvmcplustrigger_elec_202882_v1_20150924.root",
         "C:\\orb\\School\\ATLAS\\Data\\TriggerRun2_samples\\rpvmcplustrigger_elec_friend.root");
}
