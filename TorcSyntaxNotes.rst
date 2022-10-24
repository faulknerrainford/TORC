##################
Torc Syntax Notes
##################

Possible syntax for the first circuit:

Circuit(ori, amp){
    Gene(tetA),
    <<
    Promoter(leu500),
    Florescence(rasberry),
    <<
    Bridge(lac){
        Promoter(leu500, inv),
        Florescence(merlak),
    }
}

Giving alternative expression as:

Circuit(ori, amp){
    Bridge(lac){
        Promoter(leu500, inv),
        Florescence(merlak),
    }
    >>
    Promoter(leu500),
    Florescence(rasberry),
    >>
    Gene(tetA),
}

Which wrong as it would give gene->ori->amp rather than ori->amp<-gene with in the template.
Neeed to regular expressions position relative to ori and amp. (Talk to alap and victor about this to find out
restrictions, may need an expressed but overridable default rather than a fixed relative position.)
