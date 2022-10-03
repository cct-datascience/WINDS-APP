#Output Webpage
#WINDS Dashboard
#======================Block 0: Adding Libraries=============================
from datetime import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
import pymysql

pymysql.install_as_MySQLdb()
from flask import Flask,render_template, request, Response
from flask import redirect, url_for, session
import re
from sqlalchemy import create_engine
from matplotlib.ticker import MaxNLocator
import os
import pymysql
pymysql.install_as_MySQLdb()
import io
import base64
import urllib.parse
import random
import bcrypt
import boto3
import numpy as np
import mariadb
import sys


#=========================================================#
def lengthen_list(l, n, pad=0):
    if len(l) >= n:
        del l[n:]
    else:
        l.extend([pad] * (n - len(l)))
        
def stringToList(string):
    listRes = list(string.split(" "))
    return listRes
#==============================================================#
##=======================================================#

try:
    db = mariadb.connect(
        user = "root",
        password = "",
        host = "127.0.0.1",
        port = 3306,
        database = "winds_test")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
#==================================================================#
now = dt.today()
currentDate = now.strftime("%Y-%m-%d")
Output_Array=pd.read_sql('SELECT * from OutputWebpage_copy',con=db)
Irrigation_app=pd.read_sql('SELECT * from Irrigation_app',con=db)
neutron_probe=pd.read_sql('SELECT * from NeutronProbe',con=db)
weather_stations=pd.read_sql(sql='SELECT * from weather_stations_edited',con=db)
weather_stations=weather_stations.drop(weather_stations[weather_stations.Status == 'INACTIVE'].index)
list_ws=weather_stations.loc[:,'Location']
list_ws_drop=list_ws.tolist()
##================Webpage development for output layer variables===============================================4#
application = Flask(__name__)

#Populate our selections for the user, this is what they can pick from basically
plantingnum=Output_Array.loc[:,'PlantingNum'].drop_duplicates()
plantingname=Output_Array.loc[:,'Planting_name'].drop_duplicates()
fieldname=Output_Array.loc[:,'Field_name'].drop_duplicates()
accountname=Output_Array.loc[:,'Account_name'].drop_duplicates()

plant_number=plantingnum.tolist()
plant_name=plantingname.tolist()
field_name=fieldname.tolist()
account_name=accountname.tolist()

planting_date=Irrigation_app['Date']
planting_date=planting_date.tolist()
planting_date_irrigation=planting_date[20:]

application.secret_key = 'winds-app'

# Upload folder
UPLOAD_FOLDER = 'static/files'
application.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

DOWNLOAD_FOLDER='static/download'
application.config['DOWNLOAD_FOLDER']=DOWNLOAD_FOLDER

@application.route('/',methods=['GET','POST'])
@application.route('/index',methods=['GET','POST'])
def index():
    if 'loggedin' in session: #If the user is logged in
        return render_template('homepage_dropdown.html',username=session['username'])
        #return render_template('homepageloggedin.html',username=session['username'])
    else:
        return render_template("homepagev4.html")
#If the Layered Data Button is pressed
@application.route('/layereddata',methods=['GET','POST'])
def learnmore():
    #If they clicked the button
    if request.method== "POST":
        x=Output_Array.drop_duplicates('PlantingNum')
        y=x.loc[:, ['PlantingNum']]

        layered_data=['LayerWC','LayerDep','LayerAF','LayerInf','LayerPD']
        layerno=['1','2','3','4','5','6','7','8','9','10','11','12','13']
        DOY_1=list(range(166,321))  #166 to 320
        DOY_2=list(range(167,321))  #167 to 320
      #  return render_template('layerdata.html',dropdown_list=layered_data_selection,layered_data=layered_data,layerno=layerno,DOY_1=DOY_1,DOY_2=DOY_2)
        return render_template('layerdata.html',plant_name=plant_name,field_name=field_name,account_name=account_name,layered_data=layered_data,layerno=layerno,DOY_1=DOY_1,DOY_2=DOY_2)
@application.route("/login",methods=["GET", "POST"])
def login():
 # connect
    connection = db.raw_connection()
    cursor=connection.cursor()
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accounts table in out database
    #If the password is correct, we will direct them to the home page  
        if bcrypt.checkpw(password.encode('utf-8'),account[3]):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)
@application.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    connection = db.raw_connection()
    cursor=connection.cursor()
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_id=random.randint(100000,999999)
   
  #Check if account exists using MySQL
        select_stmt_check="SELECT * FROM accounts WHERE username=%(username)s"
        cursor.execute(select_stmt_check,{'username':username})
        #cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
                    
            hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

            
            cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', (new_id,fullname, username, hashed, email)) 

            #cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)', (new_id,fullname, username, password_string, email)) 
            connection.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
