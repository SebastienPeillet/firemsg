import Tkinter
from tkFileDialog import *
import Tix
import ConfigParser
import os

main_variable=['FIREMSG_PATH','ENABLE_POSTGRES','PG_DBNAME','PG_TABLENAME','PG_USER','PG_PW','FTP_host','FTP_name','FTP_pw', 'PG_HOST','ENABLE_FIRE_DETECTION','SAVE_INTERMEDIATE_FILES','PPP_CONFIG_DIR']
day_process_variable=['dateDeb','dateFin','FTP_download']
advanced_variable=['T039','T108','delta_day','delta_night','day_start','day_end','window_width','potfire_nb_limit','level_requirement']

class GrumpyConfigParser(ConfigParser.ConfigParser):
  """Virtually identical to the original method, but delimit keys and values with '=' instead of ' = '"""
  def write(self, fp):
    if self._defaults:
      fp.write("[%s]\n" % DEFAULTSECT)
      for (key, value) in self._defaults.items():
        fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
      fp.write("\n")
    for section in self._sections:
      fp.write("[%s]\n" % section)
      for (key, value) in self._sections[section].items():
        if key == "__name__":
          continue
        if (value is not None) or (self._optcre == self.OPTCRE):

          # This is the important departure from ConfigParser for what you are looking for
          key = "=".join((key, str(value).replace('\n', '\n\t')))

        fp.write("%s\n" % (key))
      fp.write("\n")


