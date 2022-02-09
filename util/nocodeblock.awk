#!/usr/bin/env -S gawk -f

## Delete code blocks
## Useful for sending to Grammarly, but make sure you save


# sline = skip line
# sblokc = skip block
/```/{ 
    if(sblock==0){
        sblock=1
    } else {
        sline=1
        sblock=0
    }
}
/~~~/{ 
    if(sblock==0){
        sblock=1
    } else {
        sline=1
        sblock=0
    }
}
/<div/{ 
        sline=1
}
{
    if(sblock==0 && sline==0){ 
        print $0
    }
    # 
    sline=0
}