@application.route('/dataview',methods=['GET','POST'])
def viewlayered():
    if request.method== "POST":

        plant_name_user=request.form.get("plant_name",None)
        field_name_user=request.form.get("field_name",None)
        account_name_user=request.form.get("account_name",None)

        user_data=request.form.get("layered_data",None)
        layers=request.form.getlist("mycheckboxes",None)
        DOY_start=request.form.get("DOY_1",None)
        DOY_end=request.form.get("DOY_2",None)
        neutron_probe_box=request.form.get("neutronprobe",None)

        DOY_start=int(DOY_start)
        DOY_end=int(DOY_end)
        b=plant_name_user.split()
        tr=field_name_user.split()
        c=[" ".join(tr)]
        d=account_name_user.split()
        
        #Now we need to pull whatever data they requested
        if user_data=='LayerWC':
            db_variable=['WC L1', 'WC L2', 'WC L3', 'WC L4', 'WC L5', 'WC L6', 'WC L7', 'WC L8', 'WC L9', 'WC L10', 'WC L11' , 'WC L12' , 'WC L13']
            variable_data_WC=Output_Array.loc[(Output_Array['Planting_name'].isin(b)) & (Output_Array['Field_name'].isin(c)) & (Output_Array['Account_name'].isin(d))]
            variable_data=variable_data_WC[['DOY','WC L1', 'WC L2', 'WC L3', 'WC L4', 'WC L5', 'WC L6', 'WC L7', 'WC L8', 'WC L9', 'WC L10', 'WC L11' , 'WC L12' , 'WC L13']]
            #14 columns total DOY then L1, L2, etc, need to determine how to find which layers
            for i in range(0,len(layers)):
                it_layers=list(map(int,layers))
                x=variable_data.iloc[:,it_layers]
            DOY_frame=variable_data['DOY']
            final_frame=pd.concat([DOY_frame,x],axis=1)
            final_frame=final_frame[final_frame['DOY'].between(DOY_start,DOY_end)]
        if user_data=='LayerDep':
                db_variable=['Dep L1', 'Dep L2', 'Dep L3', 'Dep L4', 'Dep L5', 'Dep L6', 'Dep L7', 'Dep L8', 'Dep L9', 'Dep L10', 'Dep L11', 'Dep L12', 'Dep L13']
                variable_data_DP=Output_Array.loc[(Output_Array['Planting_name'].isin(b)) & (Output_Array['Field_name'].isin(c)) & (Output_Array['Account_name'].isin(d))]
                variable_data=variable_data_DP[['DOY','Dep L1', 'Dep L2', 'Dep L3', 'Dep L4', 'Dep L5', 'Dep L6', 'Dep L7', 'Dep L8', 'Dep L9', 'Dep L10', 'Dep L11', 'Dep L12', 'Dep L13']]
                for i in range(0,len(layers)):
                    it_layers=list(map(int,layers))
                    x=variable_data.iloc[:,it_layers]
                DOY_frame=variable_data['DOY']
                final_frame=pd.concat([DOY_frame,x],axis=1)
                final_frame=final_frame[final_frame['DOY'].between(DOY_start,DOY_end)]
        if user_data=='LayerAF':
                db_variable=['AF L1', 'AF L2', 'AF L3', 'AF L4', 'AF L5', 'AF L6', 'AF L7', 'AF L8', 'AF L9', 'AF L10', 'AF L11', 'AF L12', 'AF L13']
                variable_data_AF=Output_Array.loc[(Output_Array['Planting_name'].isin(b)) & (Output_Array['Field_name'].isin(c)) & (Output_Array['Account_name'].isin(d))]
                variable_data=variable_data_AF[['DOY','AF L1', 'AF L2', 'AF L3', 'AF L4', 'AF L5', 'AF L6', 'AF L7', 'AF L8', 'AF L9', 'AF L10', 'AF L11', 'AF L12', 'AF L13']]
                for i in range(0,len(layers)):
                    it_layers=list(map(int,layers))
                    x=variable_data.iloc[:,it_layers]
                DOY_frame=variable_data['DOY']
                final_frame=pd.concat([DOY_frame,x],axis=1)
                final_frame=final_frame[final_frame['DOY'].between(DOY_start,DOY_end)]
        if user_data=='LayerInf':
                db_variable=['Inf L1', 'Inf L2','Inf L3','Inf L4','Inf L5','Inf L6','Inf L7','Inf L8','Inf L9','Inf L10','Inf L11','Inf L12','Inf L13']
                variable_data_Inf=Output_Array.loc[(Output_Array['Planting_name'].isin(b)) & (Output_Array['Field_name'].isin(c)) & (Output_Array['Account_name'].isin(d))]
                variable_data=variable_data_Inf[['DOY','Inf L1', 'Inf L2','Inf L3','Inf L4','Inf L5','Inf L6','Inf L7','Inf L8','Inf L9','Inf L10','Inf L11','Inf L12','Inf L13']]
                for i in range(0,len(layers)):
                    it_layers=list(map(int,layers))
                    x=variable_data.iloc[:,it_layers]
                DOY_frame=variable_data['DOY']
                final_frame=pd.concat([DOY_frame,x],axis=1)
                final_frame=final_frame[final_frame['DOY'].between(DOY_start,DOY_end)]
        if user_data=='LayerPD':
                db_variable=['Pdep L1','Pdep L2','Pdep L3','Pdep L4','Pdep L5','Pdep L6','Pdep L7','Pdep L8','Pdep L9','Pdep L10','Pdep L11','Pdep L12','Pdep L13']
                variable_data_PD=Output_Array.loc[(Output_Array['Planting_name'].isin(b)) & (Output_Array['Field_name'].isin(c)) & (Output_Array['Account_name'].isin(d))]
                variable_data=variable_data_PD[['DOY','Pdep L1','Pdep L2','Pdep L3','Pdep L4','Pdep L5','Pdep L6','Pdep L7','Pdep L8','Pdep L9','Pdep L10','Pdep L11','Pdep L12','Pdep L13']]
                for i in range(0,len(layers)):
                    it_layers=list(map(int,layers))
                    x=variable_data.iloc[:,it_layers]
                DOY_frame=variable_data['DOY']
                final_frame=pd.concat([DOY_frame,x],axis=1)
                final_frame=final_frame[final_frame['DOY'].between(DOY_start,DOY_end)]
        global df_download
        #if they want to compare neutron probe
        if neutron_probe_box=='on':
            neutron_data=neutron_probe.loc[(neutron_probe['Planting Name'].isin(b))]
            neutron_df=neutron_data[['DOY','L1','L2','L3','L4','L5','L6','L7','L8','L9','L10','L11','L12','L13']]
            for i in range(0,len(layers)):
                            neutron_layers=list(map(int,layers))
                            neutron_x=neutron_df.iloc[:,neutron_layers]
            DOY_frame_neu=neutron_df['DOY']
            final_frame_neutron=pd.concat([DOY_frame_neu,neutron_x],axis=1)
            final_frame_neutron=final_frame_neutron[final_frame_neutron['DOY'].between(DOY_start,DOY_end)]

            img = io.BytesIO()
            y1=list(final_frame.columns.values)
            y2=list(final_frame_neutron.columns.values)
            del y1[0]
            del y2[0]
            first=final_frame.plot(x='DOY',y=y1,colormap='Accent')
            final_frame_neutron.plot(x='DOY',y=y2,ax=first,style=".",ms=12,colormap='Accent')
            plt.show()

            plt.savefig(img, format='png', bbox_inches="tight")  # save figure to the buffer
            plt.close()
            img.seek(0)  # rewind your buffer
            plot_url = urllib.parse.quote(base64.b64encode(img.read()).decode())
            
            planting_name_df=[b for i in range(0,len(final_frame))]
            field_name_df=[c for i in range(0,len(final_frame))]
            accountowner_df=[d for i in range(0,len(final_frame))]
            
            final_frame['Planting Name']=planting_name_df
            final_frame['Field Name']=field_name_df
            final_frame['Account Owner']=accountowner_df
            
            df_download=final_frame.to_csv(index=False)

            return render_template('layerdataview.html',user_plant=b,user_data=user_data,plot_url=plot_url)
        else:
                #act normal
            img = io.BytesIO()
            y=list(final_frame.columns.values)
            del y[0]
            final_frame.plot(x='DOY',y=y)
            plt.show()

            plt.savefig(img, format='png', bbox_inches="tight")  # save figure to the buffer
            plt.close()
            img.seek(0)  # rewind your buffer
            plot_url = urllib.parse.quote(base64.b64encode(img.read()).decode())
            
            planting_name_df=[b for i in range(0,len(final_frame))]
            field_name_df=[c for i in range(0,len(final_frame))]
            accountowner_df=[d for i in range(0,len(final_frame))]
            
            final_frame['Planting Name']=planting_name_df
            final_frame['Field Name']=field_name_df
            final_frame['Account Owner']=accountowner_df
            df_download=final_frame.to_csv(index=False)

            return render_template('layerdataview.html',user_plant=b,user_data=user_data,plot_url=plot_url)
    
