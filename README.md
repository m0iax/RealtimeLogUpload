# RealtimeLogUpload
 Realtime log uploader for JS8Call. QRZ.com and eQSL.cc
 
 This app is designed to work with JS8Call. http://js8call.com
 
 This app listens to the UDP output from JS8Call and will automatically upload log ADIF entries to QRZ.com and/or eQSL.cc when the user logs a QSO in JS8Call.
 
 It will run on any OS that will run python.
 
 Prerequiesites:
 
 <ul>
 <li>JS8Call</li>
 <li>python 3.7 or later</li>
 <li>an account on QRZ.com with a valid APIKEY*</li>
 <li>a User name and password for eQSL.cc*</li>
</ul>

*and account for either QRZ.com or eQSL.cc is required. you dont need both but it will work with both

Install:

clone or download this repo if downlading a .zip file unzip into a directory on your computer.

<b>Linux (including Raspberry Pi)</b>

run a command prompt, change directory to the installation directory.<br>

cd RealtimeLogUpload<br>

Before you run it for the first time enter the command:
chmod +x adifUploader.py

to run the app:
./adifUploader.py

<b>Windows</b>
 from the command prompt<br>
 
 cd RealTimeLogUpload<br>
 
 py -m adifUploader.py<br>
 
 <br>
 <br>
 
 The first time you run the app it will create two files in the installation directory<br>
 
 js8call.cfg<br>
 loguploader.cfg<br>
 
 js8call.cfg has the UDP port number to listen on, it uses the JS8Call default of 2242. You only need to change this if you have changed it in the JS8Call settings.<br>
 
 To set up the loguploader open the file loguploader.cfg in a text editor, the contents will look like this:<br>
 <p>
 [QRZ.COM]<br>
apikey = APIKEY<br>
<br>
[EQSL.CC]<br>
username = USERNAME<br>
password = PASSWORD<br>
<br>
[SERVICES]<br>
eqsl = 0<br>
qrz = 0<br>
 </p>
 
<b>Do not change the format of the file</b>, but update the values APIKEY, USERNAME, PASSWORD with your details, for example 

 <p>
 [QRZ.COM]<br>
apikey = ABCD-EFGH<br>
<br>
[EQSL.CC]<br>
username = MyUserName<br>
password = MyPassword<br>
<br>
[SERVICES]<br>
eqsl = 0<br>
qrz = 0<br>
 </p>

Note if you do not use one or the other then you do not need to change the default setting for it.
In the services section you can specify which ones you want enabled at startup change the 0 to a 1 if you want is enabled by default when you run the app, leave them at 0 and you will just need to click the button after running.
<br>

Once you have updated the settings file, close the app and run it again to pick up the new settings values.
Click on the buttons to enable or disable auto upload, the button will be red or green to indicate disabled or enbled.
If you run from a command prompt or terminal window you will see upload error messages if the upload fails, if it is sucessful you will not see a message after upload.
<br>

<b>Future Enhancements Will include</b><br>
<ul>
 <li>Upload Status messages to be shown on the UI</li>
 <li>QRZ Callsign Lookup</li>
 <li>Offline Mode - collect ADIF for upload when back online</li>
</ul>

If you have any feature requests please get in touch http://m0iax.com/findme

73
Mark
M0IAX



