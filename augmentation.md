# data augmentation

將現有資料以 data augmentation 的方式增加 dataset 的數量，並且可以讓使用者設定不同 augmentation method 的參數。

## Requirement

- argpars
- data_aug
- json
- matplotlib
- numpy
- python-opencv
- Pillow
- random

## Usage

    augmentation.py [-h] [-f FILE_NAME] [-r] [-flip FLIP] [-scale SCALE]
                       [-scale_diff SCALE_DIFF] [-translate TRANSLATE]
                       [-translate_diff TRANSLATE_DIFF] [-rotate ROTATE]
                       [-shear SHEAR] [-hsv HSV HSV HSV]
    
## Description

#### essential
- type -f to set the file name

#### optional
- type **-r** to draw rectangle
- type **-flip** to set the probability that the image will be flipped
- type **-scale** to set the scale factors for x and y directions to randomly sampled from (-arg, arg)
- type **-scale_diff** to set True or False. If True, the image will scale with different values in x and y directions
- type **-translate** to set the translating factors for x and y directions to randomly sampled from (-arg, arg)
- type **-translate_diff** to set True or False. If True, the image will translate with different values in x and y directions
- type **-rotate** to set the rotating angle, in degrees, which is sampled from (-arg, arg)
- type **-shear** to set the shearing factor sampled from (-arg, arg)
- type **-hsv** to set the hue, saturation, and value factors samples form (-arg, arg)

#### default parameter: 
- flip: 0.5
- scale: 0.1, scale_diff: True
- translate: 0.1, translate_diff: True
- rotate: 3
- shear: 0.1
- hsv: 10, 10, 10


## Result

#### original image
![](https://i.imgur.com/RI3nIWR.jpg)

#### RandomHorizontalFlip (-flip)
![](https://i.imgur.com/QGTmYH0.jpg)

#### RandomScale (-scale)
![](https://i.imgur.com/JAUzX69.jpg)

#### RandomTranslate (-translate)
![](https://i.imgur.com/Med1yU5.jpg)

#### RandomRotate (-rotate)
![](https://i.imgur.com/LoNrB9y.jpg)

#### RandomShear (-shear)
![](https://i.imgur.com/ElFVgbx.jpg)

#### RandomHSV (-hsv)
![](https://i.imgur.com/iCkN9nK.jpg)
