from bottle import route, run, request 
from bottle import template 
import bottle
from bottle import BaseResponse
from bottle import LocalResponse
import json
from voluptuous import Schema, Required, Invalid , MultipleInvalid, All
from voluptuous import *
from collections import OrderedDict

# REMEMBER :  LocalResponse is the subclass of Response class which contains the "body"  variable 
# Therefore it needs to be inherited 
class ResponseClass(LocalResponse):

    _linksBar = """ 
        <div>
            | <a href="/?json=1&ui=1">Home</a>
            | <a href="/serveragent/confFile?json=1&ui=1">Conf File</a>  
            | <a href="/serveragent/logLineParser?json=1&ui=1">Log Parser</a>  
            | <a href="/serveragent/validateschema?json=1&ui=1">Validate Schema</a>
            | <a href="/serveragent/impressionLog?json=1&ui=1">Impression Log</a>
        </div>
    """ 

    _htmlHeader = """
        <HTML>
        <HEAD>
        <TITLE>Hello World With JavaScript</TITLE>
        </HEAD>
        <BODY>
    """

    _htmlFooter = """
        </BODY>
        </HTML>
    """


    _htmlForm   = """
         <div> 
            <form > 
               <input type="hidden" value="1" name="ui"> 
               <input type="hidden" value="0" name="json"> 
               <input type="text" name=id size="50" rows=4 value="[VAR:id]"> 
               <input type="submit" value="submit">  
            </form>  
         </div> 
    """
    
    _htmlResult = """
        <div>
           <pre>
             [VAR:result] 
           </pre>
      </div>
   """
 


    _impression_log_field_names =  ["col1","col2","col3","col4","col5","col6","col7"]

    def __init__(self):
        pass 

 
    def readFile(self,filename= ""):
    
        # read file and if ui set to 1 then return html string 
        fileContents = ""
        with open('/etc/httpd/conf/httpd.conf', 'r') as fileHandle:
            fileContents = fileHandle.read()
    
        if ( int(request.query.ui) == 1 ):
            fileContents_html_block = """
               <div id="list">
               <pre>
               """ + fileContents + """
               </pre>  
               </div>
             """
            return fileContents_html_block 

        return fileContents  


    def getFileContents(self,filename= ""):

        if ( int(request.query.ui) == 1 ):
            fileContents_html_block =  self.readFile(filename)
            self.content_type = 'text/html; charset=UTF-8'
            self.body = self._htmlHeader +  self._linksBar + fileContents_html_block + self._htmlFooter

        elif ( int(request.query.ui) == 0 ):
            fileContents =  self.readFile(filename)
            self.content_type = 'text/plain; charset=us-ascii'
            self.body = fileContents 
        return 0 

    

    def parseLine(self,lineString= ""):
        lineString = lineString.strip()  
        lineValues = lineString.split('^') 
        parsedLine = []
        counter=0 
        for fieldName , fieldValue in zip ( self._impression_log_field_names , lineValues ) :
            counter +=1
            parsedLine.append("%s -- %s -- %s "  % (counter, fieldName, fieldValue)) 


        if ( int(request.query.ui) == 1 ):
            lineValues_html_block = """
                <div>
                <form >
                  <input type="hidden" value="1" name="ui"> 
                  <input type="hidden" value="0" name="json"> 
                  <input type="text" name=logLine  size="50" rows=4 value='""" + lineString + """'>
                  <input type="submit" value="submit">
                </form>
                </div>
                <div>
                <pre> 
                """ + '\n' + '\n'.join(parsedLine) + """
                </pre>
                </div>
                """
            return lineValues_html_block

        return '\n'.join(parsedLine)


    def parseLogLine(self,logLine=""):

        if ( int(request.query.ui) == 1 ):
            parsedLine_html_block =  self.parseLine(logLine)
            self.content_type = 'text/html; charset=UTF-8'
            self.body = self._htmlHeader +  self._linksBar + parsedLine_html_block + self._htmlFooter

        elif ( int(request.query.ui) == 0 ):
            parsedLine =  self.parseLine(logLine)
            self.content_type = 'text/plain; charset=us-ascii'
            self.body = parsedLine  
        return 0 

   
    def validateSchema(self):
        htmlTextAreaForm = """
         <div> 
            <form > 
             <textarea id="txtArea" rows="10" cols="70"></textarea>  
             At w3schools.com you will learn how to make a website. We offer free tutorials in all web development technologies.
             </textarea> 
             <input type="submit" value="submit">
            </form > 
         </div> 

         """

    '''
data = {
    'address': 'some street',
    'page' : "thisis page",
    'streetAddress' : "this is street address",
    'details' : {
          'paint' : 1
       }
     }
 


my_dictionary=OrderedDict(json.loads(string))
print my_dictionary

print ( json.dumps(my_dictionary , indent = 4 ) )
print '\n'.join(my_dictionary)

    '''




 
    def validateSchema(self,data=""):
       
        listOfErrors = []

        if (data):
            dataDict= json.loads(data, 'latin-1')
            #orderedDataDict = OrderedDict(json.loads(data))
            #print orderedDataDict 
            print dataDict 
    
            schemaTemplate = {
                   Required('address'):   All ( Any(str, unicode), Length(min=1)),
                   'page':                All(int, Range(min=0)),
                   'details' : {
                       'paint' :          All ( Any(str, unicode), Length(min=1))
                    }
                 }
            
            schema = Schema(schemaTemplate, extra=ALLOW_EXTRA) 
             
            try :
                schema (dataDict) 
            except MultipleInvalid as e :
                listOfErrors = sorted(str(i) for i in e.errors)
                print(sorted(str(i) for i in e.errors))
                    

        htmlTextAreaForm = """
         <div> 
             <form action="http://192.168.150.101:28080/serveragent/validateschema?json=1&ui=1" name="confirmationForm"  method="post">
             <textarea id="confirmationText" class="text" cols="86" rows ="20" name="confirmationText">
             """ + data   + """
             </textarea>
             <input type="submit" value="jsonsubmit">
           </form>
         </div> 
        """
        
        if len(listOfErrors) > 0 :
            result = '\n'.join(listOfErrors)
        else :
            result = "All good!!! " 
     
        #htmlResult = """<div>  <pre>  """ + '\n'.join(listOfErrors) + """   </pre>  </div>  """  

        htmlResult = """<div>  <pre>  """ + result + """   </pre>  </div>  """  

        self.body = self._htmlHeader +  self._linksBar + htmlTextAreaForm + htmlResult + self._htmlFooter
        
   
    def home(self):
        self.body = self._htmlHeader +  self._linksBar + self._htmlFooter

 

    def getLogLine(self,id="",responseType="raw"):
        id = id.strip()
        result =""
        matchFlag = False 
        matchedLine = ""  
       
        if (id != ""):
            for line in reversed(open("impression.log").readlines()):
                logLineValues = line.split('^') 
                # if id found then populate content variable 
                if ( logLineValues[0] == id ): 
                     matchFlag = True 
                     matchedLine = line 
                     break 
        else :
            #result = "no such line found"
            result = "id missing in request"

        # TODO 
        if ( responseType == "raw" ) :
            if ( matchFlag ) :
                result = matchedLine 
            else:
                result = "No match found"

        elif ( responseType == "parsed" ):
            if ( matchFlag ) :
                lineValues = matchedLine.split('^')
                parsedLine = []
                counter=0
                for fieldName , fieldValue in zip ( self._impression_log_field_names , lineValues ) :
                    counter +=1 
                    parsedLine.append("%s -- %s -- %s "  % (counter, fieldName, fieldValue))
                result = parsedLine
            else: 
                result = "No match found"
 
        elif ( responseType == "json" ):
            if ( matchFlag ) :
                lineValues = matchedLine.split('^')
                parsedDict = {} 
                parsedDict['data'] = {}
                for fieldName , fieldValue in zip ( self._impression_log_field_names , lineValues ) :
                    parsedDict['data'][fieldName] = fieldValue
                print parsedDict 
                result = parsedDict  
            else: 
                result = "No match found"


 
       # foo - <div>    <form >      <input type="hidden" value="1" name="ui">      <input type="hidden" value="0" name="json">      <input type="text" name=logLine  size="50" rows=4 value='""" + lineString + """'>      <input type="submit" value="submit">    </form>    </div> 
        return result 




    def getImpressionLogLine(self,id=""):
 
        # search for log line 
        result =  self.getLogLine(id)

        if ( int(request.query.ui) == 0 )  and ( int(request.query.json) == 0 ) :
            result =  self.getLogLine(id)
            self.content_type = 'text/plain; charset=us-ascii'
            self.body = result   
      
        elif ( int(request.query.ui) == 1 )  and ( int(request.query.json) == 0 ) :
            result =  self.getLogLine(id,"parsed")
            self.content_type = 'text/html; charset=UTF-8'
            htmlResult = """<div>  <pre>  """ + '\n'.join(result) + """   </pre>  </div>  """  
            htmlForm = self._htmlForm.replace("[VAR:id]",id)  
            self.body = self._htmlHeader +  self._linksBar + htmlForm + htmlResult + self._htmlFooter

        elif ( int(request.query.ui) == 1 )  and ( int(request.query.json) == 1 ) :
            result =  self.getLogLine(id,"json")
            self.content_type = 'text/html; charset=UTF-8'
            htmlResult = """<div>  <pre>  """ +  json.dumps(result , indent=4, sort_keys=True)  + """   </pre>  </div>  """  
            print json.dumps(result , indent=4, sort_keys=True) 
            htmlForm = self._htmlForm.replace("[VAR:id]",id)  
            self.body = self._htmlHeader +  self._linksBar + htmlForm + htmlResult + self._htmlFooter

        elif ( int(request.query.ui) == 0 )  and ( int(request.query.json) == 1 ) :
            result =  self.getLogLine(id,"json")
            self.content_type = 'application/json'
            #htmlResult = """<div>  <pre>  """ +  json.dumps(result , indent=4, sort_keys=True)  + """ \  </pre>  </div>  """  
            print json.dumps(result , indent=4, sort_keys=True) 
            #htmlForm = self._htmlForm.replace("[VAR:id]",id)  
            #self.body = self._htmlHeader +  self._linksBar + htmlForm + htmlResult + self._htmlFooter
            self.body = json.dumps(result , indent=4, sort_keys=True)  


 


        #elif ( int(request.query.ui) == 1 ):
        #    self.content_type = 'text/html; charset=UTF-8'
        #    htmlForm = self._htmlForm.replace("[VAR:id]",id)  




           # htmlResult = """<div>  <pre>  """ + result + """ \  </pre>  </div>  """  
           # self.body = self._htmlHeader +  self._linksBar + htmlForm + htmlResult + self._htmlFooter

            




       # elif ( int(request.query.ui) == 0 ):
       #     self.content_type = 'text/plain; charset=us-ascii'
       #     self.body = result   
        return 0 

     