#If they download data
@application.route('/getPlotCSV',methods=['GET','POST'])
def output_csv():
        csv=df_download
        return Response(csv,mimetype="text/csv", headers={"Content-disposition":"attachment; filename=requesteddata.csv"})
#If the Non Layered Button is pressed
@application.route('/nonlayered',methods=['GET','POST'])
def nonlayer():
    #If they clicked the button
    if request.method== "POST":
        x=Output_Array.drop_duplicates('PlantingNum')
        y=x.loc[:, ['PlantingNum']]
        plant_name=y.PlantingNum #plant name here is by planting number

        nonlayered_data=['KcbUsed','Ke','Evap','Transpiration','ET','PotTranspiration','CumulativePotentialET','CumulativeActualET','ReferenceET','oneminusc','EqMax','EqMaxNumber','IrrigationPlusRain','Leaching','DepthDifference','ET1','SumSourcesSinks']

        DOY_1=list(range(166,321))  #166 to 320
        DOY_2=list(range(167,321))  #166 to 320

        return render_template('nonlayerdata.html', plant_name=plantingname,field_name=field_name,account_name=account_name,nonlayered_data=nonlayered_data,DOY_1=DOY_1,DOY_2=DOY_2)

@application.route('/nonlayerdataview',methods=['GET','POST'])
def viewnonlayered():
    global nonlayered_df
    if request.method== "POST":
        plant_name_user=request.form.get("plant_name",None)
        field_name_user=request.form.get("field_name",None)
        user_data=request.form.get("nonlayered_data",None)
        DOY_start=request.form.get("DOY_1",None)
        DOY_end=request.form.get("DOY_2",None)

        DOY_start=int(DOY_start)
        DOY_end=int(DOY_end)

        b=plant_name_user.split()
        tr=field_name_user.split()

        c=[" ".join(tr)]

        Requested_Data=Output_Array.loc[(Output_Array['Planting_name'].isin(b)) & (Output_Array['Field_name'].isin(c))]

        numRows=Requested_Data.shape[0]
        numCols=1
        Requested_Variable= pd.DataFrame(index=range(numRows),columns=range(numCols))
        Requested_Variable[user_data]=Requested_Data[user_data]
        Requested_Value=Requested_Variable.drop([Requested_Variable.columns[0]], axis = 1)

        DOY_frame=Requested_Data['DOY']
        final_frame=pd.concat([DOY_frame,Requested_Value],axis=1)
        final_frame=final_frame[final_frame['DOY'].between(DOY_start,DOY_end)]
        df=final_frame

        img = io.BytesIO()
        y=list(df.columns.values)
        del y[0]
        df.plot(x='DOY',y=y)
        plt.show()

        plt.savefig(img, format='png', bbox_inches="tight")  # save figure to the buffer
        plt.close()
        img.seek(0)  # rewind your buffer
        plot_url = urllib.parse.quote(base64.b64encode(img.read()).decode())
        
        planting_name_df=[b for i in range(0,len(final_frame))]
        field_name_df=[c for i in range(0,len(final_frame))]
       
        df['Planting Name']=planting_name_df
        df['Field Name']=field_name_df
        
        nonlayered_df=df.to_csv(index=False)

        return render_template('nonlayerdataview.html',user_plant=b,user_data=user_data,plot_url=plot_url)
#If they download data
@application.route('/getPlotCSVnonlayered',methods=['GET','POST'])
def getcsv_nonlayered():
    csv=nonlayered_df
    return Response(csv,mimetype="text/csv", headers={"Content-disposition":"attachment; filename=requesteddata.csv"})
