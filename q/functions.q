// function to print log info
out:{-1(string .z.z)," ",x}

getCandlestick:{[Sym;Exch;interval]
    t:select first sym,first exch,
        o:first price,
        h:max price,
        l:min price,
        c:last price,
        vwap:amount wavg price,
        volume:sum amount,
        buyVol:sum amount where side=`buy,
        sellVol:sum amount where side=`sell,
        num:count i,
        buyNum:count amount where side=`buy,
        sellNum:count amount where side=`sell
    by interval xbar utc_datetime.minute from trades where sym=Sym,exch=Exch;
    t};
    
getLastTrade:{[]
    select last exch,
        last sym,
        last price, 
        last amount, 
        last side
    by sym from trades
    };
    
    
getSymList:{[] (exec distinct sym from quote)};

syncmd:{[SYMBOL;EXCH]
    q:select from quotes where sym=SYMBOL,exch=EXCH;
    q:update nav:((asize*bid)+(bsize*ask))%(bsize+asize) from q;
    Sym:SYMBOL;
    old_cols:cols q;
    new_cols:{?[x in `bnum`bsize`bid`ask`asize`anum`nav;`$(string x),"_",ssr[(string y);"-";"_"];x]}[;Sym] each old_cols;
    q:new_cols xcol q;
    t:`utc_datetime xasc select from trades where sym=SYMBOL;
    tq:`utc_datetime xasc t uj q;
    tq};

jjoin:{[x;y]x uj y};
