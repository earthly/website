#!/usr/bin/env -S gawk -f

/```/{ 
    processed[NR]=1
    if(open==0){
        open=1
    } else {
        open=0
    }
}
/~~~/{ 
    processed[NR]=1
    if(open==0){
        open=1
    } else {
        open=0
    }
}
{
    if(open==0){ 
        print $0
    }
}