#If the Irrigation Button is pressed
@application.route('/irrigation',methods=['GET','POST'])
def irrigation():
    #Have them input the planting date

    #The depth of depletion at that time will be the depth to apply.
    if request.method== "POST":
        plant_name_irr=Irrigation_app.loc[:,'Planting_name'].drop_duplicates()
        field_name_irr=Irrigation_app.loc[:,'Field_name'].drop_duplicates()
        account_name_irr=Irrigation_app.loc[:,'Account_name'].drop_duplicates()

        plant_name_irr=plant_name_irr.tolist()
        field_name_irr=field_name_irr.tolist()
        account_name_irr=account_name_irr.tolist()

      #  return render_template('layerdata.html',dropdown_list=layered_data_selection,layered_data=layered_data,layerno=layerno,DOY_1=DOY_1,DOY_2=DOY_2)
        return render_template('irrigation.html',plant_name_irr=plant_name_irr,field_name_irr=field_name_irr,account_name_irr=account_name_irr,planting_date=planting_date_irrigation)
@application.route('/irrigationcalculator',methods=['GET','POST'])
def irrigation_calc():
    #If they select the next button on the irrigation page
    if request.method== "POST":

        plant_name_user=request.form.get("plant_name_irr",None)
        field_name_user=request.form.get("field_name_irr",None)
        date_user=request.form.get('planting_date',None)

        user_date_selection=date_user.split()
        Requested_Data=Irrigation_app.loc[(Irrigation_app['Date'].isin(user_date_selection))]
        AllowableDepl=Irrigation_app[['AllowableDepletion']].max()/25.4
        DOY_current=Requested_Data['DOY']
        DOY_num=int(DOY_current)
        
        DOY_range=[DOY_num-7,DOY_num+7]
        DOY_start=DOY_range[0]
        DOY_end=DOY_range[1]
        
        
        if DOY_num<=176:
            #Not all data will be produced
            print('Some data will be missing, add on forward for the number of days lost')
            DOY_start=167
            DOY_end=192
        else:
            #all is good 
            print('All applicable data will be shown')
            
        today_date=Requested_Data[['Date']] #should be that day

       # AllowableDepl=Requested_Data[['AllowableDepletion']]/25.4 # in inches
        AllowableDepl=AllowableDepl.values
        AllowableDepl=float(AllowableDepl)
        
        ActualDepl=Requested_Data['ActualDepletion']/25.4 # in inches
        ActualDepl=ActualDepl.values
        ActualDepl=float(ActualDepl)
        
        raw_value=(Irrigation_app['AllowableDepletion'].max()-Requested_Data['ActualDepletion'])/25.4 #in inches
        current_depl=Requested_Data[['ActualDepletion']]/25.4 #in inches
            
        raw_value=raw_value.values #readily available water
        current_depl= current_depl.values
        
        raw_value=float('%.3g' % float(raw_value))
        current_depl=float('%.3g' % float(current_depl))
        
        #find our average values, use iloc to find it
        data_top=Requested_Data.head()
        index_no=list(data_top.index)
        index_int=int(index_no[0])
        
        #Let's make a new mini-df to find our average values
        lhs=index_int-2
        rhs=index_int+5
        
        #Pick the 5 days previously for pot_et_avg 
        if lhs < 0:
            df_raw=Irrigation_app.iloc[0:rhs]
            df_mini=df_raw.drop(index=index_int)
            et_avg=abs(df_mini['ET_neg'].mean())
            pot_et_df=Irrigation_app.iloc[0:rhs]
            pot_et_avg=abs(pot_et_df['PotTranspiration'].mean()/25.4) #in inches
        else:
            df_raw=Irrigation_app.iloc[lhs:rhs]
            df_mini=df_raw.drop(index=index_int)    
            et_avg=abs(df_mini['ET_neg'].mean())  
            pot_et_df=Irrigation_app.iloc[index_int-5:index_int]
            pot_et_avg=abs(pot_et_df['PotTranspiration'].mean()/25.4) #in inches
            
        if ActualDepl >= AllowableDepl:
            #past time to irrigate
            print('It is past time to irrigate. Irrigate the depletion amount.')
            Irr_depth=Requested_Data[['ActualDepletion']] #mm convert to inches
            Irr_depth_inches=Irr_depth/25.4 #converted to inches
            irr_depth_raw=Irr_depth_inches.values
            irr_depth_rounded=float('%.3g' % irr_depth_raw)
            
            Irr_date=Requested_Data[['Date']] #should be that day
        
            raw_value=(Irrigation_app['AllowableDepletion'].max()-Requested_Data['ActualDepletion'])/25.4 #in inches
            current_depl=Requested_Data[['ActualDepletion']]/25.4 #in inches
            
            raw_value=raw_value.values
            current_depl= current_depl.values
            
            raw_value=float('%.3g' % float(raw_value))
            current_depl=float('%.3g' % float(current_depl))
            
            irr_date_raw=Irr_date['Date'].values.tolist()
            irr_date_raw=''.join(irr_date_raw)
            
            DOY_graph=DOY_num
                        
            WeekBefore=Irrigation_app[Irrigation_app['DOY'].between(DOY_num-7,DOY_num)]
            FullDOY=Irrigation_app[Irrigation_app['DOY'].between(DOY_num-7,DOY_num+7)]
            
            #Add the projected 7 days after
            day1=ActualDepl+pot_et_avg
            day2=day1+pot_et_avg
            day3=day2+pot_et_avg
            day4=day3+pot_et_avg
            day5=day4+pot_et_avg
            day6=day5+pot_et_avg
            day7=day6+pot_et_avg
            
            WeekAfter=[day1,day2,day3,day4,day5,day6,day7]
            WeekAfter_df=pd.Series(WeekAfter)
            
            y_lhs=WeekBefore['ActualDepletion']/25.4 # in inches
            
            y=pd.concat([y_lhs,WeekAfter_df])
            x=FullDOY['DOY']
            
            img = io.BytesIO()
            fig, ax=plt.subplots()
            ax.set_xlabel('DOY')
            ax.set_ylabel('Actual Depletion (inches)')
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
            ax.plot(x,y,label='Actual depletion (inches)',color='black')
            dot_on_graph=(Requested_Data['ActualDepletion']/25.4).to_string(index=False)
            plt.plot(DOY_num,float(dot_on_graph),'ro',color='blue',label='Selected DOY')
        
            plt.axvline(DOY_graph,-100,100,color='red',label='Predicted Irrigation Day')
            ax.legend(loc = 'upper left')
            plt.show()
        
            plt.savefig(img, format='png', bbox_inches="tight")  # save figure to the buffer
            plt.close()
            img.seek(0)  # rewind your buffer
            plot_url_1 = urllib.parse.quote(base64.b64encode(img.read()).decode())
            
            return render_template('irrigationcalculator_caseone.html',user_date_selection=user_date_selection[0],user_DOY=DOY_num,Irr_depth=irr_depth_rounded, irr_date=irr_date_raw,raw_value=raw_value,current_depl=current_depl,plot_url_1=plot_url_1)
        
        else: 
            #Now we check to see if our pot_et_avg will allow us to irrigate within 7 days
            print('We are in case 2')
            today_date=Requested_Data[['Date']] #should be that day
    
            day1=ActualDepl+pot_et_avg
            day2=day1+pot_et_avg
            day3=day2+pot_et_avg
            day4=day3+pot_et_avg
            day5=day4+pot_et_avg
            day6=day5+pot_et_avg
            day7=day6+pot_et_avg
            
            WeekAfter=[day1,day2,day3,day4,day5,day6,day7]
            WeekAfter_df=pd.Series(WeekAfter)
            
            day=[]
            
            for item in WeekAfter:
                if item >= AllowableDepl:
                    day.append(item)
                    
            if len(day)==0: #If our list is empty
                print('We will not irrigate in the 7 day period.')
                DOY_graph=DOY_num
                        
                WeekBefore=Irrigation_app[Irrigation_app['DOY'].between(DOY_num-7,DOY_num)]
                FullDOY=Irrigation_app[Irrigation_app['DOY'].between(DOY_num-7,DOY_num+7)]
        
                y_lhs=WeekBefore['ActualDepletion']/25.4 # in inches
            
                y=pd.concat([y_lhs,WeekAfter_df])
                x=FullDOY['DOY']
                
                img = io.BytesIO()
                fig, ax=plt.subplots()
                ax.set_xlabel('DOY')
                ax.set_ylabel('Actual Depletion (inches)')
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                
                ax.plot(x,y,label='Actual depletion (inches)',color='black')
                dot_on_graph=(Requested_Data['ActualDepletion']/25.4).to_string(index=False)
                plt.plot(DOY_num,float(dot_on_graph),'ro',color='blue',label='Selected DOY')
                
                ax.legend(loc = 'upper left')
                plt.show()
                
                plt.savefig(img, format='png', bbox_inches="tight")  # save figure to the buffer
                plt.close()
                img.seek(0)  # rewind your buffer
                plot_url_1 = urllib.parse.quote(base64.b64encode(img.read()).decode())
                
                return render_template('irrigationcalculator_casethree.html',user_date_selection=user_date_selection[0],user_DOY=DOY_num,raw_value=raw_value,current_depl=current_depl,plot_url_1=plot_url_1)
            else:
                print('We will irrigate in the 7 day period.')
                output_irrigate=[i for i, item in enumerate(WeekAfter) if item in day]
                days_to_irrigate=min(output_irrigate)+1 #0 index
                today_date['NewDate'] = pd.to_datetime(today_date.Date) + pd.to_timedelta(days_to_irrigate, unit="D")
                today_date['NewDate']=today_date['NewDate'].astype(str).str.replace("\s:00", "")
                irr_date_raw=today_date['NewDate']
                irr_date_print=today_date['NewDate'].to_string(index=False)
                
                date_list=today_date.astype(str)
                Irr_depth_df=Irrigation_app.loc[(Irrigation_app['Date'].isin(date_list['NewDate']))]
                applied_irr=Irr_depth_df['ActualDepletion']/25.4 #in inches
                
                irr_depth_raw=applied_irr.values
                irr_depth_rounded=float('%.3g' % irr_depth_raw)
                    
                DOY_graph=DOY_num+days_to_irrigate
                        
                WeekBefore=Irrigation_app[Irrigation_app['DOY'].between(DOY_num-7,DOY_num)]
                FullDOY=Irrigation_app[Irrigation_app['DOY'].between(DOY_num-7,DOY_num+7)]
                
                y_lhs=WeekBefore['ActualDepletion']/25.4 # in inches
            
                y=pd.concat([y_lhs,WeekAfter_df])
                x=FullDOY['DOY']
                
                img = io.BytesIO()
                fig, ax=plt.subplots()
                ax.set_xlabel('DOY')
                ax.set_ylabel('Actual Depletion (inches)')
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                
                ax.plot(x,y,label='Actual depletion (inches)',color='black')
                dot_on_graph=(Requested_Data['ActualDepletion']/25.4).to_string(index=False)
                plt.plot(DOY_num,float(dot_on_graph),'ro',color='blue',label='Selected DOY')
                
                plt.axvline(DOY_graph,-100,100,color='red',label='Predicted Irrigation Day')
                ax.legend(loc = 'upper left')
                plt.show()
                
                plt.savefig(img, format='png', bbox_inches="tight")  # save figure to the buffer
                plt.close()
                img.seek(0)  # rewind your buffer
                plot_url_1 = urllib.parse.quote(base64.b64encode(img.read()).decode())
                
                return render_template('irrigationcalculator_casetwo.html',user_date_selection=user_date_selection[0],user_DOY=DOY_num,Irr_depth=irr_depth_rounded, irr_date=irr_date_print,raw_value=raw_value,current_depl=current_depl,plot_url_1=plot_url_1)        


