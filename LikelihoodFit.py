# Tony Tong; baojia.tong@cern.ch
import os, argparse, sys, math, time
#import config as CONF
from array import array
import ROOT as ROOT
#import helpers
import rootlogon
#for parallel processing!
import multiprocessing as mp
#other setups
ROOT.gROOT.LoadMacro("AtlasStyle.C") 
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()
ROOT.TH1.AddDirectory(False)
ROOT.gROOT.SetBatch(True)

def options():
    '''pass on options'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotpath",  default="Plot")
    return parser.parse_args()

def checkpath(outputpath):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

def GenEvent(n=20, par=[2]):
    '''generate random events, n is the length, 
        par is the parameter for the functional form'''
    result = []
    rand_gen = ROOT.TRandom3(0)
    for i in range(n):
        result.append(rand_gen.Exp(par[0]))
    return result

def PlotEvent(result=[]):
    '''generate a 1D plot, fill it by the arrys and return the histogram'''
    hist = ROOT.TH1D("h1","Generated Exponential data", 10, 0, 5*2)
    for i in result:
        hist.Fill(i)
    return hist

# Main
def main():
    '''main program'''
    #start time
    start_time = time.time()
    global ops
    ops = options()
    #setup basics
    events = GenEvent()
    
    #print events
    canv = ROOT.TCanvas("tempcanv", " ", 800, 800)
    canv.cd()
    events_hist =  PlotEvent(events)
    events_hist.Draw()
    checkpath("Plot")
    canv.SaveAs(ops.plotpath + "/" + "events.pdf")
    print("--- %s seconds ---" % (time.time() - start_time))



#####################################
if __name__ == '__main__':
    main()