class MainWindow(Tix.Tk):
	def __init__(self,parent):
		Tix.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		self.config(menu=self.menu)

	def initialize(self):
		self.grid()
		self.geometry("445x385")

		self.configParser=GrumpyConfigParser()
		self.configParser.optionxform = str
		configFilePath='cmd/config_firemsg.cfg'
		self.configParser.read(configFilePath)

		self.menu=Tkinter.Menu(self)
		self.subMenu=Tkinter.Menu(self.menu)
		self.subMenu.add_command(label="Save",command=self.save)
		self.subMenu.add_command(label="Reset file parameters",command=self.reset)
		self.subMenu.add_command(label="Reset initial parameters",command=self.reset_init)
		self.subMenu.add_command(label="Quit",command=self.quit)
		self.menu.add_cascade(label="File", menu=self.subMenu)

		ongletBook=Tix.NoteBook(self)
		ongletBook.add("onglet1", label='Main config')
		ongletBook.add("onglet2", label='Day process')
		ongletBook.add("onglet3", label='Advanced variable')

		p1 = ongletBook.subwidget_list["onglet1"]
		p2 = ongletBook.subwidget_list["onglet2"]
		p3 = ongletBook.subwidget_list["onglet3"]
		
		canvas1=Tkinter.Canvas(p1)
		canvas2=Tkinter.Canvas(p2)
		canvas3=Tkinter.Canvas(p3)

		###############################"#Canvas1
		i=0
		#FIREMSG VARIABLE
		self.labelp1_1=Tkinter.Label(canvas1,text=main_variable[0]+' :',anchor=Tkinter.W)
		self.labelp1_1.grid(row=i,column=0)
		self.valuep1_1=self.configParser.get('Main config',main_variable[0])
		self.entValuep1_1=Tkinter.StringVar()
		self.entryp1_1=Tkinter.Entry(canvas1,textvariable=self.entValuep1_1, width=30)
		self.entryp1_1.grid(row=i,column=1)
		self.entryp1_1.insert(0,self.valuep1_1)
		self.button1=Tkinter.Button(canvas1,text='Change',command=self.path_button)
		self.button1.grid(row=i,column=2)
		i+=1

		#MPOP PATH
		self.labelp1_13=Tkinter.Label(canvas1,text='MPOP_PATH :',anchor=Tkinter.W)
		self.labelp1_13.grid(row=i,column=0)
		self.valuep1_13=self.configParser.get('Main config',main_variable[12])
		self.entValuep1_13=Tkinter.StringVar()
		self.entryp1_13=Tkinter.Entry(canvas1,textvariable=self.entValuep1_13, width=30)
		self.entryp1_13.grid(row=i,column=1)
		self.entryp1_13.insert(0,self.valuep1_13)
		self.button1=Tkinter.Button(canvas1,text='Change',command=self.path_button)
		self.button1.grid(row=i,column=2)
		i+=1		

		#ENABLE FIRE DETECTION
		self.checkValuep1_11=Tkinter.StringVar()
		self.checkfirep1_11=Tkinter.Checkbutton(canvas1,text=main_variable[10],variable=self.checkValuep1_11,onvalue="true",offvalue="false",anchor=Tkinter.W)
		self.checkfirep1_11.grid(row=i,column=1)
		self.valuep1_11=self.configParser.get('Main config',main_variable[10])
		if self.valuep1_11=="true" :
			self.checkfirep1_11.select()
		else :
			self.checkfirep1_11.deselect()
		i+=1

		#INTERMEDIATE_FILES
		self.checkValuep1_12=Tkinter.StringVar()
		self.checkSaveFilep1_12=Tkinter.Checkbutton(canvas1,text=main_variable[11],variable=self.checkValuep1_12,onvalue="true",offvalue="false",anchor=Tkinter.W)
		self.checkSaveFilep1_12.grid(row=i,column=1)
		self.valuep1_12=self.configParser.get('Main config',main_variable[11])
		if self.valuep1_12=="true" :
			self.checkSaveFilep1_12.select()
		else :
			self.checkSaveFilep1_12.deselect()
		i+=1

		#ENABLE POSTGRESQL
		self.checkValuep1_2=Tkinter.StringVar()
		self.checkPGp1_2=Tkinter.Checkbutton(canvas1,text=main_variable[1],variable=self.checkValuep1_2,onvalue="true",offvalue="false",anchor=Tkinter.W)
		self.checkPGp1_2.grid(row=i,column=1)
		self.valuep1_2=self.configParser.get('Main config',main_variable[1])
		if self.valuep1_2=="true" :
			self.checkPGp1_2.select()
		else :
			self.checkPGp1_2.deselect()
		i+=1
		
		#PG_DBNAME
		self.labelp1_3=Tkinter.Label(canvas1,text=main_variable[2]+' :',anchor=Tkinter.W)
		self.labelp1_3.grid(row=i,column=0)
		self.valuep1_3=self.configParser.get('Main config',main_variable[2])
		self.entValuep1_3=Tkinter.StringVar()
		self.entryp1_3=Tkinter.Entry(canvas1,textvariable=self.entValuep1_3, width=30)
		self.entryp1_3.grid(row=i,column=1)
		self.entryp1_3.insert(0,self.valuep1_3)
		i+=1
		
		#PG_HOST
		self.labelp1_10=Tkinter.Label(canvas1,text=main_variable[9]+' :',anchor=Tkinter.W)
		self.labelp1_10.grid(row=i,column=0)
		self.valuep1_10=self.configParser.get('Main config',main_variable[9])
		self.entValuep1_10=Tkinter.StringVar()
		self.entryp1_10=Tkinter.Entry(canvas1,textvariable=self.entValuep1_10, width=30)
		self.entryp1_10.grid(row=i,column=1)
		self.entryp1_10.insert(0,self.valuep1_10)
		i+=1

		#PG_TABLENAME
		self.labelp1_4=Tkinter.Label(canvas1,text=main_variable[3]+' :',anchor=Tkinter.W)
		self.labelp1_4.grid(row=i,column=0)
		self.valuep1_4=self.configParser.get('Main config',main_variable[3])
		self.entValuep1_4=Tkinter.StringVar()
		self.entryp1_4=Tkinter.Entry(canvas1,textvariable=self.entValuep1_4, width=30)
		self.entryp1_4.grid(row=i,column=1)
		self.entryp1_4.insert(0,self.valuep1_4)
		i+=1
		
		#PG_USER
		self.labelp1_5=Tkinter.Label(canvas1,text=main_variable[4]+' :',anchor=Tkinter.W)
		self.labelp1_5.grid(row=i,column=0)
		self.valuep1_5=self.configParser.get('Main config',main_variable[4])
		self.entValuep1_5=Tkinter.StringVar()
		self.entryp1_5=Tkinter.Entry(canvas1,textvariable=self.entValuep1_5, width=30)
		self.entryp1_5.grid(row=i,column=1)
		self.entryp1_5.insert(0,self.valuep1_5)
		i+=1

		#PG_PW
		self.labelp1_6=Tkinter.Label(canvas1,text=main_variable[5]+' :',anchor=Tkinter.W)
		self.labelp1_6.grid(row=i,column=0)
		self.valuep1_6=self.configParser.get('Main config',main_variable[5])
		self.entValuep1_6=Tkinter.StringVar()
		self.entryp1_6=Tkinter.Entry(canvas1,textvariable=self.entValuep1_6, width=30)
		self.entryp1_6.grid(row=i,column=1)
		self.entryp1_6.insert(0,self.valuep1_6)
		i+=1

		#FTP_host
		self.labelp1_7=Tkinter.Label(canvas1,text=main_variable[6]+' :',anchor=Tkinter.W)
		self.labelp1_7.grid(row=i,column=0)
		self.valuep1_7=self.configParser.get('Main config',main_variable[6])
		self.entValuep1_7=Tkinter.StringVar()
		self.entryp1_7=Tkinter.Entry(canvas1,textvariable=self.entValuep1_7, width=30)
		self.entryp1_7.grid(row=i,column=1)
		self.entryp1_7.insert(0,self.valuep1_7)
		i+=1

		#FTP_name
		self.labelp1_8=Tkinter.Label(canvas1,text=main_variable[7]+' :',anchor=Tkinter.W)
		self.labelp1_8.grid(row=i,column=0)
		self.valuep1_8=self.configParser.get('Main config',main_variable[7])
		self.entValuep1_8=Tkinter.StringVar()
		self.entryp1_8=Tkinter.Entry(canvas1,textvariable=self.entValuep1_8, width=30)
		self.entryp1_8.grid(row=i,column=1)
		self.entryp1_8.insert(0,self.valuep1_8)
		i+=1

		#FTP_pw
		self.labelp1_9=Tkinter.Label(canvas1,text=main_variable[8]+' :',anchor=Tkinter.W)
		self.labelp1_9.grid(row=i,column=0)
		self.valuep1_9=self.configParser.get('Main config',main_variable[8])
		self.entValuep1_9=Tkinter.StringVar()
		self.entryp1_9=Tkinter.Entry(canvas1,textvariable=self.entValuep1_9, width=30)
		self.entryp1_9.grid(row=i,column=1)
		self.entryp1_9.insert(0,self.valuep1_9)
		i+=1
		
		self.saveButton=Tkinter.Button(canvas1,text='Save',command=self.save)
		self.saveButton.grid(row=i,column=1)
		i+=1
		self.resetButton=Tkinter.Button(canvas1,text='Reset',command=self.reset)
		self.resetButton.grid(row=i,column=1)
		canvas1.grid(row=1,column=0)

		##############################Canvas2
		i=0

		#DateDeb
		self.labelp2_1=Tkinter.Label(canvas2,text=day_process_variable[0]+' (format YYYY-MM-DD) :',anchor=Tkinter.W)
		self.labelp2_1.grid(row=i,column=0)
		self.valuep2_1=self.configParser.get('Day process',day_process_variable[0])
		self.entValuep2_1=Tkinter.StringVar()
		self.entryp2_1=Tkinter.Entry(canvas2,textvariable=self.entValuep2_1,width=30)
		self.entryp2_1.grid(row=i,column=1)
		self.entryp2_1.insert(0,self.valuep2_1)
		i+=1

		#DateFin
		self.labelp2_2=Tkinter.Label(canvas2,text=day_process_variable[1]+' (format YYYY-MM-DD) :',anchor=Tkinter.W)
		self.labelp2_2.grid(row=i,column=0)
		self.valuep2_2=self.configParser.get('Day process',day_process_variable[1])
		self.entValuep2_2=Tkinter.StringVar()
		self.entryp2_2=Tkinter.Entry(canvas2,textvariable=self.entValuep2_2,width=30)
		self.entryp2_2.grid(row=i,column=1)
		self.entryp2_2.insert(0,self.valuep2_2)
		i+=1

		#FTPdownload
		self.checkValuep2_3=Tkinter.StringVar()
		self.checkFTPp2_3=Tkinter.Checkbutton(canvas2,text=day_process_variable[2],variable=self.checkValuep2_3,onvalue="true",offvalue="false",anchor=Tkinter.W)
		self.checkFTPp2_3.grid(row=i,column=1)
		self.valuep2_3=self.configParser.get('Day process',day_process_variable[2])
		if self.valuep2_3=="true" :
			self.checkFTPp2_3.select()
		else :
			self.checkFTPp2_3.deselect()
		i+=1



		self.saveButton=Tkinter.Button(canvas2,text='Save',command=self.savep2)
		self.saveButton.grid(row=i,column=1)
		i+=1

		self.saveButton=Tkinter.Button(canvas2,text='Reset',command=self.resetp2)
		self.saveButton.grid(row=i,column=1)
		i+=1
		
		self.launchButton=Tkinter.Button(canvas2,text='Launch Day Process',command=self.launch_fd_day)
		self.launchButton.grid(row=i,column=1)
		i+=1
		
		canvas2.grid(row=1,column=0)

		##############################Canvas3
		self.framep3_1=Tkinter.LabelFrame(canvas3, text='Simple Threshold')
		self.framep3_1.grid(row=0, column=0)
		i=0

		#T039
		self.labelp3_1=Tkinter.Label(self.framep3_1,text=advanced_variable[0]+' :',anchor=Tkinter.W)
		self.labelp3_1.grid(row=i,column=0)
		self.valuep3_1=self.configParser.get('Advanced variable',advanced_variable[0])
		self.entValuep3_1=Tkinter.StringVar()
		self.entryp3_1=Tkinter.Entry(self.framep3_1,textvariable=self.entValuep3_1,width=30)
		self.entryp3_1.grid(row=i,column=1)
		self.entryp3_1.insert(0,self.valuep3_1)
		i+=1

		#T108
		self.labelp3_2=Tkinter.Label(self.framep3_1,text=advanced_variable[1]+' :',anchor=Tkinter.W)
		self.labelp3_2.grid(row=i,column=0)
		self.valuep3_2=self.configParser.get('Advanced variable',advanced_variable[1])
		self.entValuep3_2=Tkinter.StringVar()
		self.entryp3_2=Tkinter.Entry(self.framep3_1,textvariable=self.entValuep3_2,width=30)
		self.entryp3_2.grid(row=i,column=1)
		self.entryp3_2.insert(0,self.valuep3_2)
		i+=1

		#delta_day
		self.labelp3_3=Tkinter.Label(self.framep3_1,text=advanced_variable[2]+' :',anchor=Tkinter.W)
		self.labelp3_3.grid(row=i,column=0)
		self.valuep3_3=self.configParser.get('Advanced variable',advanced_variable[2])
		self.entValuep3_3=Tkinter.StringVar()
		self.entryp3_3=Tkinter.Entry(self.framep3_1,textvariable=self.entValuep3_3,width=30)
		self.entryp3_3.grid(row=i,column=1)
		self.entryp3_3.insert(0,self.valuep3_3)
		i+=1

		#delta_night
		self.labelp3_4=Tkinter.Label(self.framep3_1,text=advanced_variable[3]+' :',anchor=Tkinter.W)
		self.labelp3_4.grid(row=i,column=0)
		self.valuep3_4=self.configParser.get('Advanced variable',advanced_variable[3])
		self.entValuep3_4=Tkinter.StringVar()
		self.entryp3_4=Tkinter.Entry(self.framep3_1,textvariable=self.entValuep3_4,width=30)
		self.entryp3_4.grid(row=i,column=1)
		self.entryp3_4.insert(0,self.valuep3_4)
		i+=1

		#day_start
		self.labelp3_5=Tkinter.Label(self.framep3_1,text=advanced_variable[4]+' :',anchor=Tkinter.W)
		self.labelp3_5.grid(row=i,column=0)
		self.valuep3_5=self.configParser.get('Advanced variable',advanced_variable[4])
		self.entValuep3_5=Tkinter.StringVar()
		self.entryp3_5=Tkinter.Entry(self.framep3_1,textvariable=self.entValuep3_5,width=30)
		self.entryp3_5.grid(row=i,column=1)
		self.entryp3_5.insert(0,self.valuep3_5)
		i+=1

		#day_end
		self.labelp3_6=Tkinter.Label(self.framep3_1,text=advanced_variable[5]+' :',anchor=Tkinter.W)
		self.labelp3_6.grid(row=i,column=0)
		self.valuep3_6=self.configParser.get('Advanced variable',advanced_variable[5])
		self.entValuep3_6=Tkinter.StringVar()
		self.entryp3_6=Tkinter.Entry(self.framep3_1,textvariable=self.entValuep3_6,width=30)
		self.entryp3_6.grid(row=i,column=1)
		self.entryp3_6.insert(0,self.valuep3_6)
		i+=1

		self.framep3_2=Tkinter.LabelFrame(canvas3, text='Contextual Threshold')
		self.framep3_2.grid(row=1, column=0)

		#window_width
		self.labelp3_7=Tkinter.Label(self.framep3_2,text=advanced_variable[6]+' :',anchor=Tkinter.W)
		self.labelp3_7.grid(row=i,column=0)
		self.valuep3_7=self.configParser.get('Advanced variable',advanced_variable[6])
		self.entValuep3_7=Tkinter.StringVar()
		self.entryp3_7=Tkinter.Entry(self.framep3_2,textvariable=self.entValuep3_7,width=30)
		self.entryp3_7.grid(row=i,column=1)
		self.entryp3_7.insert(0,self.valuep3_7)
		i+=1

		#potfire_nb_limit
		self.labelp3_8=Tkinter.Label(self.framep3_2,text=advanced_variable[7]+' :',anchor=Tkinter.W)
		self.labelp3_8.grid(row=i,column=0)
		self.valuep3_8=self.configParser.get('Advanced variable',advanced_variable[7])
		self.entValuep3_8=Tkinter.StringVar()
		self.entryp3_8=Tkinter.Entry(self.framep3_2,textvariable=self.entValuep3_8,width=30)
		self.entryp3_8.grid(row=i,column=1)
		self.entryp3_8.insert(0,self.valuep3_8)
		i+=1

		#level_requierement
		self.labelp3_9=Tkinter.Label(self.framep3_2,text=advanced_variable[8]+' :',anchor=Tkinter.W)
		self.labelp3_9.grid(row=i,column=0)
		self.valuep3_9=self.configParser.get('Advanced variable',advanced_variable[8])
		self.entValuep3_9=Tkinter.StringVar()
		self.entryp3_9=Tkinter.Entry(self.framep3_2,textvariable=self.entValuep3_9,width=30)
		self.entryp3_9.grid(row=i,column=1)
		self.entryp3_9.insert(0,self.valuep3_9)
		i+=1

		self.saveButton=Tkinter.Button(canvas3,text='Save',command=self.savep3)
		self.saveButton.grid(row=i,column=1)
		i+=1
		self.saveButton=Tkinter.Button(canvas3,text='Reset',command=self.resetp3)
		self.saveButton.grid(row=i,column=1)
		i+=1		

		canvas3.grid(row=0,column=0)

		ongletBook.grid(row=1,column=0)

	def save(self):
		self.configParser.set('Main config','FIREMSG_PATH',self.entryp1_1.get())

		self.configParser.set('Main config','PPP_CONFIG_DIR',self.entryp1_13.get())

		if (self.checkValuep1_11.get()=="true"):
			self.configParser.set('Main config','ENABLE_FIRE_DETECTION','true')
		else:
			self.configParser.set('Main config','ENABLE_FIRE_DETECTION','false')
		
		if (self.checkValuep1_2.get()=="true"):
			self.configParser.set('Main config','ENABLE_POSTGRES','true')
		else:
			self.configParser.set('Main config','ENABLE_POSTGRES','false')

		if (self.checkValuep1_12.get()=="true"):
			self.configParser.set('Main config','SAVE_INTERMEDIATE_FILES','true')
		else:
			self.configParser.set('Main config','SAVE_INTERMEDIATE_FILES','false')
		
		self.configParser.set('Main config','PG_DBNAME',self.entryp1_3.get())
		
		self.configParser.set('Main config','PG_HOST',self.entryp1_10.get())
		
		self.configParser.set('Main config','PG_TABLENAME',self.entryp1_4.get())
		
		self.configParser.set('Main config','PG_USER',self.entryp1_5.get())
		
		self.configParser.set('Main config','PG_PW',self.entryp1_6.get())
		
		self.configParser.set('Main config','FTP_host',self.entryp1_7.get())
		
		self.configParser.set('Main config','FTP_name',self.entryp1_8.get())
		
		self.configParser.set('Main config','FTP_pw',self.entryp1_9.get())
		
		with open (r'cmd/config_firemsg.cfg','wb') as configfile:
			self.configParser.write(configfile) 


	def savep2(self):
		self.configParser.set('Day process','dateDeb',self.entryp2_1.get())

		self.configParser.set('Day process','dateFin',self.entryp2_2.get())

		if (self.checkValuep2_3.get()=="true"):
			self.configParser.set('Day process','FTP_download','true')
		else:
			self.configParser.set('Day process','FTP_download','false')
		with open (r'cmd/config_firemsg.cfg','wb') as configfile:
			self.configParser.write(configfile) 


	def savep3(self):
		self.configParser.set('Advanced variable','T039',self.entryp3_1.get())

		self.configParser.set('Advanced variable','T108',self.entryp3_2.get())
		
		self.configParser.set('Advanced variable','delta_day',self.entryp3_3.get())
		
		self.configParser.set('Advanced variable','delta_night',self.entryp3_4.get())
		
		self.configParser.set('Advanced variable','day_start',self.entryp3_5.get())
		
		self.configParser.set('Advanced variable','day_end',self.entryp3_6.get())
		
		self.configParser.set('Advanced variable','window_width',self.entryp3_7.get())
		
		self.configParser.set('Advanced variable','potfire_nb_limit',self.entryp3_8.get())
		
		self.configParser.set('Advanced variable','level_requirement',self.entryp3_9.get())
		
		with open (r'cmd/config_firemsg.cfg','wb') as configfile:
			self.configParser.write(configfile) 

	def save_all(self):
		self.save()
		self.savep2()
		self.savep3()

	def reset(self):
		self.entValuep1_1.set(self.configParser.get('Main config',main_variable[0]))

		self.entValuep1_13.set(self.configParser.get('Main config',main_variable[12]))

		if (self.configParser.get('Main config',main_variable[10]) == 'true'):
			self.checkfirep1_11.select()
		else :
			self.checkfirep1_11.deselect()

		if (self.configParser.get('Main config',main_variable[1]) == 'true'):
			self.checkPGp1_2.select()
		else :
			self.checkPGp1_2.deselect()

		if (self.configParser.get('Main config',main_variable[11]) == 'true'):
			self.checkSaveFilep1_12.select()
		else :
			self.checkSaveFilep1_12.deselect()

		self.entValuep1_3.set(self.configParser.get('Main config',main_variable[2]))

		self.entValuep1_4.set(self.configParser.get('Main config',main_variable[3]))

		self.entValuep1_10.set(self.configParser.get('Main config',main_variable[9]))

		self.entValuep1_5.set(self.configParser.get('Main config',main_variable[4]))

		self.entValuep1_6.set(self.configParser.get('Main config',main_variable[5]))

		self.entValuep1_7.set(self.configParser.get('Main config',main_variable[6]))

		self.entValuep1_8.set(self.configParser.get('Main config',main_variable[7]))

		self.entValuep1_9.set(self.configParser.get('Main config',main_variable[8]))

	def resetp2(self):
		self.entValuep2_1.set(self.configParser.get('Day process',day_process_variable[0]))

		self.entValuep2_2.set(self.configParser.get('Day process',day_process_variable[1]))

		if self.configParser.get('Day process',day_process_variable[2])=="true" :
			self.checkFTPp2_3.select()
		else :
			self.checkFTPp2_3.deselect()


	def resetp3(self):
		self.entValuep3_1.set(self.configParser.get('Advanced variable',advanced_variable[0]))

		self.entValuep3_2.set(self.configParser.get('Advanced variable',advanced_variable[1]))

		self.entValuep3_3.set(self.configParser.get('Advanced variable',advanced_variable[2]))

		self.entValuep3_4.set(self.configParser.get('Advanced variable',advanced_variable[3]))

		self.entValuep3_5.set(self.configParser.get('Advanced variable',advanced_variable[4]))

		self.entValuep3_6.set(self.configParser.get('Advanced variable',advanced_variable[5]))

		self.entValuep3_7.set(self.configParser.get('Advanced variable',advanced_variable[6]))

		self.entValuep3_8.set(self.configParser.get('Advanced variable',advanced_variable[7]))

		self.entValuep3_9.set(self.configParser.get('Advanced variable',advanced_variable[8]))

	def reset_init(self):
		#Canvas 1
		self.entValuep1_1.set('/home/user/firemsg')
		self.entValuep1_13.set('/home/user/.local/lib/python2.7/site-packages/eggfolder/mpop')
		self.checkfirep1_11.select()
		self.checkSaveFilep1_12.select()
		self.checkPGp1_2.select()
		self.entValuep1_3.set('')
		self.entValuep1_4.set('')
		self.entValuep1_10.set('')
		self.entValuep1_5.set('')
		self.entValuep1_6.set('')
		self.entValuep1_7.set('oisftp.eumetsat.org')
		self.entValuep1_8.set('')
		self.entValuep1_9.set('')
		#Canvas 2
		self.entValuep2_1.set('')
		self.entValuep2_2.set('')
		self.checkFTPp2_3.deselect()
		#Canvas 3
		self.entValuep3_1.set(300)
		self.entValuep3_2.set(290)
		self.entValuep3_3.set(15)
		self.entValuep3_4.set(5)
		self.entValuep3_5.set(8)
		self.entValuep3_6.set(18)
		self.entValuep3_7.set(5)
		self.entValuep3_8.set(30)
		self.entValuep3_9.set(3.5)

	def launch_fd_day(self):
		script=self.configParser.get('Main config',main_variable[0])+'/cmd/fd_day_process.sh'
		os.popen("cd cmd;bash fd_day_process.sh &>/dev/null")

	def path_button(self):
		d=askdirectory()
		self.entValuep1_1.set(d)


if __name__== "__main__":
	window = MainWindow(None)
	window.title("FIREMSG")
	window.mainloop()