### Note
## 2021.12.23 / jongkwan.Park - Added code which is removing tag in json file name such as '_label' or '_maks'.
## Suakit 2.3 의 segmentation tutorial's image data를 export 하고 VPDL 2.1 import image/label/mask 를 위한 renaming existied images 주요 목적은 'Import Label' test case를 만들기 위한 external tool images data 만들기
## Directory of input/output on DeskTop-PC: D:\_1_QA_VPDL\__Suakit_Tutorial_Export_Images
### python - using path control  - https://ddolcat.tistory.com/654

import os
import cv2
import re
import math
import numpy as np
from glob import glob
from PIL import Image
from shutil import copyfile

### To use image file name which include Korean language - Used the special defined functions which found imreadKOR() and imWriteKOR() by googling.
### Cause : Python's OpenCV can not processing uni-code like Koearan.
### Solution : As you know from attached Website below, using 'imencode()', you can easily solve issue.
### When you used both method of OpenCV on Python - imread() & imwrite(), It was issue that is 한글(유니코드) - 출처: https://jangjy.tistory.com/337
#def imreadKOR(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8): 
def imreadKOR(filename, flags, dtype): 
    # 사용 예시 : def imreadKOR(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try: 
        n = np.fromfile(filename, dtype) 
        img = cv2.imdecode(n, flags) 
        return img 
    except Exception as e: print(e) 
    return None

def imwriteKOR(filename, img, params=None): 
    try: 
        ext = os.path.splitext(filename)[1] 
        result, n = cv2.imencode(ext, img, params) 
        
        if result: 
            with open(filename, mode='w+b') as f: 
                n.tofile(f)
            return True 
        else: 
            return False 
    except Exception as e: print(e)
    return False
#
# any tip : https://www.programcreek.com/python/example/70396/cv2.imencode    
##########################################################################################


### Note: The orginal images have to be 3 channel in this code below.
def ConvertImagesOneChannel(path_images, path_output):    
    allImages = glob(path_images)
    outputPath = path_output
    originImages = []   
    ImageNames = []
    
    for index, path in enumerate(allImages):  
        ### Option 1 - Note : You can use this code in case of a file name was only English.
        # sourceImage = cv2.imread(path, cv2.IMREAD_GRAYSCALE) ## Even if loaded image was 3-channel or 4-channel, sourceImage will become 1-channel.
        # originImages.append(sourceImage)       
        # ImageNames.append(os.path.basename(path))

        ### Option 2 - Note : You must use this method which is 'imreadKOR()' in case of including Korean language in loaded file name or path. Because OpenCV in Python was issue which use unicode.
        sourceImage = imreadKOR(path, cv2.IMREAD_GRAYSCALE, np.uint8)
        originImages.append(sourceImage)       
        ImageNames.append(os.path.basename(path))

    for index, image in enumerate(originImages):                 
        ### Option 1 - Note : You can use this code in case of a file name was only English.
        #pathNewName = outputPath +'\\'+ ImageNames[index]
        #cv2.imwrite(pathNewName, image)

        ### Option 2 - Note : You must use this method that is 'imwriteKOR()' in case of including Korean language in loaded file name or path.
        pathNewName = outputPath +'\\'+ ImageNames[index]
        imwriteKOR(pathNewName, image)


### Note: Both label images and mask images have to be 1 channel in this code below.
### If loaded images were 3 channel, You have to be converted these images format by using cv2.cvtColor().
### To use cvtColor(), refer to website which is 'https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html'
def RemovedTagImage(path_images, path_output, removeTagName):
    allImages = glob(path_images)
    outputPath = path_output
    
    originImages = []
    newImageNames = []
    existedImageNames = []

    for index, path in enumerate(allImages):       
        src = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        #originImages.append(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY, cv2.CV_32F))
        originImages.append(src)       
        existedImageNames = os.path.basename(path)        
        strBuffer = existedImageNames
        # if strBuffer.find('_label'):        
        #     strBuffer = re.sub('_label', '', existedImageNames) 

        if strBuffer.find(removeTagName):        
            strBuffer = re.sub(removeTagName, '', existedImageNames) 

        modifiedName = strBuffer
        newImageNames.append(modifiedName)

    for index, image in enumerate(originImages):
        pathNewName = outputPath +'\\'+ newImageNames[index]    
        cv2.imwrite(pathNewName, image)



