for e in *.png ; do echo  $e ${e%png}  --psm 6 2>/dev/null ; done | head | xargs -P 8 -n 1 echo tesseract
