#!/usr/bin/env -S gawk -f

$1 ~ /^```/{ 
    processed[NR]=1
        if($2){
            printf "~~~{.%s caption=\"\"}\n", $2
        }else{
            print "~~~"
        }
        
}
{
    if(!processed[NR]){ 
        print $0
    }
}

