import ROOT, rootlogon
import time
ROOT.gROOT.SetBatch(True)


outpath = "Plot"
outroot = ROOT.TFile.Open(outpath + "/" + "outhist_ch2.root", "recreate")


def distribution():

    ROOT.gRandom.SetSeed(0)

    pdf_dic = {
        #"binomial":"ROOT::Math::binomial_pdf(x, 0.5, 180)", ##this doesn't like convolution
        #"poisson":"ROOT::Math::poisson_pdf(x, 90)", ##this doesn't like convolution
        "exponential":"ROOT::Math::exponential_pdf(x, 0.5, 90)",
        "gaussian":"ROOT::Math::normal_pdf(x, 1.25, 90)",
        "lognormal":"ROOT::Math::lognormal_pdf(x, 4.5, 0.1)",
        "breitwigner":"ROOT::Math::breitwigner_pdf(x, 2.5, 90)",
        "landau":"ROOT::Math::landau_pdf(x, 0.4, 90)",
        }

    for name, pdf in pdf_dic.iteritems():
        print name
        f1 = ROOT.TF1("f1", pdf, 60, 120)
        fconv = ROOT.TF1Convolution("f1", "gaus", 60, 120, False)
        #fconv.SetNofPointsFFT(1000);
        f2 = ROOT.TF1("f2", fconv, 60, 120, fconv.GetNpar())
        f2.SetParameters(0, 2) ##width 2 gaussian!
        #print fconv.GetNpar(), f2.GetParameters()
        #f2.SetParameters(1.,-0.3,0.,1.)
        #f1.SetParameters(1, 0, 1)
        #f2.SetParameters(1, -1)

        #hist_list = []
        temp_hist1 = ROOT.TH1F(name, name + " distribution; x; N sampled from pdf", 100, 60, 120)
        #hist_list.append(temp_hist1)
        temp_hist2 = ROOT.TH1F(name + "_conv", "conver distribution; y", 100, 60, 120)
        #hist_list.append(temp_hist2)
        #temp_2D_hist = ROOT.TH2F("test_2d", "distribution; x; y", 100, -5, 5, 100, -5, 5)
        #hist_list.append(temp_2D_hist)
        

        canv = ROOT.TCanvas(temp_hist1.GetTitle(), temp_hist1.GetTitle(), 1000, 800)
        for i in range(10000):
            x = f1.GetRandom()
            y = f2.GetRandom()
            #print x
            temp_hist1.Fill(x)
            temp_hist2.Fill(y)
            #temp_2D_hist.Fill(x, y*x*x)
        
        temp_hist1.Draw("")
        canv.SaveAs(outpath + "/Ch2_" + temp_hist1.GetName() + ".pdf")
        canv.Clear()
        temp_hist2.Draw("")
        canv.SaveAs(outpath + "/Ch2_" + temp_hist2.GetName() + ".pdf")

        # temp_2D_hist.Draw("colz")
        # print "mean: ", temp_hist1.GetMean(), " err: ", temp_hist1.GetMeanError()
        # print "var: ", temp_hist1.GetRMS(), " err: ", temp_hist1.GetRMSError()
        # print "cov: ", temp_2D_hist.GetCovariance()

        outroot.cd()
        temp_hist1.Write()
        temp_hist2.Write()
        del canv
        #temp_2D_hist.Write()


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