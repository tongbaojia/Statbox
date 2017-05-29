import ROOT, rootlogon
import time
ROOT.gROOT.SetBatch(True)


outpath = "Plot"
outroot = ROOT.TFile.Open(outpath + "/" + "outhist.root", "recreate")

def distribution():

    ROOT.gRandom.SetSeed(0)

    f1 = ROOT.TF1("f1","gaus", -5, 5)
    f2 = ROOT.TF1("f2","expo", -5, 5)
    f1.SetParameters(1, 0, 1)
    f2.SetParameters(1, -1)

    hist_list = []
    temp_hist1 = ROOT.TH1F("test1", "1st distribution; x", 100, -5, 5)
    hist_list.append(temp_hist1)
    temp_hist2 = ROOT.TH1F("test2", "2nd distribution; y", 100, -5, 5)
    hist_list.append(temp_hist2)
    temp_2D_hist = ROOT.TH2F("test_2d", "distribution; x; y", 100, -5, 5, 100, -5, 5)
    hist_list.append(temp_2D_hist)
    

    canv = ROOT.TCanvas(temp_hist1.GetTitle(), temp_hist1.GetTitle(), 1000, 800)
    for i in range(100000):
        x = f1.GetRandom()
        y = f2.GetRandom()
        temp_hist1.Fill(x)
        temp_hist2.Fill(y)
        temp_2D_hist.Fill(x, y*x*x)
    
    temp_2D_hist.Draw("colz")
    print "mean: ", temp_hist1.GetMean(), " err: ", temp_hist1.GetMeanError()
    print "var: ", temp_hist1.GetRMS(), " err: ", temp_hist1.GetRMSError()
    print "cov: ", temp_2D_hist.GetCovariance()

    canv.SaveAs(outpath + "/" + temp_2D_hist.GetName() + ".pdf")
    outroot.cd()
    temp_hist1.Write()
    temp_hist2.Write()
    temp_2D_hist.Write()


def main():
    start_time = time.time()
    ##do the analysis
    distribution()
    ##finish
    outroot.Close()
    print("--- %s seconds ---" % (time.time() - start_time))

#def clearbranches():
if __name__ == "__main__":
    main()