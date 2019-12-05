import os, io,time,os.path
from PIL import Image, ImageChops
from google.cloud import vision
from google.cloud.vision import types
#import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'VisionAPI.json'

Version = "v1 (05-12-19)"
print "\nMulti GVision Image -> .txt %s\n\n" %Version

##########################
'''
    Author : Shirish Saxena

    Tested with : bmp,img,jpeg,jpg,png
    
'''
##########################
Files_Converted = 0


def Con_GVision(IMAGE_FILE):
        (abso_filen,ext_file) = os.path.splitext(IMAGE_FILE)
        Output_Name="%s.txt" %abso_filen
        start = time.time()
        client = vision.ImageAnnotatorClient()
        FOLDER_PATH = r''
        FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

        with io.open(FILE_PATH, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)

        docText = response.full_text_annotation.text
        with io.open(Output_Name, 'w', encoding='utf8') as file: #Writes to the File with UTF8 Enco
                file.write(docText)
        #print(docText)
        print "%s --> %s | %.1f sec" %(IMAGE_FILE,Output_Name,(time.time() - start)) #Print status with time taken
        return 1



def Trimm(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
def Trimm_Convert(filename_jpg):
    (abso_filen,ext_file) = os.path.splitext(filename_jpg)
    im = Image.open(filename_jpg)
    im = Trimm(im)
    im.save("%s_trim%s" %(abso_filen,ext_file))
    Con_GVision("%s_trim%s" %(abso_filen,ext_file))
    #im.show()
    return 1

print ("\n")

Root_Dir = os.getcwd() #Get Cur Dir

Get_Total_Image = len([name for name in os.listdir('.') if os.path.isfile(name) if name.endswith(('.bmp','.img','.jpe','.jpeg','.jpg','.png'))])

if Get_Total_Image == 0:
    print "\n\nTotal Image : 0\n"
    raw_input("Press Any key to exit : ")
else:
    print "\n\nTotal Images found : %d\n" %Get_Total_Image
    Trimm_C = raw_input("Do you want to trim the borders before conv ? (y/n) : ")
    Res = raw_input("\nStart converting ? (y/n) : ")
    if Res == 'y':
        start = time.time()
        for dirName, subdirList, fileList in os.walk(unicode(Root_Dir)):
                T_Tree_size = 0
                for fname in fileList:
                    if fname.endswith(('.bmp', '.gif','.img','.jpe','.jpeg','.jpg','.pcd','.png','.psd','.tiff','.raw','.svg','.ico')) == True:
                        # Finds Image files and call out the Con_Image
                        if Trimm_C == 'y':
                                Files_Converted += Trimm_Convert(fname)
                        else:
                                Files_Converted += Con_GVision(fname)
                        
        print "\n\nConverted -> %d | %.1f mins\n\n" %(Files_Converted,((time.time()-start)/60))
        raw_input("\nPress any key to exit : ")
        time.sleep(2)
    else:
        print "\n Exiting\n"
            



    
