#!/usr/bin/env -S gawk -f

# Print functions, but only following "External"
BEGIN { 
    printf "function        \t description\n"
    printf "----------------\t -----------------------------------------------------------------\n"
}
$2 == "External" { external=1 }
$1 ~/\(\)/{ 
    if (external==1){
        if(index($0,"#"))
            printf "%-20s \t %-60s\n",$1, substr($0, index($0,"#")+1)
        else 
            print $1 
    }
}
END {
    printf "-----------------------------------------------------------------------------------------\n"
}
