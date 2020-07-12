# bravo-pH decoder
- a MVP project to read, decode and plot the bravo pH esophageal sensor

- this is was a 4 hour weekend project. Treat it as such.

# example
![](data.png?raw=true)



### back story
Hi I'm Chris, I have acid reflux. My doctor ordered a procedure which implants a ph sensor in my esophagus.
- I wanted the data from the sensor 

### path to success
sensor->usb radio->decoder->csv->python->pandas->matlab

## Starting point
I found someone who had done something similar and was able to turbocharge my project with their information.
- https://hackaday.com/2014/03/31/sniffing-ph-sensor-rf-signals-for-feedback-re-your-esophagus/
- https://dolske.wordpress.com/2014/03/25/hacks-all-the-way-down/

### hardware 
- https://www.amazon.com/gp/product/B01MQEAEHZ/ A usb RTL_SDR (Software Defined Radio) for use with a computer ($30-$60)

### software
- https://github.com/merbanan/rtl_433 The scanner/decoder used for this automation
- https://github.com/chris17453/bravo_pH my automation for pltting the data

### install requirements
you need to install the rtl_433 project. Follow the link. It will give you a nice build manual.


## To record the data
The following command's will scan the radio and output all the data into a csv file for processing.
```
sudo ./scan.sh
#or by hand
rtl_433 -R 0 -X n=BRAVO,m=OOK_PWM,s=320,l=760,r=716,g=0,t=0,y=576,rows=2,bits=48 -F csv:data.csv
```

## To plot the data 
```
python  plot.py
```

## sensor info
- recieves input in the form of hydrogen. 
- transmits on frequency 433.92 mhz using pulse width modulation.  (same as a car key fob)
- blindly broadcasts
- has a very weak transmission. Limit 0-3 feet. the closer the better
- the data is collected every 6 seconds
- transmits every 12 seconds
- will detach and pass as waste in 5/6 days
- 48 bits (6) bytes are transmitted. 
- the first 3 bytes never change. and can be uses as an ID
- bytes 1,2 are a manufacture ID
- byte 3 is the message type
- byte 4 is a ph sensor value 
- byte 5 is a ph sensor value
- byte 6 is a checksum of the 2



## Notes
It's that easy. I'm thankfull to tll the opensource contributors who helped make this happen.

Good luck innovating!

