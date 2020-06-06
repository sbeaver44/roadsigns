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
fp ="NYS"          #specify the prefix of the output files.  Example -- fp = "PA" and the route is "44" then the output file is "PA 44.{extension}"
fext ="PNG"       #specify the output file type/extension
offset_x = 0      #default is to center the text horizontially.  If the center should be moved within the SCALED image, specify the pixels + or -
offset_y = -12      #default is to center the text vertically.  If the center should be moved within the SCALED image, specify the pixels + or -
fcol = (51,51,51)  #RGB tuple for the text color.  A good resource for official FHWA colors' RGB equivalents is http://vidthekid.info/misc/fhwacolors.html
routelist = ["10","100","100A","100B","100C","101","102","103","104","104A","104B","105","106","107","108","109","10A","110","111","112","113","114","115","116","117","118","119","11A","11B","11C","12","120","120A","121","122","123","124","125","126","127","128","129","12A","12B","12D","12E","12F","13","130","131","132","133","134","135","136","137","138","139","13A","14","140","141","142","143","144","145","146","146A","147","148","149","14A","15","150","151","153","155","156","157","157A","158","159","15A","16","160","161","162","163","164","165","166","167","168","169","17","170","170A","171","172","173","174","175","176","177","178","179","17A","17B","17C","17K","17M","18","180","182","183","184","185","186","187","189","18F","19","190","193","196","197","198","199","19A","2","200","201","203","204","205","206","207","208","21","210","211","212","213","214","215","216","217","218","22","220","221","222","223","224","225","226","227","228","22A","22B","23","230","231","232","233","235","236","237","238","23A","23B","24","240","241","242","243","244","245","246","247","248","248A","249","25","250","251","252","253","254","256","257","258","259","25A","25B","26","260","261","262","263","264","265","266","268","269","27","270","271","272","274","275","276","277","278","279","27A","28","280","281","282","283","284","286","289","28A","28N","29","290","291","292","293","294","295","296","297","298","299","29A","3","30","300","301","302","303","304","305","306","308","309","30A","31","310","311","312","313","314","315","316","317","318","31A","31E","31F","32","320","321","322","324","325","326","327","328","329","32A","33","331","332","334","335","336","337","33A","34","340","342","343","344","345","346","347","349","34B","35","350","351","352","353","354","355","357","359","36","362","363","364","365","365A","366","367","369","37","370","371","372","373","374","375","376","377","378","37B","37C","38","383","384","385","386","387","38A","38B","39","390","391","392","394","395","396","397","3A","40","400","403","404","406","408","409","41","410","411","412","414","415","416","417","418","419","41A","42","420","421","423","425","426","427","429","43","430","431","433","434","436","437","438","440","441","442","443","444","446","448","45","454","458","46","470","474","48","481","488","49","495","5","50","51","52","52A","53","531","54","54A","55","55A","56","58","59","590","598","5A","5B","5S","60","61","63","631","635","64","65","66","67","68","69","690","695","69A","6N","7","70","71","72","73","74","747","75","76","77","78","787","79","7A","7B","8","80","81","812","82","825","83","840","85","85A","86","878","88","89","890","895","90","91","92","93","94","95","96","961F","962J","96A","96B","97","98","990L","990V","9A","9B","9D","9G","9H","9J","9L","9N","9P","9R"]
#The routelist in line 17 is all the shields you want to create
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



