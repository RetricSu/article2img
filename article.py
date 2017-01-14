#	encoding: utf-8

import os
import sys
import StringIO
import pygame
import time
from PIL import Image, ImageFont, ImageDraw

def getmidpos(x,y,str,m,n):
	return (x/2-len(str)*m/2,y/2+n)

pygame.init()

 
BackgroundColor = (245,245,245)
BackgroundColor2 = (225,225,225)
TextColor = (105,105,105)
SignColor = (211,211,211)
TheFont = '/Library/Fonts/NotoSansHans-Regular.otf'
TextSize = 25

storyfile = open("story.txt")
Width = 500
Height = 35*(len(storyfile.read())/20)+50+90



def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

def is_number(uchar):
        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False

def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                return True
        else:
                return False

def is_other(uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
                return True
        else:
                return False

def B2Q(uchar):
        """半角转全角"""
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
                return uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code=0x3000
        else:
                inside_code+=0xfee0
        return unichr(inside_code)

def Q2B(uchar):
        """全角转半角"""
        inside_code=ord(uchar)
        if inside_code==0x3000:
                inside_code=0x0020
        else:
                inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                return uchar
        return unichr(inside_code)


def stringQ2B(ustring):
        """把字符串全角转半角"""
        return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
        """格式化字符串，完成全角转半角，大写转小写的工作"""
        return stringQ2B(ustring).lower()

def string2List(ustring):
        """将ustring按照中文，字母，数字分开"""
        retList=[]
        utmp=[]
        for uchar in ustring:
                if is_other(uchar):
                        if len(utmp)==0:
                                continue
                        else:
                                retList.append("".join(utmp))
                                utmp=[]
                else:
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append("".join(utmp))
        return retList



Margin = 50            #边距

list = [u'？',u'。',u'，',u'！',u'：',u'"',u'～',u'.',u',',u'；',u'”',u'、']   #标点符号

sum = 0



def AutoWordWrap ( text1 , str):
	# 自动换行
	
	if len(text1)<20:
		sum = 1
	elif len(text1)%20 == 0 :
		sum = int(len(text1)/20)
	elif len(text1)%20 != 0:
		sum = int(len(text1)/20)+1
		
	#print sum
	
	for n  in range(0,sum):
		#print n
		str.append(text1[n * 20 :n * 20 + 20])
		
	#自动把句首标点放在上一句的末尾
	'''
	for n  in range(0,sum):
	
		if n == sum :

				
			if  str[n][0] in list :
				#print "n=sum"
				#print str[n-1]
				str[n-1] = str[n-1][0:20]+str[n][0]
				str[n] = str[n][1:20]
				#print str[n-1]

		else :
			#print (sum,n)
			#print str[n]
			if  str[n+1][0] in list :
				str[n]=str[n]+str[n+1][0]
				str[n+1] = str[n+1][1:20]
				#print ("n!=sum", str[n])
				for i in range(n+1,sum+1):
					print (i,sum)
					if i == sum:
						#print i
						str[i] = str[i][1:len(str[i])]
					elif i == n+1:
						str[i] = str[i]+str[i+1][0]
					
					else : 
						
						str[i] = str[i][1:20]+str[i+1][0]
						#print i
	'''			
	#判断有没有字母或者英文字符，调整每行的总数字
	for i in range(0,sum):
		needtofill = 0
		for j in range(0,len(str[i])):
			if is_number(str[i][j]) :
				needtofill = needtofill+1
		if needtofill/2 == 0:
			pass
		else:
			str[i]=str[i]+str[i+1][0:needtofill/2]
			#print str[i]
			for k in range(i+1,sum+1):
				#print (sum,k)
				if k == sum:
					str[k]=str[k][needtofill/2:20]
					#print (str[k],k)
					if str[k]== u'':
						sum = sum-1
						#print sum
				else:
					str[k] = str[k][needtofill/2:20]+str[k+1][0:needtofill/2]

	#自动把句首标点放在上一句的末尾
	#print len(str)
	for n  in range(0,sum):
		#print (n,sum)
		#print str[n]
		if n == sum:

				
			if  str[n][0] in list :
				#print "n=sum"
				#print str[n-1]
				str[n-1] = str[n-1][0:len(str[n-1])]+str[n][0]
				str[n] = str[n][1:len(str[n])]
				#print str[n-1]

		else :
			#print (sum,n)
			#print n+1
			if  str[n+1][0] in list :
				str[n]=str[n]+str[n+1][0]
				str[n+1] = str[n+1][1:len(str[n+1])]
				#print ("n!=sum", str[n])
				for i in range(n+1,sum+1):
					if i == sum:
						#print i
						str[i] = str[i][1:len(str[i])]
					elif i == n+1:
						str[i] = str[i]+str[i+1][0]
					
					else : 
						
						str[i] = str[i][1:len(str[i])]+str[i+1][0]
						#print i
				

def AutoRender (title) :

	
	title = unicode(title, "utf-8")
	page = 0
	im = Image.new("RGB",(Width, Height),BackgroundColor)  #text image

	
	lnumber = 2
	storyfile = open("story.txt",'r')
	lastline = storyfile.readlines()
	lastline = lastline[-1]
	#print lastline
	storyfile.close()

	
	storyfile = open("story.txt",'r')
	
	if page == 0 : 
		
		font = pygame.font.Font(TheFont,25)
		
		#font.set_bold(1)
		rtext = font.render(title,True,TextColor, BackgroundColor)
		sio = StringIO.StringIO()
		pygame.image.save(rtext,sio)
		sio.seek(0)
		line1 = Image.open(sio)
		
		im.paste(line1,getmidpos(Width,2*(35*(lnumber)+50),title,25,0))
		
		
		lnumber = 5
	
		
	for line in storyfile.readlines():
	
		arr=[1000]
		arr[0] = ''
		
		linetext = unicode(line, "utf-8")
		
		AutoWordWrap(linetext,arr)
			
		
		if len(linetext)<20:
			sum = 1
		elif len(linetext)%20 == 0 :
			sum = int(len(linetext)/20)
		elif len(linetext)%20 != 0:
			sum = int(len(linetext)/20)+1
	
		for n  in range(0,sum):
			
			
			font = pygame.font.Font(TheFont,20)
			rtext = font.render(arr[n+1], True, TextColor, BackgroundColor)
			sio = StringIO.StringIO()
			pygame.image.save(rtext, sio)
			sio.seek(0)
			line1 = Image.open(sio)
			im.paste(line1, (Margin, 35*(lnumber)+50))
			#每次渲染一行文字，并载入到图片中  FZLuXTJF_V1.10   STHeiti Medium.ttc
			lnumber = lnumber + 1	
		
			if lnumber > 21:
				page = page + 1
				#lnumber = 1
				
			if line == lastline and arr[n+1]==arr[-1] : 
				print "最后一页"
				page = page +1
				im1 = Image.new("RGB",(Width, 35*(lnumber)+50+65),BackgroundColor)  #text image
				im1.paste(im,(0,0))
				im1.save(title+'.png')
	

if __name__ == '__main__' :
	t1 = raw_input("标题： ")
	#t2 = raw_input("作者： ")
	AutoRender (t1)
	
	
	



