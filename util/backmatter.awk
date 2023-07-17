#!/usr/bin/env -S gawk -f

# Print Back Matter
$0 == "---"{ 
    start++
}
$0 != "---"{
    if (start == 2)
    {
        print $0
    }
}
