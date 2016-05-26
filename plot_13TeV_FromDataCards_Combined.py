from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import math
import array
import lfv_vars
import XSec

def get_histos(savedir,filename, rootdir,histoname,postfit=True):
        inputFile = ROOT.TFile(savedir+"/"+filename)
        ROOT.gROOT.cd()
        print rootdir
        print histoname
        if postfit == True:
                fitHisto = inputFile.Get("shapes_fit_s/"+rootdir+"/"+histoname)
	else:
		fitHisto = inputFile.Get("shapes_prefit/"+rootdir+"/"+histoname)
        if "mue2" in rootdir:
                histo = ROOT.TH1D(histoname,histoname,6,0,300) #mue 2 Jet
        elif "mutauhad_2" in rootdir or "mutau2" in rootdir:
		histo = ROOT.TH1D(histoname,histoname,10,0,500) #mutau 2 Jet
	elif "mue" in rootdir:
		print "15 GeV bins"
		histo = ROOT.TH1D(histoname,histoname,20,0,300)# mue
        else:
		histo = ROOT.TH1D(histoname,histoname,25,0,500)#mutau
                
        for i in range(1,histo.GetNbinsX()+1):
                histo.SetBinContent(i,fitHisto.GetBinContent(i))
        return histo

##Set up style
JSONlumi = 2297.7
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.LoadMacro("CMS_lumi.C")


ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

savedir=argv[1]
rootdir = argv[2]
postfit = argv[3]
canvas = ROOT.TCanvas("canvas","canvas",800,800)

legend = ROOT.TLegend(0.65,0.60,0.93,0.98,' ','brNDC')
xRange = 300


p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0,1,1)
p_lfv.SetLeftMargin(0.2147651)
p_lfv.SetRightMargin(0.06543624)
p_lfv.SetTopMargin(0.04895105)
p_lfv.SetBottomMargin(0.305)
p_lfv.Draw()
p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.295)
p_ratio.SetLeftMargin(0.2147651)
p_ratio.SetRightMargin(0.06543624)
p_ratio.SetTopMargin(0.04895105)
p_ratio.SetBottomMargin(0.295)
p_ratio.SetGridy()
p_ratio.Draw()
p_lfv.cd()

dirMap = {"mue0J":"mue0J","mue1J" : "mue1J", "mue2J": "mue2J","mutau0J":"mutau0J","mutau1J" : "mutau1J", "mutau2J": "mutau2"}
mlfitMap = {"mue0J":"mlfit_MINOS_COMB_MINOS.root","mue1J" : "mlfit_MINOS_COMB_MINOS.root", "mue2J": "mlfit_MINOS_COMB_MINOS.root","mutau0J":"mlfit_MINOS_COMB_MINOS.root","mutau1J" : "mlfit_MINOS_COMB_MINOS.root", "mutau2J": "mlfit_MINOS_COMB_MINOS.root"}
dataFileMap = {"mue0J":"LFV_datacard_shape_EMU_0Jet.root","mue1J" : "LFV_datacard_shape_EMU_1Jet.root", "mue2J": "LFV_datacard_shape_EMU_2Jet.root","mutau0J":"LFV_datacard_shape_MUTAU_0Jet.root","mutau1J" : "LFV_datacard_shape_MUTAU_1Jet.root", "mutau2J": "LFV_datacard_shape_MUTAU_2Jet.root"}
dirDataMap = {"mue0J":"LFV_MuE_0Jet_1_13TeVMuE","mue1J" : "LFV_MuE_1Jet_1_13TeVMuE", "mue2J": "LFV_MuE_2Jet_1_13TeVMuE","mutau0J":"LFV_MuTau_0Jet_1_13TeVMuTau","mutau1J":"LFV_MuTau_1Jet_1_13TeVMuTau","mutau2J":"LFV_MuTau_2Jet_1_13TeVMuTau"}
maxHistMap = {"mue0J": 30, "mue1J": 35, "mue2J": 70,"mutau0J": 180, "mutau1J": 60, "mutau2J": 10}
outfileNameMap = {"mue0J":"LFVMuE_SR_OS_0Jet_UnBlinded_Postfit","mue1J" : "LFVMuE_SR_OS_1Jet_UnBlinded_Postfit", "mue2J": "LFVMuE_SR_OS_2Jet_UnBlinded_Postfit","mutau0J":"LFVMuTau_SR_OS_0Jet_UnBlinded_Postfit","mutau1J" : "LFVMuTau_SR_OS_1Jet_UnBlinded_Postfit", "mutau2J": "LFVMuTau_SR_OS_2Jet_UnBlinded_Postfit"} #only used for postfit
outfile_name = savedir+"/"+outfileNameMap[rootdir]
lumi = JSONlumi
print rootdir
inputFile = ROOT.TFile(savedir+"/"+dataFileMap[rootdir])
ROOT.gROOT.cd()
data = inputFile.Get(dirDataMap[rootdir]+"/data_obs")
ztautau = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"ZTauTau",postfit)
zjets = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"Zothers",postfit)
diboson = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"Diboson",postfit)
ttbar = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"TT",postfit)
if "mue" in rootdir:
	wjets = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"Fakes_HMuE",postfit)
