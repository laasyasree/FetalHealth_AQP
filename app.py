from flask import Flask, render_template, request, g, request, redirect, url_for, session
from ml_test import *
import pickle
import pandas as pd
#this onwards
import psycopg2


app = Flask(__name__)

links=()
# global links
links = ["home","about","team","work","query","contact"]
@app.route("/")
def hello_world():
    global links
   # links = ["home","about","team","work","query","contact"]
    return render_template("index.html", anchor=links)

@app.route("/queries")
def queries():
   # l=["query"]
    return render_template("index.html", anchor=links, c=len(links) )

'''
  
sql = CREATE TABLE Table1(
   baseline_value                                         NUMERIC(5,1) NOT NULL 
  ,accelerations                                          NUMERIC(5,3) NOT NULL
  ,fetal_movement                                         NUMERIC(5,3) NOT NULL
  ,uterine_contractions                                   NUMERIC(5,3) NOT NULL
  ,light_decelerations                                    NUMERIC(5,3) NOT NULL
  ,severe_decelerations                                   NUMERIC(5,3) NOT NULL
  ,prolongued_decelerations                               NUMERIC(5,3) NOT NULL
  ,abnormal_short_term_variability                        NUMERIC(4,1) NOT NULL
  ,mean_value_of_short_term_variability                   NUMERIC(3,1) NOT NULL
  ,percentage_of_time_with_abnormal_long_term_variability NUMERIC(4,1) NOT NULL
  ,mean_value_of_long_term_variability                    NUMERIC(4,1) NOT NULL
  ,histogram_width                                        NUMERIC(5,1) NOT NULL
  ,histogram_min                                          NUMERIC(5,1) NOT NULL
  ,histogram_max                                          NUMERIC(5,1) NOT NULL
  ,histogram_number_of_peaks                              NUMERIC(4,1) NOT NULL
  ,histogram_number_of_zeroes                             NUMERIC(4,1) NOT NULL
  ,histogram_mode                                         NUMERIC(5,1) NOT NULL
  ,histogram_mean                                         NUMERIC(5,1) NOT NULL
  ,histogram_median                                       NUMERIC(5,1) NOT NULL
  ,histogram_variance                                     NUMERIC(5,1) NOT NULL
  ,histogram_tendency                                     NUMERIC(4,1) NOT NULL
  ,fetal_health                                           NUMERIC(3,1) NOT NULL
);
  
  
CREATE TABLE Table2(
   Features    VARCHAR(536) NOT NULL
  ,Coefficient VARCHAR(440) NOT NULL
);

cur.execute(coeff_dataset)
for i in cur.fetchall():
    print(i)

'''

@app.route("/query1",methods=['POST','GET'])
def query1():
    
    from ast import literal_eval
    import ast
    
    conn = psycopg2.connect(database="postgres",
                        user='postgres', password='Srilu@7410', 
                        host='localhost', port='5432')
  
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute('select * from Table1;')
    df = pd.read_sql_query("SELECT * from Table1", conn)
    cur.execute('select * from Table2')
    coeff_dataset = pd.read_sql_query("SELECT * from Table2", conn)
    print(coeff_dataset)
    conn.commit()
    
    #UNCOMMENT LITERAL EVAL IN ALL THE QUERIES
    # coeff_dataset['features'] = coeff_dataset['features'].apply(ast.literal_eval)
    # coeff_dataset['coefficient'] = coeff_dataset['coefficient'].apply(ast.literal_eval)
        
    

    print(coeff_dataset['features'])

    print(coeff_dataset['coefficient'])

    cf_features = coeff_dataset['features']  #model data features
    print(cf_features)
    #cf_features
    global val
    cf_coffs=coeff_dataset['coefficient'] #model data coefficients
    dfeatures=request.form['features']
    dfeatures=list(dfeatures.split(','))  #user input
    val=request.form['values'] #values of the inputed features
    x=df.loc[:, dfeatures] 
    y= df.loc[:, 'fetal_health']
    print(dfeatures)
    print(val)
    print("jj")
    print(cf_features) 
    # a=list(cf_features[0][1:len(cf_features)-2].split(','))
    lngth=len(cf_features)
    pos=0
    cnt=0
    pos=0
    count=0
    for i in range(0,lngth):
        count+=1
        if set(cf_features[i]) == set(dfeatures):
            out1 = existingModel(i,dfeatures,val,cf_coffs)
            print("DontGenerate model")
            pos=i
        else:
            cnt+=1
            print("Generate model")
    if(cnt==lngth): # = check
        out1=generateModel(count,dfeatures,val,x,y,cur,conn)
        
    
    return render_template("query1.html",features=dfeatures,values=val,fet=out1)



