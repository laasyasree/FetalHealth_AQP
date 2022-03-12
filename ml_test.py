#from app import * ##1now
def existingModel(pos,dfeatures,val,cf_coffs):
        cfdt=cf_coffs[pos]
        # val=input("Enter values:")
        val=val.split(',')
        out=0.0
        for i in range (0,len(cfdt)): #cfdt inside len
            out=out+float(val[i])*(cfdt[i])
        print("Target value:",out)
        if (out<=1):
            out=1
        elif (out>1) & (out<=2):
            out=2
        elif (out>2) & (out<=3):
            out=3
        print("target = ", out)
        return out

#------------------------------------------------------
def generateModel(count,dfeatures,fval,x,y,cur,conn):
  from sklearn.model_selection import train_test_split  
  x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.2, random_state=0) 
  #Fitting the MLR model to the training set:  
  from sklearn.linear_model import LinearRegression  
  regressor= LinearRegression()  
  regressor.fit(x_train, y_train) 
  cf=regressor.coef_
  print(cf)
  cf=cf.tolist()
  print("cf after creating list",cf)
  type(cf)
  print("Calculate fetal health")
  #fnew=input("Enter features:")
  #fcolname=fnew.split(',')
  #fval=input("Enter value:")
  fval=fval.split(',')
  yfh=0.0
  out=0.0
  for i in range(0, len(cf)):
    yfh+=cf[i]*(float(fval[i]))
  if (yfh>0) & (yfh<=1):  #<1 normal coz v are getting neg values
    yfh=1
  elif (yfh>1) & (yfh<=2):
    yfh=2
  elif (yfh>2) & (yfh<=3):
    yfh=3
  print("Fetal health = ", yfh)
  out=yfh #output variable to return to main
  row=[dfeatures,cf]
  #query = ("""insert into Table2 (Features, Coefficient) 
        # values (?,?)""",(dfeatures,cf))
  i1=count #position to insert new list  #(index, Features, Coefficient) 
  print("the value of i1 is",i1)
  #cur.execute("""insert into Table2 
   #      values (?,?,?)""",(i1,str(dfeatures),str(cf)))  #insert query portion
  
  cur.execute('INSERT INTO Table2 VALUES (%s, %s)',(dfeatures, cf))
  conn.commit()
  cur.execute('Select* from Table2')
  res=cur.fetchall() #till print is for printing the table2 it is printing but not saved in table or db.
  print("Updated table")
  for ires in res:
      print(ires)
      print("\n")
  #conn.commit()

  return yfh
  

#------------------------------------------------------


def existingModel2(pos,dfeatures,val,cf_coffs):
        cfdt=cf_coffs[pos]
        # val=input("Enter values:")
        val=val.split(',')
        out=0.0
        for i in range (0,len(cfdt)): #cfdt inside len
            out=out+float(val[i])*(cfdt[i])
        print("Target value:",out)
        # if (out<=1):
        #     out=1
        # elif (out>1) & (out<=2):
        #     out=2
        # elif (out>2) & (out<=3):
        #     out=3
        # print("target = ", out)
        return out


#--------------------------------------
def generateModel2(count,dfeatures,fval,x,y,cur,conn):
  from sklearn.model_selection import train_test_split  
  x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.2, random_state=0) 
  #Fitting the MLR model to the training set:  
  from sklearn.linear_model import LinearRegression  
  regressor= LinearRegression()  
  regressor.fit(x_train, y_train) 
  cf=regressor.coef_
  print(cf)
  cf=cf.tolist()
  print("cf after creating list",cf)
  type(cf)
  print("Calculate fetal health")
  #fnew=input("Enter features:")
  #fcolname=fnew.split(',')
  #fval=input("Enter value:")
  fval=fval.split(',')
  yfh=0.0
  out=0.0
  for i in range(0, len(cf)):
    yfh+=cf[i]*(float(fval[i]))
  
  out=yfh #output variable to return to main
  row=[dfeatures,cf]
  #query = ("""insert into Table2 (Features, Coefficient) 
        # values (?,?)""",(dfeatures,cf))
  i1=count #position to insert new list  #(index, Features, Coefficient) 
  print("the value of i1 is",i1)
  cur.execute('INSERT INTO Table2 VALUES (%s, %s)',(dfeatures, cf))
  
  conn.commit()
  #cur.execute('INSERT INTO Table2 VALUES (%s, %s)',(dfeatures, cf))
  cur.execute('Select* from Table2')
  res=cur.fetchall() #till print is for printing the table2 it is printing but not saved in table or db.
  print("Updated table")
  for ires in res:
      print(ires)
      print("\n")
  #conn.commit()

  return yfh
#---------------------------------------
import ast
from ast import literal_eval

def predictTarget(pos,dfeatures,val,target,cf_coffs):
    cfdt=cf_coffs[pos]
    cfdt=cfdt[1:-1].split(',')
    val=val.split(',')
    out=0.0
    for i in range (0,len(cfdt)): #cfdt inside len
        out=out+float(val[i])*(float(cfdt[i]))
    print("Target value:",out)
    return out