elif "mutau" in rootdir:
        wjets = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"Fakes",postfit)
smhgg = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"ggHTauTau",postfit)
smhvbf = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"vbfHTauTau",postfit)
if "mue" in rootdir:
	wg = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"WG",postfit)
singlet = get_histos(savedir,mlfitMap[rootdir],dirMap[rootdir],"T",postfit)
gghmutau125 = get_histos(savedir, mlfitMap[rootdir],dirMap[rootdir],"LFVGG",False)
vbfhmutau125 = get_histos(savedir, mlfitMap[rootdir],dirMap[rootdir],"LFVVBF",False)

ttbar.Add(singlet) #merge ttbar and singlet

data.SetBinErrorOption(ROOT.TH1.kPoisson)
data.SetMarkerStyle(8)
data.SetMarkerSize(1)
data.SetLineColor(ROOT.EColor.kBlack)
gghmutau125.SetLineColor(ROOT.EColor.kRed)
gghmutau125.SetLineWidth(3)
smhgg.SetLineWidth(1)
smhgg.SetLineColor(ROOT.EColor.kBlack)
smhgg.SetFillColor(ROOT.EColor.kMagenta)
vbfhmutau125.SetLineColor(ROOT.EColor.kBlue)
vbfhmutau125.SetLineWidth(3)
vbfhmutau125.SetLineStyle(ROOT.ELineStyle.kSolid)
smhvbf.SetLineWidth(1)
smhvbf.SetMarkerSize(0)
smhvbf.SetLineColor(ROOT.EColor.kMagenta)
smhvbf.SetFillColor(ROOT.EColor.kMagenta)
wjets.SetFillColor(ROOT.EColor.kMagenta-10)
wjets.SetLineColor(ROOT.EColor.kMagenta+4)
wjets.SetLineWidth(1)
wjets.SetMarkerSize(0)
ztautau.SetFillColor(ROOT.EColor.kOrange-4)
ztautau.SetLineColor(ROOT.EColor.kOrange+4)
ztautau.SetLineWidth(1)
ztautau.SetMarkerSize(0)
zjets.SetFillColor(ROOT.EColor.kAzure+3)
zjets.SetLineColor(ROOT.EColor.kAzure+5)
zjets.SetLineWidth(1)
zjets.SetMarkerSize(0)
ttbar.SetFillColor(ROOT.EColor.kGreen+3)
ttbar.SetLineColor(ROOT.EColor.kBlack)
ttbar.SetLineWidth(1)
ttbar.SetMarkerSize(0)
diboson.SetFillColor(ROOT.EColor.kRed+2)
diboson.SetLineColor(ROOT.EColor.kRed+4)
diboson.SetLineWidth(1)
diboson.SetMarkerSize(0)
if "mue" in rootdir:
	wg.SetFillColor(ROOT.EColor.kCyan)
	wg.SetLineColor(ROOT.EColor.kCyan)
	wg.SetLineWidth(1)
	wg.SetMarkerSize(0)


smh = smhgg.Clone()
smh.Add(smhvbf)
LFVStack = ROOT.THStack("stack","")
LFVStack.Add(wjets)
if "mue" in rootdir:
	LFVStack.Add(wg)
LFVStack.Add(diboson)
LFVStack.Add(ttbar)
LFVStack.Add(zjets)
LFVStack.Add(ztautau)
LFVStack.Add(smh)

LFVStack.SetMaximum(maxHistMap[rootdir])
LFVStack.Draw('hist')
data.Draw("sames,E")

vbfhmutau125.Draw("hsame")
gghmutau125.Draw("hsame")

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

xbinLength = wjets.GetBinWidth(1)
widthOfBin = xbinLength

ylabel = " Events / " + str(int(widthOfBin)) + " GeV"