#If the user is logged in, they will be able to access this page
@application.route('/datainput',methods=['GET','POST'])
def datainput():
        # Check if user is loggedin
    if 'loggedin' in session:
        #check to see what they typed, but first render the page
        # User is loggedin show them the home page
        WS_select=list_ws_drop
        cropname=['Cotton','Guar','Guayule']
        soil_select=['Clay','Clay loam','Loam','Loamy Sand','Sand','Sandy Clay','Sandy Clay Loam','Sandy loam','Silt','Silty clay','Silty clay loam','Silt loam']
        return render_template('datainput.html',soil_select=soil_select,cropname=cropname,WS_select=WS_select)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@application.route('/datainputsuccess',methods=['GET','POST'])
def datainputsuccess():
        # Check if user is loggedin
    if 'loggedin' in session:
        if request.method== "POST":
            
            planting_name_user=request.form.get("plantingname",None)
            
            
            if planting_name_user !='': #if they typed the data 
                planting_name_user=request.form.get("plantingname",None)
                field_name_user=request.form.get("fieldname",None)
                account_name=session['username']
                #account_name=request.form.get("accountname",None)
                cropname_user=request.form.get("cropname",None)
                planting_start=request.form.get("plantingstart",None)
                planting_end=request.form.get("plantingend",None)
                sections=request.form.get("sections",None)
                soil_select=request.form.get("soil_select",None)
                WS_select=request.form.get("WS_select",None)

                connection = db.raw_connection()
                cursor=connection.cursor()
                
                plantingyear='2021'
                plantingdate=planting_start
                
                cursor.execute('INSERT INTO plantings_inter (Plantingname, Plantingyear, Plantingdate, Datestart, Dateend, Fieldname, Accountname, Cropname, Sections, Soil, WeatherStation) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)', (planting_name_user, plantingyear,plantingdate, planting_start, planting_end, field_name_user, account_name,cropname_user, sections, soil_select, WS_select)) 
                connection.commit()
    
                return render_template('datainputsuccess.html') 
            else:
                file = request.files['file']
                file_path = os.path.join(application.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                 
                df_file=pd.read_csv(file_path,sep=",")
                df_file.to_sql(name='plantings_inter',con=db,if_exists='append',index=False)
             
                return render_template('datainputsuccess.html') 

#If they download data template form
@application.route('/gettemplate',methods=['GET','POST'])
def gettemplate():
    #on AWS 
    s3 = boto3.client('s3')
    BUCKET='elasticbeanstalk-us-west-1-634500801455'
    
    file=s3.get_object(Bucket=BUCKET,Key='datatemplate.csv')
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=datatemplate.csv"}
    )
    #on local host
    #csv="C:/Users/danie/Desktop/Irrigation_app - v4/static/files/datatemplate.csv"
    #return send_file(csv,mimetype='text/csv',attachment_filename='datatemplate.csv',as_attachment=True)