@app.route("/query2",methods=['POST','GET'])
def query2():
    from ast import literal_eval
    import ast
    conn = psycopg2.connect(database="postgres",
                        user='postgres', password='Srilu@7410', 
                        host='localhost', port='5432')
  
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('select * from Table1;')
    df = pd.read_sql_query("SELECT * from Table1", conn)
    cur.execute('select * from Table2')
    coeff_dataset = pd.read_sql_query("SELECT * from Table2", conn)
    print(type(coeff_dataset))
    conn.commit()
    # coeff_dataset['features'] = coeff_dataset['features'].apply(ast.literal_eval)

    # coeff_dataset['coefficient'] = coeff_dataset['coefficient'].apply(ast.literal_eval)

    print(coeff_dataset['features'])

    print(coeff_dataset['coefficient'])

    cf_features = coeff_dataset['features']  
    print(cf_features)
    #cf_features
    global val
    cf_coffs=coeff_dataset['coefficient']
    dfeatures=request.form['features']
    val=request.form['values']
    target=request.form['target']
    dfeatures=list(dfeatures.split(','))
    x=df.loc[:, dfeatures]
    y= df.loc[:, target]
    print(dfeatures)
    print(val)
    print("jj")
    print(cf_features) 
    # a=list(cf_features[0][1:len(cf_features)-2].split(','))
    lngth=len(cf_features)
    pos=0
    cnt=0
    pos=0
    count=0
    for i in range(0,lngth):
        count+=1
        if set(cf_features[i]) == set(dfeatures):
            out1 = existingModel2(i,dfeatures,val,cf_coffs)
            pos=i
        else:
            cnt+=1
            print("Generate model")
    if(cnt==lngth):
        out1=generateModel2(count,dfeatures,val,x,y,cur,conn)  
           

    predictTarget(pos,dfeatures,val,target,cf_coffs)
    return render_template("query2.html",features=dfeatures,values=val,t=target,out=out1)

@app.route("/query3",methods=['POST','GET'])
def query3():
    from ast import literal_eval
    import ast
    conn = psycopg2.connect(database="postgres",
                        user='postgres', password='Srilu@7410', 
                        host='localhost', port='5432')
  
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('select * from Table1;')
    df = pd.read_sql_query("SELECT * from Table1", conn)
    cur.execute('select * from Table2')
    coeff_dataset = pd.read_sql_query("SELECT * from Table2", conn)
    print(coeff_dataset)
    conn.commit()
    
    # coeff_dataset['features'] = coeff_dataset['features'].apply(ast.literal_eval)

    # coeff_dataset['coefficient'] = coeff_dataset['coefficient'].apply(ast.literal_eval)

    print(coeff_dataset['features'])

    print(coeff_dataset['coefficient'])

    cf_features = coeff_dataset['features']  
    print(cf_features)
    #cf_features
    global val
    cf_coffs=coeff_dataset['coefficient']
    dfeatures=request.form['features']
    dfeatures=list(dfeatures.split(','))
    val=request.form['values']
    x=df.loc[:, dfeatures]
    y= df.loc[:, 'fetal_health']
    print(dfeatures)
    print(val)
    print("jj")
    print(cf_features) 
    # a=list(cf_features[0][1:len(cf_features)-2].split(','))
    lngth=len(cf_features)
    pos=0
    cnt=0
    pos=0
    count=0
    for i in range(0,lngth):
        if set(cf_features[i]) == set(dfeatures):
            count+=1
            out1 = existingModel(i,dfeatures,val,cf_coffs)
            pos=i
        else:
            cnt+=1
            print("Generate model")
    if(cnt==lngth):
        out1=generateModel(count,dfeatures,val,x,y,cur,conn)  
    if(out1==1):
        c="normal"     
    elif(out1==2):
        c="suspect"
    else:
        c="pathological"
   
    return render_template("query3.html",features=dfeatures,values=val,fet=c)



if __name__ =="__main__":
    app.run(debug=True)