legend.Draw('sames')
LFVStack.GetXaxis().SetNdivisions(510)
#LFVStack.GetXaxis().SetTitleOffset(3.0)
#LFVStack.GetXaxis().SetLabelOffset(3.0)
LFVStack.GetXaxis().SetLabelSize(0.035)
LFVStack.GetYaxis().SetTitle(ylabel)
LFVStack.GetYaxis().SetTitleOffset(1.40)
LFVStack.GetYaxis().SetLabelSize(0.035)

LFVStack.GetXaxis().SetRangeUser(0,xRange)
if "mue" in rootdir:
	LFVStack.GetXaxis().SetTitle("M(#mu#tau_{e})_{col} [GeV]")
elif "mutau" in rootdir:
        LFVStack.GetXaxis().SetTitle("M(#mu#tau_{h})_{col} [GeV]")

widthOfBin = wjets.GetBinWidth(1)

size = wjets.GetNbinsX()
#build tgraph of systematic bands
xUncert = array.array('f',[])
yUncert = array.array('f',[])
exlUncert = array.array('f',[])
exhUncert = array.array('f',[])
eylUncert = array.array('f',[])
eyhUncert = array.array('f',[])
xUncertRatio = array.array('f',[])
yUncertRatio = array.array('f',[])
exlUncertRatio = array.array('f',[])
exhUncertRatio = array.array('f',[])
eylUncertRatio = array.array('f',[])
eyhUncertRatio = array.array('f',[])
binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)


for i in range(1,size+1):
	if "mue" in rootdir:
        	stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+ztautau.GetBinContent(i)+ttbar.GetBinContent(i)+diboson.GetBinContent(i)+wg.GetBinContent(i)
	elif "mutau" in rootdir:
		stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+ztautau.GetBinContent(i)+ttbar.GetBinContent(i)+diboson.GetBinContent(i)
        wjetsBinContent = wjets.GetBinContent(i)
        xUncert.append(wjets.GetBinCenter(i))
        yUncert.append(stackBinContent)
        xUncertRatio.append(wjets.GetBinCenter(i))
        yUncertRatio.append(0)
        
        exlUncert.append(binLength/2)
        exhUncert.append(binLength/2)
        exlUncertRatio.append(binLength/2)
        exhUncertRatio.append(binLength/2)
	if "mue" in rootdir:
		if postfit == False: #manually apply fakes uncertainty
                        wjetsError = math.sqrt(wjets.GetBinContent(i)*0.4*wjets.GetBinContent(i)*0.4 + wjets.GetBinError(i)*wjets.GetBinError(i))

		else:
			wjetsError = wjets.GetBinError(i)
		errTot = wjetsError+zjets.GetBinError(i)+ztautau.GetBinError(i)+ttbar.GetBinError(i)+diboson.GetBinError(i)+wg.GetBinError(i)
        	eylUncert.append(errTot)
        	eyhUncert.append(errTot)
	elif "mutau" in rootdir:
                if postfit == False: #manually apply fakes uncertainty
                        wjetsError = math.sqrt(wjets.GetBinContent(i)*0.3*wjets.GetBinContent(i)*0.3 + wjets.GetBinError(i)*wjets.GetBinError(i))

                else:
                        wjetsError = wjets.GetBinError(i)
		errTot = wjetsError+zjets.GetBinError(i)+ztautau.GetBinError(i)+ttbar.GetBinError(i)+diboson.GetBinError(i)
                eylUncert.append(errTot)
                eyhUncert.append(errTot)
        if (stackBinContent==0):
        	eylUncertRatio.append(0)
                eyhUncertRatio.append(0)
	else:
		if "mue" in rootdir:
        		eylUncertRatio.append(errTot/stackBinContent)
        		eyhUncertRatio.append(errTot/stackBinContent)
		elif "mutau" in rootdir:
                        eylUncertRatio.append(errTot/stackBinContent)
                        eyhUncertRatio.append(errTot/stackBinContent)

xUncertVec = ROOT.TVectorF(len(xUncert),xUncert)
yUncertVec = ROOT.TVectorF(len(yUncert),yUncert)
exlUncertVec = ROOT.TVectorF(len(exlUncert),exlUncert)
exhUncertVec = ROOT.TVectorF(len(exhUncert),exhUncert)
eylUncertVec = ROOT.TVectorF(len(eylUncert),eylUncert)
eyhUncertVec = ROOT.TVectorF(len(eyhUncert),eyhUncert)
systErrors = ROOT.TGraphAsymmErrors(xUncertVec,yUncertVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)