@route('/')
@route('/serveragent/')
@route('/serveragent/home')
def home():
    res = ResponseClass() 
    res.home()
    return res  


@route('/serveragent/impressionLog')
@route('/serveragent/impressionLog/')
def impressionLogLine():
    id = request.query.id
    res = ResponseClass() 
    res.getImpressionLogLine(id)
    return res  


@route('/serveragent/logLineParser')
def logLineParser():


    print request.method 

    logLine = request.query.logLine
    res = ResponseClass() 
    res.parseLogLine(logLine)
    return res  


@route('/serveragent/confFile')
def confFile():
    res = ResponseClass() 
    res.getFileContents()
    return res  


@route('/serveragent/validateschema', method='GET')
def validateschema():
    res = ResponseClass() 
    res.validateSchema()
    return res  

   

@route('/serveragent/validateschema', method='POST')
def validateschema():
    
    data = request.POST['confirmationText']
    res = ResponseClass() 
    res.validateSchema( data )
    return res  




#@bottle.route('/requestdetails', method='POST')




run(host="0.0.0.0", port=28080, debug=True)

'''
sc = {
       Required('address'):   All(str, Length(min=1)),
       'page':                All(int, Range(min=0)),
       'details' : {
          'paint' :           All(str, Length(min=1))
          }
     }

schema = Schema(sc, extra=ALLOW_EXTRA) 

data = {
    'address': 'some street',
    'page' : "thisis page",
    'streetAddress' : "this is street address",
    'details' : {
          'paint' : 1
       }
     }




try :
    schema (data) 
except MultipleInvalid as e :
    print(sorted(str(i) for i in e.errors))
'''

