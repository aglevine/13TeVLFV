from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import array

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

channelTight=argv[1]
channelLoose=argv[2]
var=argv[3]

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
canvas.SetGrid()

#mmtFile = ROOT.TFile("MariaNtuples_Oct13_MM/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root")
mmtFile = ROOT.TFile("MariaNtuples_Oct13_MM/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
mmtLoose = mmtFile.Get(channelLoose+"/"+var)
mmtTight = mmtFile.Get(channelTight+"/"+var)

data2015CFile = ROOT.TFile("MariaNtuples_Oct13_MM/data_SingleMuon_Run2015C_05Oct2015_25ns.root")
data2015CLoose = data2015CFile.Get(channelLoose+"/"+var)
data2015CTight = data2015CFile.Get(channelTight+"/"+var)

data2015DFile = ROOT.TFile("MariaNtuples_Oct13_MM/data_SingleMuon_Run2015D_05Oct2015_25ns.root")
data2015DLoose = data2015DFile.Get(channelLoose+"/"+var)
data2015DTight = data2015DFile.Get(channelTight+"/"+var)

data2015Dv4File = ROOT.TFile("MariaNtuples_Oct13_MM/data_SingleMuon_Run2015D_PromptReco-v4_25ns.root")
data2015Dv4Loose = data2015Dv4File.Get(channelLoose+"/"+var)
data2015Dv4Tight = data2015Dv4File.Get(channelTight+"/"+var)

dataLoose = data2015CLoose.Clone()
dataLoose.Add(data2015DLoose)
dataLoose.Add(data2015Dv4Loose)

dataTight = data2015CTight.Clone()
dataTight.Add(data2015DTight)
dataTight.Add(data2015Dv4Tight)

xBins = array.array('d',[35,45,55,75,100,200])

if ("tDecayMode" not in var and "tPt" not in var):
	mmtLoose.Rebin(10)
	mmtTight.Rebin(10)
        dataLoose.Rebin(10)
        dataTight.Rebin(10)
if("tPt" in var):
        mmtLoose.Rebin(len(xBins)-1,"mmtLooseRebinned",xBins)
        mmtTight.Rebin(len(xBins)-1,"mmtTightRebinned",xBins)
        mmtLooseRebinned = ROOT.gDirectory.Get("mmtLooseRebinned")
        mmtTightRebinned = ROOT.gDirectory.Get("mmtTightRebinned")
        mmtLoose = mmtLooseRebinned.Clone()
        mmtTight = mmtTightRebinned.Clone()
        dataLoose.Rebin(len(xBins)-1,"dataLooseRebinned",xBins)
        dataTight.Rebin(len(xBins)-1,"dataTightRebinned",xBins)
        dataLooseRebinned = ROOT.gDirectory.Get("dataLooseRebinned")
        dataTightRebinned = ROOT.gDirectory.Get("dataTightRebinned")
        dataLoose = dataLooseRebinned.Clone()
        dataTight = dataTightRebinned.Clone()

fakeRate = mmtTight.Clone()
if ("m1_m2" not in var):
	fakeRate.Divide(mmtLoose)
if ("m1_m2" in var):
	#fakeRate.Scale(6025.2*1253/28747969.000000)
        fakeRate.Scale(6025*1253/9042031.000000)
fakeRate.SetMarkerStyle(20)
fakeRate.SetMarkerColor(ROOT.EColor.kRed)
fakeRate.SetMarkerSize(1.5)

fakeRateData = dataTight.Clone()
if ("m1_m2" not in var):
	fakeRateData.Divide(dataLoose)
fakeRateData.SetMarkerStyle(20)
fakeRateData.SetMarkerColor(ROOT.EColor.kBlue)
fakeRateData.SetMarkerSize(1.5)
fakeRateData.SetTitle("")

fakeRate.Draw("ep")
fakeRateData.Draw("epsames")
maxy = max(fakeRate.GetMaximum(),fakeRateData.GetMaximum())*1.1

if ("m1_m2" not in var):
	fakeRate.GetYaxis().SetRangeUser(0,1.1)
else:
	fakeRate.GetYaxis().SetRangeUser(0,1.1*maxy)

legend = ROOT.TLegend(0.55,0.6,0.8,0.90,' ','brNDC')
legend.AddEntry(fakeRate,"DY MC")
legend.AddEntry(fakeRateData,"Data")

legend.Draw("sames")

if ("Eta" in var):
  fakeRate.GetXaxis().SetTitle("#tau Eta")
elif ("Pt" in var):
  fakeRate.GetXaxis().SetTitle("#tau Pt")
if ("DecayMode" in var):
  fakeRate.GetXaxis().SetTitle("#tau Decay Mode")
  print "decay mode 0: " + str(fakeRateData.GetBinContent(1))
  print "decay mode 1: " + str(fakeRateData.GetBinContent(2))
  print "decay mode 10: " + str(fakeRateData.GetBinContent(11))

canvas.SaveAs("FakesEtaCut_Nov24/"+channelTight+"_"+channelLoose+"_"+var+"_fakeRate.png")