xUncertVecRatio = ROOT.TVectorF(len(xUncertRatio),xUncertRatio)
yUncertVecRatio = ROOT.TVectorF(len(yUncertRatio),yUncertRatio)
exlUncertVecRatio = ROOT.TVectorF(len(exlUncertRatio),exlUncertRatio)
exhUncertVecRatio = ROOT.TVectorF(len(exhUncertRatio),exhUncertRatio)
eylUncertVecRatio = ROOT.TVectorF(len(eylUncertRatio),eylUncertRatio)
eyhUncertVecRatio = ROOT.TVectorF(len(eyhUncertRatio),eyhUncertRatio)
systErrorsRatio = ROOT.TGraphAsymmErrors(xUncertVecRatio,yUncertVecRatio,exlUncertVecRatio,exhUncertVecRatio,eylUncertVecRatio,eyhUncertVecRatio)

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.03)
latex.SetTextAlign(31)
latexStr = "%.2f fb^{-1} (13 TeV)"%(lumi/1000)
latex.DrawLatex(0.9,0.96,latexStr)
latex.SetTextAlign(11)
if "mue0J" in rootdir:
        catString = "#mu#tau_{e} 0-Jet"
if "mue1J" in rootdir:
        catString = "#mu#tau_{e} 1-Jet"
if "mue2J" in rootdir:
        catString = "#mu#tau_{e} 2-Jet"
if "mutau0J" in rootdir:
        catString = "#mu#tau_{h} 0-Jet"
if "mutau1J" in rootdir:
        catString = "#mu#tau_{h} 1-Jet"
if "mutau2J" in rootdir:
        catString = "#mu#tau_{h} 2-Jet"
