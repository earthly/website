double-image() { # Double size of image. Using imagemagick
    ./util/superresolution/realesrgan-ncnn-vulkan -i "$1" -o "$1_new.png" -m "./util/superresolution/models" -s 2
    rm "$1"
    mv "$1_new.png" "$1"
}

while IFS= read -r line; do
  double-image "$line"
done < warn.txt