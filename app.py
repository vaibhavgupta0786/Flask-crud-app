from flask import Flask ,  request , jsonify, Response , render_template , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
import subprocess
import asyncio
import os 
import flask
import ffmpy3
import speech_recognition as sr 
from pydub import AudioSegment 
from pydub.silence import split_on_silence 


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__ , template_folder="templates")
# Database
folder_name = "Uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'newdb.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_root = os.path.dirname(os.path.abspath(__file__))

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Metadata(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    File_Size =   db.Column(db.String(5000) )
    File_Name =   db.Column(db.String(5000) )
    File_Type = db.Column(db.String(5000) )
    MIME_Type  =  db.Column(db.String(5000) )                 
    Major_Brand  =  db.Column(db.String(5000) )                   
    Minor_Version                   =  db.Column(db.String(5000) )
    Compatible_Brands               =  db.Column(db.String(5000) )
    Movie_Header_Version            =  db.Column(db.String(5000) )
    Create_Date                     =  db.Column(db.String(5000) )
    Modify_Date                     =  db.Column(db.String(5000) )
    Time_Scale                      =  db.Column(db.String(5000) )
    Duration                        =  db.Column(db.String(5000) )
    Preferred_Rate                  =  db.Column(db.String(5000) )
    Preferred_Volume                =  db.Column(db.String(5000) )
    Preview_Time                    =  db.Column(db.String(5000) )
    Preview_Duration                =  db.Column(db.String(5000) )
    Poster_Time                     =  db.Column(db.String(5000) )
    Selection_Time                  =  db.Column(db.String(5000) )
    Selection_Duration              =  db.Column(db.String(5000) )
    Current_Time                    =  db.Column(db.String(5000) )
    Next_Track_ID                   =  db.Column(db.String(5000) )
    Track_Header_Version            =  db.Column(db.String(5000) )
    Track_Create_Date               =  db.Column(db.String(5000) )
    Track_Modify_Date               =  db.Column(db.String(5000) )
    Track_ID                        =  db.Column(db.String(5000) )
    Track_Duration                  =  db.Column(db.String(5000) )
    Track_Layer                     =  db.Column(db.String(5000) )
    Track_Volume                    =  db.Column(db.String(5000) )
    Image_Width                     =  db.Column(db.String(5000) )
    Image_Height                    =  db.Column(db.String(5000) )
    Graphics_Mode                   =  db.Column(db.String(5000) )
    Op_Color                        =  db.Column(db.String(5000) )
    Compressor_ID                   =  db.Column(db.String(5000) )
    Source_Image_Width              =  db.Column(db.String(5000) )
    Source_Image_Height             =  db.Column(db.String(5000) )
    X_Resolution                    =  db.Column(db.String(5000) )
    Y_Resolution                    =  db.Column(db.String(5000) )
    Compressor_Name                 =  db.Column(db.String(5000) )
    Bit_Depth                       =  db.Column(db.String(5000) )
    Pixel_Aspect_Ratio              =  db.Column(db.String(5000) )
    Video_Frame_Rate                =  db.Column(db.String(5000) )
    Matrix_Structure                =  db.Column(db.String(5000) )
    Media_Header_Version            =  db.Column(db.String(5000) )
    Media_Create_Date               =  db.Column(db.String(5000) )
    Media_Modify_Date               =  db.Column(db.String(5000) )
    Media_Time_Scale                =  db.Column(db.String(5000) )
    Media_Duration                  =  db.Column(db.String(5000) )
    Media_Language_Code             =  db.Column(db.String(5000) )
    Handler_Type                    =  db.Column(db.String(5000) )
    Handler_Description             =  db.Column(db.String(5000) )
    Balance                         =  db.Column(db.String(5000) )
    Audio_Format                    =  db.Column(db.String(5000) )
    Audio_Channels                  =  db.Column(db.String(5000) )
    Audio_Bits_Per_Sample           =  db.Column(db.String(5000) )
    Audio_Sample_Rate               =  db.Column(db.String(5000) )
    Media_Data_Size                 =  db.Column(db.String(5000) )
    Media_Data_Offset               =  db.Column(db.String(5000) )
    Image_Size                      =  db.Column(db.String(5000) )
    Megapixels                      =  db.Column(db.String(5000) )
    Avg_Bitrate                     =  db.Column(db.String(5000) )
    Rotation                        =  db.Column(db.String(5000) )



    def __init__( self ,File_Name,File_Type,File_Size,MIME_Type,Major_Brand,Minor_Version,Compatible_Brands,
        Movie_Header_Version,Create_Date,Modify_Date,Time_Scale,
        Duration,Preferred_Rate,Preferred_Volume,Preview_Time,
        Preview_Duration,Poster_Time,Selection_Time,Selection_Duration,Current_Time,Next_Track_ID,Track_Header_Version,Track_Create_Date,
        Track_Modify_Date,Track_ID,Track_Duration,Track_Layer,Track_Volume,
        Image_Width,Image_Height,Graphics_Mode,Op_Color,
        Compressor_ID,Source_Image_Width,Source_Image_Height,X_Resolution,Y_Resolution,Compressor_Name,Bit_Depth,Pixel_Aspect_Ratio,Video_Frame_Rate,
        Matrix_Structure,Media_Header_Version,Media_Create_Date,Media_Modify_Date,Media_Time_Scale,Media_Duration,Media_Language_Code,Handler_Type,Handler_Description,
        Balance,Audio_Format,Audio_Channels,Audio_Bits_Per_Sample,Audio_Sample_Rate,Media_Data_Size,Media_Data_Offset,Image_Size
        ,Megapixels,Avg_Bitrate,Rotation):
        self.File_Name=File_Name
        self.File_Type=File_Type
        self.File_Size = File_Size
        self.MIME_Type=MIME_Type
        self.Major_Brand=Major_Brand
        self.Minor_Version=Minor_Version
        self.Compatible_Brands=Compatible_Brands
        self.Movie_Header_Version=Movie_Header_Version
        self.Create_Date=Create_Date
        self.Modify_Date=Modify_Date
        self.Time_Scale=Time_Scale
        self.Duration=Duration
        self.Preferred_Rate=Preferred_Rate
        self.Preferred_Volume=Preferred_Volume
        self.Preview_Time=Preview_Time
        self.Preview_Duration=Preview_Duration
        self.Poster_Time=Poster_Time
        self.Selection_Time=Selection_Time
        self.Selection_Duration=Selection_Duration
        self.Current_Time=Current_Time
        self.Next_Track_ID=Next_Track_ID
        self.Track_Header_Version=Track_Header_Version
        self.Track_Create_Date=Track_Create_Date
        self.Track_Modify_Date=Track_Modify_Date
        self.Track_ID=Track_ID
        self.Track_Duration=Track_Duration
        self.Track_Layer=Track_Layer
        self.Track_Volume=Track_Volume
        self.Image_Width=Image_Width
        self.Image_Height=Image_Height
        self.Graphics_Mode=Graphics_Mode
        self.Op_Color=Op_Color
        self.Compressor_ID=Compressor_ID
        self.Source_Image_Width=Source_Image_Width
        self.Source_Image_Height=Source_Image_Height
        self.X_Resolution=X_Resolution
        self.Y_Resolution=Y_Resolution
        self.Compressor_Name=Compressor_Name
        self.Bit_Depth=Bit_Depth
        self.Pixel_Aspect_Ratio=Pixel_Aspect_Ratio
        self.Video_Frame_Rate=Video_Frame_Rate
        self.Matrix_Structure=Matrix_Structure
        self.Media_Header_Version=Media_Header_Version
        self.Media_Create_Date=Media_Create_Date
        self.Media_Modify_Date=Media_Modify_Date
        self.Media_Time_Scale=Media_Time_Scale
        self.Media_Duration=Media_Duration
        self.Media_Language_Code=Media_Language_Code
        self.Handler_Type=Handler_Type
        self.Handler_Description=Handler_Description
        self.Balance=Balance
        self.Audio_Format=Audio_Format
        self.Audio_Channels=Audio_Channels
        self.Audio_Bits_Per_Sample=Audio_Bits_Per_Sample
        self.Audio_Sample_Rate=Audio_Sample_Rate
        self.Media_Data_Size=Media_Data_Size
        self.Media_Data_Offset=Media_Data_Offset
        self.Image_Size=Image_Size
        self.Megapixels=Megapixels
        self.Avg_Bitrate=Avg_Bitrate
        self.Rotation=Rotation
 
class Videoinfos(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    transcription = db.Column(db.String(5000) )
    name = db.Column(db.String(5000) )        
    def __init__(self,name,transcription):
        self.Name = name
        self.Transcription = transcription

class MetadataSchema(ma.ModelSchema):
    class Meta:
        model = Metadata


class VideoinfosSchema(ma.ModelSchema):
    class Meta:
        model = Videoinfos


db.create_all()
metadata_schema = MetadataSchema(many=True)
videoinfo_schema = VideoinfosSchema(many=True) 

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload" ,methods = [ "POST" , "GET"])
def upload():
    if request.method == "POST":
        if request.files:
            files = request.files["file"]
            print(request.files)
            target = os.path.join(app_root, 'files/{}'.format(folder_name))

            if not os.path.isdir(target):
                os.mkdir(target)
            ##for file in files:
               # print (type(file))
            if (files.filename != '')  : 
                print (files.filename)
               #print(file.decode())
                filename = secure_filename(files.filename)
                print("{} is the file name".format(files.filename))
                
                destination = "/".join([target, filename])
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                files.save(destination)
                print("saved")
                new_metadata = extractmetadata(destination)
                #print(new_netadata)

                audio_destination =  video_to_audio_converter(filename,destination)
                db.session.add(new_metadata)

            ##new_videoinfo = extractvideoinfo(audio_destination)
                db.session.commit()

            else:
                print("no File given to load")    
        
            
    return render_template("upload.html")

def extractmetadata(input_file):
    exe = "exiftool"
    #proc = await asyncio.create_subprocess_exec(
    #    [exe,input_file]
    #    stdout=asyncio.subprocess.PIPE,
    #    stderr=asyncio.subprocess.PIPE)
    proc = subprocess.Popen([exe, input_file],stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    stdout, stderr =  proc.communicate()
    array = []
    lot = []
    for string in stdout.split("\n"):
        #print(string.split(":")[0].split("  ")[0])
        if (string.split(";")[0] != ""):
            array.append(string.split(":")[0].strip())


        if (len(string.split(":")) > 1):
            lot.append(string.split(":")[1].strip())
        else:
            lot.append("")
    res = {'Compressor_Name':"DNE" , 'Pixel_Aspect_Ratio':"DNE"}        
    res1 = {array[i].replace(" " , "_").replace("/" , ""): lot[i] for i in range(len(array))} 
    res.update(res1)
    #print(res)
    new_metadata = Metadata(  res['File_Name'],  res['File_Type'],  res['File_Size'], res['MIME_Type'],                 res['Major_Brand'], res['Minor_Version'], 
        res['Compatible_Brands'], res['Movie_Header_Version'],res['Create_Date'], res['Modify_Date'], res['Time_Scale'], res['Duration'], res['Preferred_Rate'],
        res['Preferred_Volume'], res['Preview_Time'], res['Preview_Duration'], res['Poster_Time'], res['Selection_Time'], res['Selection_Duration'], res['Current_Time'], 
        res['Next_Track_ID'], 
        res['Track_Header_Version'], res['Track_Create_Date'], res['Track_Modify_Date'], res['Track_ID'], res['Track_Duration'], res['Track_Layer'], res['Track_Volume'], 
        res['Image_Width'], res['Image_Height'], res['Graphics_Mode'], res['Op_Color'], 
        res['Compressor_ID'], res['Source_Image_Width'], res['Source_Image_Height'], 
        res['X_Resolution'], res['Y_Resolution'], res['Compressor_Name'], res['Bit_Depth'], res['Pixel_Aspect_Ratio'], res['Video_Frame_Rate'], res['Matrix_Structure'], 
        res['Media_Header_Version'], res['Media_Create_Date'], res['Media_Modify_Date'], res['Media_Time_Scale'], res['Media_Duration'], res['Media_Language_Code'], 
        res['Handler_Type'],
        res['Handler_Description'], res['Balance'],
        res['Audio_Format'], res['Audio_Channels'], res['Audio_Bits_Per_Sample'], res['Audio_Sample_Rate'], res['Media_Data_Size'], res['Media_Data_Offset'],
        res['Image_Size'], res['Megapixels'], res['Avg_Bitrate'], res['Rotation'])
    #print(new_metadata)
    return new_metadata 


def extractvideoinfo(filepath):
    # open the audio file stored in 
	# the local system as a wav file. 
	song = AudioSegment.from_wav(path) 
	# open a file where we will concatenate 
	# and store the recognized text 
	fh = open("recognized.txt", "w+") 
		
	# split track where silence is 0.5 seconds 
	# or more and get chunks
	chunks = split_on_silence(song, 
		# must be silent for at least 0.5 seconds 
		# or 500 ms. adjust this value based on user 
		# requirement. if the speaker stays silent for 
		# longer, increase this value. else, decrease it. 
		min_silence_len = 1000, 

		# consider it silent if quieter than -16 dBFS 
		# adjust this per requirement 
		silence_thresh = -16
	) 
	# create a directory to store the audio chunks. 
	try: 
		os.mkdir('audio_chunks') 
	except(FileExistsError): 
		pass

	# move into the directory to 
	# store the audio files. 
	os.chdir('audio_chunks') 

	i = 0 ; print("processing chunks") 
	# process each chunk 
	for chunk in chunks: 
			
		# Create 0.5 seconds silence chunk 
		chunk_silent = AudioSegment.silent(duration = 10) 

		# add 0.5 sec silence to beginning and 
		# end of audio chunk. This is done so that 
		# it doesn't seem abruptly sliced. 
		audio_chunk = chunk_silent + chunk + chunk_silent 

		# export audio chunk and save it in 
		# the current directory. 
		print("saving chunk{0}.wav".format(i)) 
		# specify the bitrate to be 192 k 
		audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 

		# the name of the newly created chunk 
		filename = 'chunk'+str(i)+'.wav'

		print("Processing chunk "+str(i)) 

		# get the name of the newly created chunk 
		# in the AUDIO_FILE variable for later use. 
		file = filename 

		# create a speech recognition object 
		r = sr.Recognizer() 

		# recognize the chunk 
		with sr.AudioFile(file) as source: 
			# remove this if it is not working 
			# correctly. 
			r.adjust_for_ambient_noise(source) 
			audio_listened = r.listen(source) 

		try: 
			# try converting it to text 
			rec = r.recognize_google(audio_listened) 
			# write the output to the file. 
			fh.write(rec+". ") 

		# catch any errors. 
		except sr.UnknownValueError: 
			print("Could not understand audio") 

		except sr.RequestError as e: 
			print("Could not request results. check your internet connection") 

		i += 1

	os.chdir('..') 

def video_to_audio_converter(filename , destiny):
    print("**************  converter started ***********")
    #preext= input.filename.substring(0 , filename.lastIndexOf('.')+1).toLowerCase()

    output_file = '{}_converted.wav'.format(filename)
    print (filename)
    print (output_file)
    target = os.path.join(app_root, 'files/{}'.format("converted_media"))
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    destination = "/".join([target, output_file])
    if ( os.path.exists(destination) == False & os.path.isfile(destination) == False ):
        print ("File Already EXISTS")
        ff = ffmpy3.FFmpeg(
        inputs={ os.path.abspath(destiny) : None },
        outputs={ destination : None})
        ff.run()
    print("***************** converter Done ****************")
    return destination

@app.route('/metadata/latest' , methods=["GET" ] )
def get_metadata():
    if(db.session.query( Metadata ).first() is None ):
        return Response( {' {\"message\" : \"No Data in the Database\"} '}, mimetype='application/json')

    #data = db.session.query(  Metadata ).first()
    #data = db.Session.query(Metadata).filter(Metadata.id == session.query(func.max(Metadata.id)))
    data = db.session.query(Metadata).order_by(Metadata.id.desc()).first()
    return Response( { tojsonstring(data) }, mimetype='application/json')


@app.route('/transcription/latest' , methods=["GET" ])
def get_transcription():
    
    if(db.session.query(Videoinfos).first() is None):
        return Response( {' {\"message\" : \"No Data in the Database\"} '}, mimetype='application/json')
    data = db.session.query(Videoinfos).order_by(Videoinfos.id.desc()).first()

    return Response({ tojsonstring(data)  }  , mimetype='application/json')


def tojsonstring( data ):
    strng = '{'
    print("****************")
    for attr, value in data.__dict__.items():
        #print(attr, value)
        strng += ' \"{}\" : \"{}\" '.format(attr,value)

    strng += '}'    
    strng = strng.replace('\"  \"' , '\" , \"')
    print("****************")    
    return strng


@app.route("/metadata/all" , methods=["GET" ])
def get_all_metadata():
    all_metadata = db.session.query(Metadata).all()
    result = metadata_schema.dump(all_metadata)
    if (len(result) == 0 ): 
        return Response( {' {\"message\" : \"No Data in the Database\"} '}, mimetype='application/json')
    print(type(result))    
    return Response(flask.json.dumps(result) , mimetype='application/json' )

@app.route("/transcription/all" , methods=["GET"])
def get_all_transcription():
    all_videoInfos =  db.session.query(Videoinfos).all()
    print(all_videoInfos)
    result = videoinfo_schema.dump(all_videoInfos)
    if (len(result) == 0 ): 
        return Response( {' {\"message\" : \"No Data in the Database\"} '}, mimetype='application/json')
    return Response(flask.json.dumps(result) ,mimetype='application/json' )





# Run Server
if __name__ == '__main__':
  app.run(debug=True) 
  