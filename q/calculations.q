getCandlestick:{[Sym;Exch;interval]
    t:select first sym,first exch,
        num:count i,
        volume:sum amount,
        o:first price,
        h:max price,
        l:min price,
        c:last price,
        vwap:amount wavg price,
        buyVol: sum amount where side=`buy,
        sellVol: sum amount where side=`sell,
        buyNum: count amount where side=`buy,
        sellNum: count amount where side=`sell
    by interval xbar utc_datetime.minute from trades where sym=Sym,exch=Exch;
    t};
