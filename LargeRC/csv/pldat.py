
def read_dat(lines):
    x=[]
    y=[]
    for line in lines:
        if '[' in line:
            cols=line.split(' [')
        else:
            cols=line.split()
        try:
            f=float(cols[0])
            #print f
        except ValueError:
            continue
        Ncols=len(cols)
        #print Ncols
        if Ncols == 2:  # no error given
            c=cols[1]
        elif Ncols == 4:
            c=cols[2]
        x.append(f)
        c.strip('{}[]()')
        d=float(c.split(',')[0])
        y.append(d)
    return x,y        
        
if __name__ == "__main__":
    import sys
    import pylab as pl

    for infile in sys.argv[1:]: 
        lines=open(infile, 'r').readlines()        
        x,y=read_dat(lines)
        pl.figure(1)
        pl.semilogx(x,y, label=infile)
    pl.grid()
    pl.legend(loc='best')
    pl.show()