#!/usr/bin/python
from PIL import Image,ImageDraw,ImageFont
import re
#parameters begin here
file_2d ="ny2.png"   #blank file for 1/2 digit shields
file_3d ="ny3.png"   #blank file for 3/4 digit shields
fontLocation = ""    #directory (or blank for this one) containing the RG2014 fonts from https://github.com/sammdot/roadgeek-fonts/releases 
lock_height=480      #specify the scaled height for the images
font_scale =.75		 #specify the font size to use relative to the image
font_scale_3 = .65   #specify the font size to use relative to the image for 3 or more digit routes
font_scale_letters = .50 #specify the font size to use relative to THE REGULAR FONT SCALE if the route contains letters.  Example -- See New York's State Routes like 14A.  If 14 is printed in 48pt font, and the scale here is .50, then the A will be printed in 24pt font.
fp ="NYTEST"          #specify the prefix of the output files.  Example -- fp = "PA" and the route is "44" then the output file is "PA 44.{extension}"
fext ="PNG"       #specify the output file type/extension
offset_x = 0      #default is to center the text horizontially.  If the center should be moved within the SCALED image, specify the pixels + or -
offset_y = -12      #default is to center the text vertically.  If the center should be moved within the SCALED image, specify the pixels + or -
fcol = (51,51,51)  #RGB tuple for the text color.  A good resource for official FHWA colors' RGB equivalents is http://vidthekid.info/misc/fhwacolors.html
routelist = ["9","9A","9B","14","14A","224","414","990V"]
#The routelist in line 14 is all the shields you want to create
use2dfor3dwith1 = True   #If True, when there is a 3 digit shield, but the route contains a 1, we'll use the 2-digit font, because 1 only takes up half the width.  PennDOT does this.  For example, PA 147 will still be in the D font like PA 45, whereas PA 225 will be in the C font.
alwaysuseD = True  #Force use of D font
alwaysuseC = False  #Force use of C font
alwaysuseB = False  #Force use of B font
#parameters end here
fs=int(lock_height*font_scale)
fontD = ImageFont.truetype(fontLocation+"RG2014D.ttf",fs)
fontC = ImageFont.truetype(fontLocation+"RG2014C.ttf",fs)
fontB = ImageFont.truetype(fontLocation+"RG2014B.ttf",fs)
fontD_3 = ImageFont.truetype(fontLocation+"RG2014D.ttf",int(lock_height*font_scale_3))
fontC_3 = ImageFont.truetype(fontLocation+"RG2014C.ttf",int(lock_height*font_scale_3))
fontB_3 = ImageFont.truetype(fontLocation+"RG2014B.ttf",int(lock_height*font_scale_3))
fontD_drop = ImageFont.truetype(fontLocation+"RG2014D.ttf",int(lock_height*font_scale*font_scale_letters))
fontC_drop = ImageFont.truetype(fontLocation+"RG2014C.ttf",int(lock_height*font_scale*font_scale_letters))
fontB_drop = ImageFont.truetype(fontLocation+"RG2014B.ttf",int(lock_height*font_scale*font_scale_letters))
fontfor2d = fontD
fontfor3d = fontC
fontfor4d = fontB
fontfor2d_drop = fontD_drop
fontfor3d_drop = fontC_drop
fontfor4d_drop = fontB_drop
for rt in routelist:
	g=len(rt)
	matched=bool(re.match("[A-Z]",rt[-1:]))
	if(matched==False):
		if g < 3:
			im = Image.open(file_2d).convert('RGB')
			if (alwaysuseD == False and alwaysuseC == False):
				usefont=fontfor2d
		if g==3:
			im = Image.open(file_3d).convert('RGB')
			if (alwaysuseD == False and alwaysuseC == False and use2dfor3dwith1 == True):
				if"1" not in rt:
					usefont=fontfor3d
				else:
					usefont=fontfor2d
			if (alwaysuseD == False and alwaysuseC == False and use2dfor3dwith1 == False):
				usefont=fontfor3d
		if g==4:
			im = Image.open(file_3d).convert('RGB')
			usefont=fontfor4d
		if(alwaysuseD == True):
			if(g<3):
				usefont = fontfor2d
			else:
				usefont = fontD_3
		if(alwaysuseC == True):
			if(g<3):
				usefont = fontfor3d
			else:
				usefont = fontC_3
		fw = usefont.getsize(rt,direction=None, features=None, language=None, stroke_width=0)
		imsize = im.size
		im=im.resize((int(imsize[0]*lock_height/imsize[1]),lock_height))
		imsize = im.size
		d = ImageDraw.Draw(im)
		d.text((int(imsize[0]/2+offset_x-fw[0]/2),int(imsize[1]/2+offset_y-fw[1]/2)),rt,font=usefont,fill=fcol)
	if(matched==True):
		rtnumber=rt[:(g-1)]
		rtletter=rt[-1:]
		if g ==2:
			im = Image.open(file_2d).convert('RGB')
			if (alwaysuseD == False and alwaysuseC == False):
				usefont_number=fontfor2d
				usefont_letter=fontfor2d_drop
		if g==3:
			im = Image.open(file_3d).convert('RGB')
			if (alwaysuseD == False and alwaysuseC == False and use2dfor3dwith1 == True):
				if"1" not in rt:
					usefont_number=fontfor3d
					usefont_letter=fontfor3d_drop
				else:
					usefont_number=fontfor2d
					usefont_letter=fontfor2d_drop
			if (alwaysuseD == False and alwaysuseC == False and use2dfor3dwith1 == False):
				usefont_number=fontfor3d
				usefont_letter=fontfor3d_drop
		if g==4:
			im = Image.open(file_3d).convert('RGB')
			usefont_number=fontfor4d
			usefont_letter=fontfor4d_drop
		if(alwaysuseD == True):
			if(g<3):
				usefont_number = fontD
			else:
				usefont_number = fontD_3
			usefont_letter= fontfor2d_drop
		if(alwaysuseC == True):
			if(g<3):
				usefont_number = fontC
			else:
				usefont_number = fontC_3
			usefont_letter = fontfor3d_drop
		imsize = im.size
		im=im.resize((int(imsize[0]*lock_height/imsize[1]),lock_height))
		imsize = im.size
		d = ImageDraw.Draw(im)
		fw_n = usefont_number.getsize(rtnumber,direction=None, features=None, language=None, stroke_width=0)
		fw_l = usefont_letter.getsize(rtletter,direction=None, features=None, language=None, stroke_width=0)
		fw_spc=0
		fw_t = fw_n[0] +fw_spc+ fw_l[0]
		fsx = (int(imsize[0]/2+offset_x-fw_t/2))
		fy_letter= int(imsize[1]/2+offset_y-fw_n[1]/2) + fw_n[1] - fw_l[1]
		d.text((fsx,int(imsize[1]/2+offset_y-fw_n[1]/2)),rtnumber,font=usefont_number,fill=fcol)
		d.text((fsx+fw_spc+fw_n[0],fy_letter),rtletter,font=usefont_letter,fill=fcol)
	im.save(fp + rt +"." + fext,fext,)
	im.close()



