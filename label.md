# label

可以快速視覺化圖片的標註資料 ，並且決定是否加上 bounding box、多邊形或是標註類別三種資訊。

## Requirement

- argpars
- json
- os
- pillow
- shutil

## Usage

    label.py [-h] [-f FILE_NAME] [-r] [-p] [-t] [-font FONT]
    
## Description

#### essential
- type -f to set the file name
- type -font to set file path of font, ex: "/System/Library/Fonts/Supplemental/Arial.ttf"

#### optional
- type -r to draw rectangle
- type -p to draw polygon
- type -t to add annotation id on rectangle




## Result

#### rectangle (-r)
![](https://i.imgur.com/LHir2uE.jpg)

#### polygon (-p)
![](https://i.imgur.com/tTwomed.jpg)

#### text (-t)
![](https://i.imgur.com/YLjPwq8.jpg)

#### all (-r, -p, -t)
![](https://i.imgur.com/BwoxtAk.jpg)
