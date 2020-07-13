
#!/bin/python
                                                                                        
#                                                                                         
# ██╗    ██╗ █████╗ ████████╗██╗  ██╗██╗███╗   ██╗███████╗██╗      █████╗ ██████╗ ███████╗
# ██║    ██║██╔══██╗╚══██╔══╝██║ ██╔╝██║████╗  ██║██╔════╝██║     ██╔══██╗██╔══██╗██╔════╝
# ██║ █╗ ██║███████║   ██║   █████╔╝ ██║██╔██╗ ██║███████╗██║     ███████║██████╔╝███████╗
# ██║███╗██║██╔══██║   ██║   ██╔═██╗ ██║██║╚██╗██║╚════██║██║     ██╔══██║██╔══██╗╚════██║
# ╚███╔███╔╝██║  ██║   ██║   ██║  ██╗██║██║ ╚████║███████║███████╗██║  ██║██████╔╝███████║
#  ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
                                                                                        
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from   urllib.request import Request, urlopen
import datetime
import argparse

# Inspired by : https://hackaday.com/2014/03/31/sniffing-ph-sensor-rf-signals-for-feedback-re-your-esophagus/
# Details: https://dolske.wordpress.com/2014/03/25/hacks-all-the-way-down/

class parse_bravo_pH:
   name=""
   data_file=""
   output_file=""
   debug=None
   
   # init/constructor for class
   def __init__(self,name,data_file,output_file,debug=None):
      now = datetime.datetime.now()

      self.data_file=data_file
      self.output_file=output_file
      self.name=name
      self.debug=debug
      self.plot()
      
   # used for printing info messages to the screen for the user
   def info(self,msg):
      print(" Info: "+msg)

   # used for printing error messages to the screen for the user
   def error(self,msg):
      print(" Error: "+msg)      


   def plot(self):

      ph_levels=[]
      ph_time=[]
      data_store=[]
      with open(self.data_file,"r") as content:
         line="start"
         
         while line!="":
            line=content.readline()
            tokens=line.split(',')
            if len(tokens)<3: continue
            if tokens[0]=='time': continue
            date=tokens[0]
            hex=tokens[2]
            hex_data=hex[4:-4]
            mfid=hex_data[0:4]
            mf_msg_type=hex_data[4:6]
            ph_data1=int(hex_data[6:8], 16)/25 
            ph_data2=int(hex_data[8:10], 16)/25 
            ph_checksum=hex_data[10:12]
            
            datetime=pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S', utc=True)
            print("{0} mfid:{1} mf_msg_type:{2} ph1:{3} ph2:{4} ph_checksum:{5}".format(datetime,mfid,mf_msg_type,ph_data1,ph_data2,ph_checksum))
            line=[datetime,ph_data1]
            data_store.append(line)
            line=[datetime,ph_data2]
            data_store.append(line)

      df = pd.DataFrame(data_store)
      df.columns = ['date', 'ph']

      df.set_index('date', inplace=True)

      #plot data
      fig = plt.figure()
      ax1 = fig.add_subplot()
      ax1.plot(df.index.values,       df['ph'])
      
      ax1.set( xlabel="Date",
               ylabel="pH Level",
               title="{0} pH Levels".format(self.name))

      # Define the date format
      date_form = DateFormatter("%m-%d %H:%M")
      ax1.xaxis.set_major_formatter(date_form)

      # Ensure a major tick for each week using (interval=1) 
      ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
      plt.setp(ax1.get_xticklabels(), rotation=45)
      plt.show()



parser = argparse.ArgumentParser(description='downdetector datascrapeer')
parser.add_argument('--name'       , '-n' , help='your name', required=True)
parser.add_argument('--input'      , '-i' , help='csv_file', required=True)
parser.add_argument('--output'     , '-o' , help='output_file', required=True)
parser.add_argument('--debug'      , '-d' , help='show processing information',action='store_true', default=None)

args = parser.parse_args()

if args.name:
   parse_bravo_pH(args.name,args.input,args.output,args.debug)

else:
   parser.print_help()