### Note : Remove tag that is '_label' or '_mask' of the existed Json-file name.
def RemovedTagJson(path_inJsonFiles, path_outJsonFiles, removeJsonTag):

    allJF = glob(path_inJsonFiles)      ## 입력 경로에 있는 *.jong 
    outputJsonFolder = path_outJsonFiles    ## 출력 경로    

    newJFNames = []

    ## remove tag '_label' or '_mask'
    for index, path in enumerate(allJF):       
        existedJFName = os.path.basename(path)  # aaa_label.json
        strBuffer = existedJFName       # aaa_label.json
        if strBuffer.find(removeJsonTag):        # search '_label'
            strBuffer = re.sub(removeJsonTag, '', existedJFName)  # aaa.json
        modifiedName = strBuffer        
        newJFNames.append(modifiedName) # newJFNames's array add rename.

    ## copy file
    for index, path in enumerate(allJF):
        pathNewNameJson = outputJsonFolder +'\\'+ newJFNames[index]    
        copyfile(path, pathNewNameJson)

### Actural running code after enter each folder directory
#        
print("Start program\n")
curpath = os.getcwd() ## 현재 경로 확인 https://ddolcat.tistory.com/654

PathImagesMultiCh = os.path.join(curpath,"0_Input_PNG_Convert_3chto1ch")
PathLabelImages = os.path.join(curpath,"1_Input_PNG_Remove_Label")
PathLabelJson = os.path.join(curpath,"3_Input_JSON_Remove_Label")
PathMaskImages = os.path.join(curpath,"2_Input_PNG_Remove_Mask")
PathMaskJson = os.path.join(curpath,"4_Input_JSON_Remove_Mask")

#PathImagesMultiCh = 'C:\\_1_Remove_keyword_in_filename\\0_Input_PNG3ch'
OutputPathImagesMultiCh = os.path.join(PathImagesMultiCh, "ConvertChannel")
os.makedirs(OutputPathImagesMultiCh, exist_ok=True)
InputPathImagesMultiCh = os.path.join(PathImagesMultiCh, "*.png")
ConvertImagesOneChannel(InputPathImagesMultiCh, OutputPathImagesMultiCh)

#PathLabelImages = 'C:\\_1_Remove_keyword_in_filename\\1_Input_PNG'
OutputPathLabelImages = os.path.join(PathLabelImages, "Remove_Label_PNG")
os.makedirs(OutputPathLabelImages, exist_ok=True)
InputPathLabelImages = os.path.join(PathLabelImages, "*.png")
RemovedTagImage(InputPathLabelImages, OutputPathLabelImages, '_label')

OutputPathMaskImages = os.path.join(PathMaskImages, "Remove_Mask_PNG")
os.makedirs(OutputPathMaskImages, exist_ok=True)
InputPathMaskImages = os.path.join(PathMaskImages, "*.png")
RemovedTagImage(InputPathMaskImages, OutputPathMaskImages, '_mask')

#PathLabelJson = 'C:\\_1_Remove_keyword_in_filename\\2_Input_JSON'
OutputPathLabelJson = os.path.join(PathLabelJson, "Remove_Label_JSON")
os.makedirs(OutputPathLabelJson, exist_ok=True)
InputPathLabelJson = os.path.join(PathLabelJson, "*.json")
RemovedTagJson(InputPathLabelJson, OutputPathLabelJson, '_label')

