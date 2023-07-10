#!/usr/bin/env -S gawk -f

# Print Front Matter
$0 == "---"{ 
    start++
    print $0
}
$0 != "---"{
    if (start == 1)
    {
        print $0
    }
}