@application.route('/irrigationinput',methods=['GET','POST'])
def irrigation_input():
    #We need to identify how many sections the logged in user has 
    if 'loggedin' in session:
        #check to see what they typed, but first render the page
        Accountname=session['username']
        #Find our username in the plantings_inter to determine how many sections they have 
        connection = db.raw_connection()
        cursor=connection.cursor()
        select_stmt_check="SELECT * FROM plantings_inter WHERE Accountname=%(Accountname)s"
        cursor.execute(select_stmt_check,{'Accountname':Accountname})
        account_info_irr = cursor.fetchone()
        if account_info_irr != None: #they have entered a planting
            fields=account_info_irr[9]
            int(float(fields))
            irr_type=['sprinkler','furrow','drip']
            
            return render_template('irrigationinput.html',irr_type=irr_type,fields=fields)
        if account_info_irr == None:
            return render_template('no_planting.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@application.route('/irrigationsuccess',methods=['GET','POST'])
def irrigation_success():
    if 'loggedin' in session:
        Accountname=session['username']
        irr_date=request.form.getlist("irr_date",None)
        irr_type=request.form.getlist('irr_type',None)
         #read their irrigation amounts
        x=request.form.getlist("x",None)
        account_string=stringToList(Accountname)
        ab=irr_date+account_string+irr_type+x
        
        
        columns=['Date','Accountname','type','Amount_Sec1','Amount_Sec2','Amount_Sec3','Amount_Sec4','Amount_Sec5','Amount_Sec6','Amount_Sec7','Amount_Sec8','Amount_Sec9','Amount_Sec10','Amount_Sec11','Amount_Sec12','Amount_Sec13','Amount_Sec14','Amount_Sec15','Amount_Sec16','Amount_Sec17','Amount_Sec18','Amount_Sec19','Amount_Sec20']
     
        if len(ab) < 23:
            #if we have less than 20 sections, add NULLS until len(ab) == 24
            lengthen_list(ab,23)
    
 
        df_final=pd.DataFrame(data=[ab],columns=columns)
        df_final=df_final.replace(0,np.nan)
        df_final.to_sql(name='irrigation_user',con=db,if_exists='append',index=False)
    
        return render_template('irrigationsuccess.html')
    return redirect(url_for('login'))
@application.route('/neutronprobe',methods=['GET','POST'])
def neutronprobeupload():
    if 'loggedin' in session:

        #if the user is logged in, find their planting name/treatment name and populate the dropdown list....
        Accountname=session['username']
        connection = db.raw_connection()
        cursor=connection.cursor()
        select_stmt_check="SELECT * FROM plantings_inter WHERE Accountname=%(Accountname)s"
        cursor.execute(select_stmt_check,{'Accountname':Accountname})
        account_info_irr = cursor.fetchone()
        
        if account_info_irr != None: #they have entered a planting
            user_plantingname_raw=account_info_irr[1]
            user_plantingname=[user_plantingname_raw]

            return render_template('neutronprobeupload.html',plantingname=user_plantingname)
        if account_info_irr == None:

            return render_template('no_planting.html')

        return redirect(url_for('login'))
@application.route('/neutronprobesuccess',methods=['GET','POST'])
def neutronprocess():

        file = request.files['file']
        file_path = os.path.join(application.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
 
        #Define our constants
        standard=16361.0
        slope=[0.30845,0.24146] #0th value: 0-30cm, 1stvalue: below 30cm only the first column needs the first value
        intercept=[-0.098356,-0.057349] #0th value: 0-30cm, 1stvalue: below 30cm
       
        Accountname=session['username']
        connection = db.raw_connection()
        cursor=connection.cursor()
        select_stmt_check="SELECT * FROM plantings_inter WHERE Accountname=%(Accountname)s"
        cursor.execute(select_stmt_check,{'Accountname':Accountname})
        account_info = cursor.fetchone()
        plantingnum_db=account_info[0] #read their planting number from the database

        int(float(plantingnum_db))
        #=================================#
        np_template=pd.read_excel(file)
        raw=np_template.drop([0,1,2])
        date_of_collection=raw.columns.values.tolist()
        date_NP=date_of_collection[1] #corresponds to the date the file was submitted
        DOY=date_NP.strftime("%j")[-1:]
        #rename columns & drop extra
        raw.columns=['TubeNumber','0-25cm','35-55cm','65-85cm','95-115cm','125-145cm','155-175cm','185-205cm']
        raw.drop([3], axis=0, inplace=True)
        #replace any present text (NOT NaN) with NaN's using regex
        finalized=raw.replace(r'^([A-Za-z]|[0-9]|_)+$', np.NaN, regex=True)
        ###====================================================#
        ###Now we have our raw dataframe that needs to be manipulated
        ##index 4-42, column 3 is the first slope and intercept
        finalized['0-25cm']=(100*((finalized['0-25cm']/standard)*slope[0]+intercept[0]))
        for i in finalized.columns[2:8]:
            finalized[i]=(100*((finalized[i]/standard)*slope[1]+intercept[1]))
        #F
        ###Now we have our DF, need to take averages and all that jazz and rearrange by treatment/ID
        ###======================================================#
        ####We need to add a new column with Plot and Treat ID, using Key from Diaa's file
        TreatmentID=[1,1,1,1,1,1]
        ###1-d50,....6F100
        ##
        finalized['TreatmentID']=TreatmentID 
        ###Need to take averages of all 5 treat ID's independently 
        mean_by_id=finalized.groupby('TreatmentID').mean()
        ##=============================================================#
        ##===define our constants====#
        depth_diff=30
        TAW=240
        FC_Frac=['0.28','0.28','0.28','0.28','0.28','0.19','0.20']
        ##====define our dataframes====#
        df=mean_by_id.iloc[[0]]
        df_T=df.T
        df_T.columns=['Percentage']
        ##==============================================================#
        results=[]
        depths=[]
        for i in [df_T]:
            mm=i['Percentage']/100
            moisture=mm*depth_diff
        
            cumulative=moisture.cumsum()
            
            FC_cm=np.array(FC_Frac,dtype=float)*depth_diff
            FC_cm_pd=pd.Series(FC_cm)
            
            sum_root_moisture=moisture.iloc[0:6].sum()
            sum_root_fc=FC_cm_pd.iloc[0:6].sum()     #sum of FC_cm, minus the last one
        
            if sum_root_moisture==0:
                depl_mm=0
            else:
                depl_mm=10*(sum_root_fc-sum_root_moisture)
            
            depl_per=100*depl_mm/TAW
            
        #    results.append(
        #            {
        #                #'TreatmentName': TreatmentName,
        #                'SumRootDepth': sum_root_moisture,
        #                'DepletionMM': depl_mm,
        #                'DepletionPercent': depl_per
        #                
        #            }
        #        )
        #    final_frame=pd.DataFrame(results)
            
            depths.append(
                    {
                      'L1':mm[6],
                      'L2':mm[5],
                      'L3':mm[4],
                      'L4':mm[3],
                      'L5':mm[2],
                      'L6':mm[1],
                      'L7':mm[0]     
                    }
                    )
        #final_frame['TreatmentName']=TreatmentName   
        
        neutron=pd.DataFrame(depths,columns=['L1','L2','L3','L4','L5','L6','L7'])
        neutron['Planting Name']='D50_MAC_R6' # get planting name from USER
        
        DOY_new=[]
        plantingnum_new=[]
        date_new=[]
        DOY_new=[DOY for i in range(0,len(neutron))]
        plantingnum_new=[plantingnum_db for i in range(0,len(neutron))]  #replace w/ plantingnum, access db for it... this is fine for now..
        date_new=[date_NP.date() for i in range(0,len(neutron))]
        neutron['Planting number']=plantingnum_new
        neutron['Date']=date_new
        neutron['DOY']=DOY_new
        neutron=neutron[['Planting number','Planting Name','Date','DOY','L1','L2','L3','L4','L5','L6','L7']]
        neutron.to_sql(name='NeutronProbe',con=db,if_exists='append',index=False)
        
        global neutron_download
        
        neutron_download=neutron.to_csv(index=False)
        
        #fix output
        return render_template('neutronprobesuccess.html',date_NP=date_NP,DOY=DOY,sum_root_moisutre=sum_root_moisture,depl_mm=depl_mm,depl_per=depl_per)#,plot_neutron=plot_neutron)
#If they need a template
@application.route('/gettemplateneutron',methods=['GET','POST'])
def get_neutron_template():
    #on AWS 
    s3 = boto3.client('s3')
    BUCKET='elasticbeanstalk-us-west-1-634500801455'
    
    file=s3.get_object(Bucket=BUCKET,Key='np_template_AWS.xlsx')
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=neutron_template.xlsx"}
    )

#If they download data
@application.route('/getPlotCSVneutron',methods=['GET','POST'])
def output_csv_neutron():
        csv=neutron_download
        return Response(csv,mimetype="text/csv", headers={"Content-disposition":"attachment; filename=neutronprobe_data.csv"})
@application.route('/RSdata',methods=['GET','POST'])
def rsupload():
   if 'loggedin' in session:
        Accountname=session['username']
        connection = db.raw_connection()
        cursor=connection.cursor()
        select_stmt_check="SELECT * FROM plantings_inter WHERE Accountname=%(Accountname)s"
        cursor.execute(select_stmt_check,{'Accountname':Accountname})
        account_info_irr = cursor.fetchone()
        
        if account_info_irr != None: #they have entered a planting
            user_plantingname_raw=account_info_irr[1]
            user_plantingname=[user_plantingname_raw]
            return render_template('rsupload.html',plantingname=user_plantingname)

        if account_info_irr == None:
            return render_template('no_planting.html')
       
    # User is not loggedin redirect to login page
   return redirect(url_for('login'))
#If they need a template
@application.route('/gettemplateRS',methods=['GET','POST'])
def get_RS_template():
    #on AWS 
    s3 = boto3.client('s3')
    BUCKET='elasticbeanstalk-us-west-1-634500801455'
    
    file=s3.get_object(Bucket=BUCKET,Key='NDVI-Template-1planting.xlsx')
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=RS_template.xlsx"}
    )