OutputPathMaskJson = os.path.join(PathMaskJson, "Remove_Mask_JSON")
os.makedirs(OutputPathMaskJson, exist_ok=True)
InputPathMaskJson = os.path.join(PathMaskJson, "*.json")
RemovedTagJson(InputPathMaskJson, OutputPathMaskJson, '_mask')

print("Completion of processing!\n")


# PathImagesMultiCh = 'C:\\_1_Remove_keyword_in_filename\\0_Input_PNG3ch'
# OutputPathImagesMultiCh = os.path.join(PathImagesMultiCh, "Convert")
# os.makedirs(OutputPathImagesMultiCh, exist_ok=True)
# InputPathImagesMultiCh = os.path.join(PathImagesMultiCh, "*.png")
# ConvertImagesOneChannel(InputPathImagesMultiCh, OutputPathImagesMultiCh)

# PathLabelImages = 'C:\\_1_Remove_keyword_in_filename\\1_Input_PNG'
# OutputPathLabelImages = os.path.join(PathLabelImages, "RemoveLabelImage")
# os.makedirs(OutputPathLabelImages, exist_ok=True)
# InputPathLabelImages = os.path.join(PathLabelImages, "*.png")
# RemovedTagImage(InputPathLabelImages, OutputPathLabelImages, '_label')

# PathLabelJson = 'C:\\_1_Remove_keyword_in_filename\\2_Input_JSON'
# OutputPathLabelJson = os.path.join(PathLabelJson, "RemoveLabelJSON")
# os.makedirs(OutputPathLabelJson, exist_ok=True)
# InputPathLabelJson = os.path.join(PathLabelJson, "*.json")
# RemovedTagJson(InputPathLabelJson, OutputPathLabelJson, '_label')


# inpathJson = 'C:\\_1_Remove_keyword_in_filename\\2_Input_JSON\\*.json'
# outpathJson = 'C:\\_1_Remove_keyword_in_filename\\2_Input_JSON'
# RemovedTagJson(inpathJson, outpathJson, '_label')

# # ### Tip
# curpath = os.getcwd() ## 현재 경로 확인 https://ddolcat.tistory.com/654
# print(curpath)
# dncurpath = os.chdir("../") ## 현재 경로 -> 한단계 내려가기 확인 
# checkpath = os.getcwd()
# print(checkpath)






#################################################################################################
### Hard coding test before making function which the name is 'RemoveTag'.

# pathSuaKIT_Label_Train_Labeled_Images = glob(SuaKIT_Label_Train_Labeled)
# pathSuaKIT_Label_Train_Labeled_output = pathSuaKIT_Label_Train_Labeled
# # sourceImages2 = glob(SuaKIT_Label_Train_Unlabeled)
# # outputIamges2 = pathSuaKIT_Label_Train_Unlabeled

# ## Making Buffer
# originImages_Labeled = []
# imageFileNames_Labeled = []
# filesname_Labeled = []

# for index, path in enumerate(pathSuaKIT_Label_Train_Labeled_Images):       
#     src_Labeled = cv2.imread(path, cv2.IMREAD_GRAYSCALE)#CVReadImage(path)
#     #dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY, cv2.CV_32F)            
#     #originImages.append(dst)       
#     originImages_Labeled.append(src_Labeled)       
#     filesname_Labeled = os.path.basename(path)
    
#     strfileName_Labeled = filesname_Labeled # Save the split file name of path to a variable for testing.
#     if strfileName_Labeled.find('_label'):        
#         strfileName_Labeled = re.sub('_label', '', strfileName_Labeled) # Ourput : Just only remove '_label'           
#     filesname_Labeled = strfileName_Labeled
#     imageFileNames_Labeled.append(filesname_Labeled)

# for index, image in enumerate(originImages_Labeled):    
#     resultPath_Labeled = pathSuaKIT_Label_Train_Labeled_output +'\\'+ imageFileNames_Labeled[index]    
#     cv2.imwrite(resultPath_Labeled, image)


