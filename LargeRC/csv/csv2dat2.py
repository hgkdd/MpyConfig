

if __name__ == '__main__':
    import sys
    import os, glob
    
    indir = sys.argv[1]
    magerr=0.2
    angerr=1
    
    datheader="""FUNIT: Hz
UNIT: dB\n"""


    for infname in glob.glob( os.path.join(indir, '*.csv') ):
        print infname
        outfname=infname[:-3]+'dat'
        outf=open(outfname, 'w')
        outf.write(datheader)
        lines = open(infname).readlines()
        for line in lines[3:]:
            f, db  = map(float, line.split(';')[:2])
            ml=db-magerr
            #al=ang-angerr
            mu=db+magerr
            #au=ang+angerr
            outf.write("%e %.2f %.2f %.2f\n"%(f, ml, db, mu))
        outf.close()