latex.DrawLatex(0.25,0.87,catString)
latex.SetTextAlign(11)
latex.SetTextFont(61)
latex.SetTextSize(0.04)
latex.DrawLatex(0.25,0.92,"CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.027)
latex.DrawLatex(0.35,0.92,"Preliminary")

#systErrors.SetFillStyle(3003)
systErrors.SetFillColorAlpha(ROOT.EColor.kGray+2,0.35)
systErrors.SetMarkerSize(0)
systErrors.Draw('E2,sames')
legend.AddEntry(data, 'Data #mu#tau_{e}',"lp")
if postfit == False:
        legend.AddEntry(systErrors,'Pre-fit background unc.','f')
else:
        legend.AddEntry(systErrors,'Post-fit background unc.','f')
legend.AddEntry(smh, 'SM Higgs','f')
legend.AddEntry(ztautau,'Z->#tau#tau','f')
legend.AddEntry(zjets,'Z->l^{+}l^{-}','f')
legend.AddEntry(ttbar,'t#bar{t}, t, #bar{t}','f')
legend.AddEntry(diboson,'VV',"f")
if "mue" in rootdir:
	legend.AddEntry(wg,"W#gamma","f")
legend.AddEntry(wjets,'Misidentified leptons','f')
legend.AddEntry(gghmutau125,'LFV GF Higgs (BR=1%)',"l")
legend.AddEntry(vbfhmutau125,'LFV VBF Higgs (BR=1%)',"l")

p_ratio.cd()
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
ratio = data.Clone()
mc = wjets.Clone()
mc.Add(zjets)
mc.Add(ztautau)
mc.Add(ttbar)
mc.Add(diboson)
if "mue" in rootdir:
	mc.Add(wg)
mc.Scale(-1)
ratio.Add(mc)
mc.Scale(-1)
ratio.Divide(mc)
ratio.Draw("E1")
systErrorsRatio.SetFillColorAlpha(ROOT.EColor.kGray+2,0.35)
systErrorsRatio.SetMarkerSize(0)
systErrorsRatio.Draw('E2,sames')
if "mue" in rootdir:
	ratio.GetXaxis().SetTitle("collinear M(#mu#tau_{e}) (GeV)")
elif "mutau" in rootdir:
        ratio.GetXaxis().SetTitle("collinear M(#mu#tau_{h}) (GeV)")
ratio.GetXaxis().SetTitleSize(0.12)
ratio.GetXaxis().SetNdivisions(510)
ratio.GetXaxis().SetTitleOffset(1.1)
ratio.GetXaxis().SetLabelSize(0.12)
ratio.GetXaxis().SetLabelFont(42)
ratio.GetYaxis().SetNdivisions(505)
ratio.GetYaxis().SetLabelFont(42)
ratio.GetYaxis().SetLabelSize(0.1)
ratio.GetYaxis().SetRangeUser(-1,1)
ratio.GetYaxis().SetTitle("#frac{Data-BG}{BG}")
ratio.GetYaxis().CenterTitle(1)
ratio.GetYaxis().SetTitleOffset(0.4)
ratio.GetYaxis().SetTitleSize(0.12)
ratio.SetTitle("")

ratio.GetXaxis().SetRangeUser(0,xRange)
if (postfit == False):
	outfile_name = savedir+"/"+rootdir+"prefit"
canvas.SaveAs(outfile_name+".png")
canvas.SaveAs(outfile_name+".pdf")

#print event yields

if (widthOfBin == 50):
        print "Signal Region Yields:"
        print "misidentified leptons: " +str(wjets.GetBinContent(3))
        print "Z->TauTau: " + str(ztautau.GetBinContent(3))
        print "ZZ, WW: " + str(diboson.GetBinContent(3))
	if "mue" in rootdir:
        	print "Wgamma: " +str(wg.GetBinContent(3))
	elif "mutau" in rootdir:
		print "Wgamma: -"
        print "Z->ll: " + str(zjets.GetBinContent(3))
        print "ttbar: " + str(ttbar.GetBinContent(3))
        print "t: " + str(singlet.GetBinContent(3))
        print "sm higgs: " + str(smhgg.GetBinContent(3)+smhvbf.GetBinContent(3))
	if "mue" in rootdir:
        	print "sum of backgrounds: " + str(wjets.GetBinContent(3)+ztautau.GetBinContent(3)+diboson.GetBinContent(3)+zjets.GetBinContent(3)+ttbar.GetBinContent(3)+singlet.GetBinContent(3)+smhgg.GetBinContent(3)+smhvbf.GetBinContent(3)+wg.GetBinContent(3))
	elif "mutau" in rootdir:
                print "sum of backgrounds: " + str(wjets.GetBinContent(3)+ztautau.GetBinContent(3)+diboson.GetBinContent(3)+zjets.GetBinContent(3)+ttbar.GetBinContent(3)+singlet.GetBinContent(3)+smhgg.GetBinContent(3)+smhvbf.GetBinContent(3))
        print "lfv higgs: " + str(gghmutau125.GetBinContent(3)+vbfhmutau125.GetBinContent(3))
        print "data: " + str(data.GetBinContent(3))
if (widthOfBin == 15):
        print "Signal Region Yields 0 or 1:"
        print "misidentified leptons: " +str(wjets.Integral(7,10))
        print "Z->TauTau: " + str(ztautau.Integral(7,10))
        print "ZZ, WW: " + str(diboson.Integral(7,10))
        print "Wgamma: " + str(wg.Integral(7,10))
        print "Z->ll: " + str(zjets.Integral(7,10))
        print "ttbar: " + str(ttbar.Integral(7,10))
        print "t: " + str(singlet.Integral(7,10))
        print "sm higgs: " + str(smhgg.Integral(7,10)+smhvbf.Integral(7,10))
        print "sum of backgrounds: " + str(wjets.Integral(7,10)+ztautau.Integral(7,10)+diboson.Integral(7,10)+zjets.Integral(7,10)+ttbar.Integral(7,10)+singlet.Integral(7,10)+smhgg.Integral(7,10)+smhvbf.Integral(7,10)+wg.Integral(7,10))
        print "lfv higgs: " + str(gghmutau125.Integral(7,10)+vbfhmutau125.Integral(7,10))
        print "data: " + str(data.Integral(7,10))
if (widthOfBin == 20):
        print "Signal Region Yields 0 or 1:"
        print "misidentified leptons: " +str(wjets.Integral(6,8))
        print "Z->TauTau: " + str(ztautau.Integral(6,8))
        print "ZZ, WW: " + str(diboson.Integral(6,8))
        print "Wgamma: -"
        print "Z->ll: " + str(zjets.Integral(6,8))
        print "ttbar: " + str(ttbar.Integral(6,8))
        print "t: " + str(singlet.Integral(6,8))
        print "sm higgs: " + str(smhgg.Integral(6,8)+smhvbf.Integral(6,8))
        print "sum of backgrounds: " + str(wjets.Integral(6,8)+ztautau.Integral(6,8)+diboson.Integral(6,8)+zjets.Integral(6,8)+ttbar.Integral(6,8)+singlet.Integral(6,8)+smhgg.Integral(6,8)+smhvbf.Integral(6,8))
        print "lfv higgs: " + str(gghmutau125.Integral(6,8)+vbfhmutau125.Integral(6,8))
        print "data: " + str(data.Integral(6,8))
