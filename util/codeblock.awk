#!/usr/bin/env -S gawk -f

/```/{ 
    processed[NR]=1
    if(open==0){
        open=1
        printf "~~~{.bash caption=\">_\"}\n", $0
    } else {
        open=0
        printf "~~~\n", $0
    }
}
{
    if(!processed[NR]){ 
        print $0
    }
}