# pathSuaKIT_Label_Train_Unlabeled_Images = glob(SuaKIT_Label_Train_Unlabeled)
# pathSuaKIT_Label_Train_Unlabeled_output = pathSuaKIT_Label_Train_Unlabeled

# originImages_Unlabeled = []
# imageFileNames_Unlabeled = []
# filesname_Unlabeled = []

# for index, path in enumerate(pathSuaKIT_Label_Train_Unlabeled_Images):       
#     src_Unlabeled = cv2.imread(path, cv2.IMREAD_GRAYSCALE)#CVReadImage(path)
#     #dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY, cv2.CV_32F)            
#     #originImages.append(dst)       
#     originImages_Unlabeled.append(src_Unlabeled)       
#     filesname_Unlabeled = os.path.basename(path)
    
#     strfileName_Unlabeled = filesname_Unlabeled # Save the split file name of path to a variable for testing.
#     if strfileName_Unlabeled.find('_label'):        
#         strfileName_Unlabeled = re.sub('_label', '', strfileName_Unlabeled) # Ourput : Just only remove '_label'           
#     filesname_Unlabeled = strfileName_Unlabeled
#     imageFileNames_Unlabeled.append(filesname_Unlabeled)

# for index, image in enumerate(originImages_Unlabeled):
#     resultPath_Unlabeled = pathSuaKIT_Label_Train_Unlabeled_output +'\\'+ imageFileNames_Unlabeled[index]    
#     cv2.imwrite(resultPath_Unlabeled, image)


###########################################################################################################
### JK'test - 2021.11.18 - Need to modify this under code because it has a little issue or error.
# if os.path.isdir(pathSuaKIT) == 0:
#     print('JK Alram: Have done checking output-folder, Need to delete output-folder which is Rename_SuaKit_DataSet')
# else:
#     os.mkdir(pathSuaKIT)

# ## refer to : https://info-lab.tistory.com/303 ## if else 한줄로 만들기
# checkingDirectory = os.path.isdir(pathSuaKIT)
# print('checking output-folder whether it is or not : ', checkingDirectory)

# if checkingDirectory == True:
#     print('Being output-folder')
#     os.mkdir(pathSuaKIT_Image)
#     os.mkdir(pathSuaKIT_Image_Train)
#     os.mkdir(pathSuaKIT_Image_Train_Labeled)
#     os.mkdir(pathSuaKIT_Image_Train_Unlabeled)
#     os.mkdir(pathSuaKIT_Label)
#     os.mkdir(pathSuaKIT_Label_Train)
#     os.mkdir(pathSuaKIT_Label_Train_Labeled)
#     os.mkdir(pathSuaKIT_Label_Train_Unlabeled)    
#     os.mkdir(pathSuaKIT_Mask)
#     os.mkdir(pathSuaKIT_Mask_Train)
#     os.mkdir(pathSuaKIT_Mask_Train_Masked)
#     os.mkdir(pathSuaKIT_Mask_Train_NotMasked)
# else:
#     print('Made output-folder because of nothing directory.')    
#     os.mkdir(pathSuaKIT) 
#     os.mkdir(pathSuaKIT_Image)
#     os.mkdir(pathSuaKIT_Image_Train)
#     os.mkdir(pathSuaKIT_Image_Train_Labeled)
#     os.mkdir(pathSuaKIT_Image_Train_Unlabeled)
#     os.mkdir(pathSuaKIT_Label)
#     os.mkdir(pathSuaKIT_Label_Train)
#     os.mkdir(pathSuaKIT_Label_Train_Labeled)
#     os.mkdir(pathSuaKIT_Label_Train_Unlabeled)    
#     os.mkdir(pathSuaKIT_Mask)
#     os.mkdir(pathSuaKIT_Mask_Train)
#     os.mkdir(pathSuaKIT_Mask_Train_Masked)
#     os.mkdir(pathSuaKIT_Mask_Train_NotMasked)