@application.route('/rssubmit',methods=['GET','POST'])
def rs_success():
    #process file 
    if 'loggedin' in session:

        #if the user is logged in, find their planting name/treatment name and populate the dropdown list....
        Accountname=session['username']
        connection = db.raw_connection()
        cursor=connection.cursor()
        select_stmt_check="SELECT * FROM plantings_inter WHERE Accountname=%(Accountname)s"
        cursor.execute(select_stmt_check,{'Accountname':Accountname})
        account_info_irr = cursor.fetchone()
         

        user_plantingname_raw=account_info_irr[1]
            
        file = request.files['file']
        file_path = os.path.join(application.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
    
#        #==========Define our constants============#
        #pull date from their defined entry, right now let's test with this
        user_date=request.form.get('userdate',None)
        year=user_date[:-6]
        conv_date=dt.strptime(user_date,'%Y-%m-%d')
        DOY=conv_date.strftime('%j')
        month=user_date[-5:-3]
  
        new_values=[['x',-0.07184],['y',0.58808],['a',1.00],['b',0.10]]
        df_1=pd.DataFrame(new_values,columns=['Variable','Value'])
        
        old_values=[['x',0.09515],['y',0.60229],['a',1.00],['b',0.10]]
        df_2=pd.DataFrame(old_values,columns=['Variable','Value'])
        
        #==========================================#
        ndvi_raw=pd.read_excel(file)
        
        ndvi_raw.drop(['ID','MEAST','MNORTH','STATION'],axis=1,inplace=True)
        ndvi=ndvi_raw.rename(columns={"SECTION":'ID'})
        
        ndvi_n_long=ndvi[['PLOT','ID','TYPE','LEVEL','_mean','_stdev','_Var']]
        #if date====... to use the new or old values... shoudln't matter moving forward w/submissions
        
        ndvi_n_long['NDVI-N']=(((df_1['Value'][2]-df_1['Value'][3])*(ndvi_n_long['_mean']-df_1['Value'][0]))/(df_1['Value'][1]-df_1['Value'][0]))+df_1['Value'][0]
        
        #pull treatment from planting name
        ndvi_n_long['Treatment']= user_plantingname_raw
        
        
        ndvi_n_x=ndvi_n_long.sort_values(['Treatment','PLOT'])
        
        ndvi_x=ndvi_n_x.groupby(['PLOT','Treatment']).mean()
        ndvi_x.reset_index(level=0,inplace=True)
        ndvi_x.reset_index(level=0,inplace=True)
        ndvi_whole=ndvi_x.drop(['ID','LEVEL'],axis=1)
        
        
        ndvi_whole.reset_index(level=0,inplace=True)
        ndvi_whole=ndvi_whole.drop(['index'],axis=1)
        final_frame=ndvi_whole.rename(columns={'_mean':'NDVI','_stdev':'STDEV','_Var':'Var','PLOT':'Plot'})
        
        final_frame['Date']=user_date
        final_frame['DOY']=DOY
        final_frame['Month']=month
        final_frame['Year']=year
        final_frame['Accountname']=Accountname
        
        

        final_frame['Kcb']=-0.15+2.34*(final_frame['NDVI'])
        
        final_frame['Kc']=-0.15+2.39*(final_frame['NDVI'])
        
       
        ff_frame=final_frame.drop(['STDEV','Var','NDVI-N'],axis=1)
        ff_frame=ff_frame[["Date","DOY","Year","Month","Treatment","Plot","NDVI","Kcb","Kc","Accountname"]]
        
        ff_frame.round(3)

        ff_frame.to_sql(name='RS_Data',con=db,if_exists='append',index=False)


        return render_template('rssuccess.html')    

@application.route('/about',methods=['GET','POST'])
def aboutpage():
    return render_template('about.html')
@application.route('/thanks',methods=['GET','POST'])
def thanks():
    return render_template('thanks.html')
if __name__ == "__main__":
    application.run()
