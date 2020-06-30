# split

可以將現有以 coco format 輸出，具有每張圖片檔名和其標註資料的 json 檔，整理成方便進行機器學習模型訓練的資料形式。

## Requirement

- argparse
- copy
- datetime
- json
- numpy
- os
- pathlib
- shutil
- sys

## Usage

prepare json and image in same file path first.

    split.py [-h] [-s] [-y] [-tr TRAIN_RATIO]


## Description

#### optional
- type -s or -y to determine the final format
- type -tr to set the train ratio

#### default parameter: 
- train_ratio: 0.8

## Flow Chart

#### first run (without -s and -y)
```flow
st=>start: start
e=>end: end
op=>operation: combine json
op2=>operation: area filter
op3=>operation: split json
op4=>operation: convert to yolo
cond=>condition: -s
cond2=>condition: -y

st->op->op2->e
cond(yes, right)->op3
cond(no)->cond2
cond2(yes, right)->op4
cond2(no)->e
```

#### after first run (with combined json file)

```flow
st=>start: start
e=>end: end
op=>operation: combine json
op2=>operation: area filter
op3=>operation: split json
op4=>operation: convert to yolo
cond=>condition: -s
cond2=>condition: -y

st->cond->op3->cond2->op4->e
cond(yes, right)->op3
cond(no)->cond2
cond2(yes, right)->op4
cond2(no)->e
```
    
## Result

#### split json (-s)
![](https://i.imgur.com/v4yLePE.png)

- images in folder
- rename list 
- json 
- overview of the result

#### convert to yolo (-y)
![](https://i.imgur.com/9zIijuF.png)

- images in folder
- labels in folder
- file neme list
- overview of the result
