#!/usr/bin/env -S gawk -f

# Print functions, but only following "External"
BEGIN { 
    printf "function        \t description\n"
    printf "----------------\t -----------------------------------------------------------------\n"
}
$2 == "External" { external=1 }
$1 ~/\(\)/{ 
    if (external==1){
        f=substr($1, 0, index($1,"(")-1)
        if(index($0,"#"))
            printf "%-20s \t %-60s\n",f, substr($0, index($0,"#")+1)
        else 
            print f
    }
}
END {
    printf "-----------------------------------------------------------------------------------------\n"
}
