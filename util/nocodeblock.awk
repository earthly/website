#!/usr/bin/env -S gawk -f

## Delete code blocks
## Useful for sending to Grammarly, but make sure you save
/```/{ 
    if(open==0){
        open=1
    } else {
        ending=1
        open=0
    }
}
/~~~/{ 
    if(open==0){
        open=1
    } else {
        ending=1
        open=0
    }
}
{
    if(open==0 && ending==0){ 
        print $0
    }
    ending=0
}

