# 13TeVLFV
Plotting scripts for LFV Higgs 13 TeV 
 
Summary: 
plot_13TeV_LFV.py does the dirty work, applying the fake rate method, filling empty bins appropriately, 
scaling histograms appropriately, etc. Then it makes datacards and basic plots of the datacards. 
plot_13TeV_FromDataCards_Combined.py is a streamlined plotting script that plots directly from the datacards. 
 
################################################################################################################### 
plot_13TeV_LFV: 
 
plot_13TeV_LFV.py creates basic plots (not pretty plots for PAS) and creates datacards. 
It loads XSec.py, which contains cross sections for each sample, and lfv_vars.py, which arranges the legends 
and other plotting information for each variable.

Usage: plot_13TeV_LFV.py [dirname] [varname] [channel] [lumi] [systematic]

dirname is the directory where the .root histograms are stored. It also must contain a folder named "weights/" that 
contains the weights for each histogram, as output by the setup.sh script.

varname is the variable being plotted

channel is the channel being plotted 

lumi is the luminosity to scale to. The scaling ability was built to be able to scale to higher luminosities and 
project future results. In a standard analysis you should input 0 as the lumi, then the lumi will default to the 
value of JSONlumi, defined in the script.

systematic is the systematic that is being plotted. If no systematic, use "none". Options are "JesUp", "JesDown", 
"TesUp", "TesDown", "UesUp","UesDown","FakesUp","FakesDown", and "none". 
The directory that contains the shifted histograms should have the systematic name added to it at the end. 
For example, if the unshifted histograms are stored in 76X_V2_MuonFix_March30/ then the fakes shifted histograms 
should be stored in 76X_V2_MuonFix_March30_FakesUp/, 76X_V2_MuonFix_March30_FakesDown/ and so on.

An example of the script in action:

python plot_13TeV_LFV.py 76X_V2_MuonFix_March30/ mPt preselection 0 none

The above command will plot the histograms contained in 76X_V2_MuonFix_March30/ with respect to the 
muon Pt variable in the preselection channel. The default JSONlumi is used and no systematic shift is used. 
It also creates a .root datacard with the plotted histograms, ready to be used in the fitting process.

#######################################################################################################################
plot_13TeV_FromDataCards_Combined:

This script creates PAS ready plots from the datacards.

Usage: plot_13TeV_FromDataCards_Combined.py [dirname] [channel]

Dirname is the directory with the mlfit file.
Channel is the channel to be plotted.
        Options: mue0J, mue1J, mue2J, mutau0J, mutau1J, mutau2J
