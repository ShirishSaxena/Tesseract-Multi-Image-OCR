import pytesseract
from PIL import Image, ImageChops
import os,os.path
import io
import time

Version = "v1.4 (05-12-19)"
print "\nMulti Tesseract Image -> .txt %s\n\n" %Version

##########################
'''
    Author : Shirish Saxena

    Tested with : bmp,img,jpeg,jpg,png
    
'''
##########################

pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Sets the Tesseract Dir

Files_Converted = 0
Lang_Tess = "eng" #Set Language to use when converting

# Function that converts jpg/ or any image file to .txt format
def Con_Image(filename_jpg):
    global Lang_Tess
    (abso_filen,ext_file) = os.path.splitext(filename_jpg) #Split FileName and Extension
    Output_Name="%s.txt" %abso_filen
    start = time.time()
    Save_Data=(pytesseract.image_to_string(Image.open(filename_jpg),lang=Lang_Tess))  #JPG conv starts here
    with io.open(Output_Name, 'w', encoding='utf8') as file: #Writes to the File with UTF8 Enco
        file.write(Save_Data)
    print "%s --> %s | %.1f sec" %(filename_jpg,Output_Name,(time.time() - start)) #Print status with time taken
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
    im.save("%s_trim.%s" %(abso_filen,ext_file))
    Con_Image("%s_trim.%s" %(abso_filen,ext_file))
    #im.show()
    return 1
    
    

    
Root_Dir = os.getcwd() #Get Cur Dir

Get_Total_Image = len([name for name in os.listdir('.') if os.path.isfile(name) if name.endswith(('.bmp','.img','.jpe','.jpeg','.jpg','.png'))])

if Get_Total_Image == 0:
    print "\n\nTotal Image : 0\n"
    raw_input("Press Any key to exit : ")
else:
    print "\n\nTotal Images found : %d\n" %Get_Total_Image
    Trimm_Check = raw_input("Do you want to trim the borders before conv ? (y/n) : ")
    Res = raw_input("\nStart converting ? (y/n) : ")
    print "\n"
    if Res == 'y':
        start = time.time()
        for dirName, subdirList, fileList in os.walk(unicode(Root_Dir)):
                T_Tree_size = 0
                for fname in fileList:
                    if fname.endswith(('.bmp', '.gif','.img','.jpe','.jpeg','.jpg','.pcd','.png','.psd','.tiff','.raw','.svg','.ico')) == True:
                        # Finds Image files and call out the Con_Image
                        if Trimm_Check == 'y':
                            Files_Converted += Trimm_Convert(fname)
                        else:
                            Files_Converted += Con_Image(fname)
        print "\n\nConverted -> %d | %.1f sec\n\n" %(Files_Converted,(time.time()-start))
        raw_input("\nPress any key to exit : ")
        time.sleep(2)
    else:
        print "\n Exiting\n"

