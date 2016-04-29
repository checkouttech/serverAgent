from bottle import route, run, request 
from bottle import template 
import bottle
from bottle import BaseResponse
from bottle import LocalResponse

#class ResponseClass(bottle):
class ResponseClass(LocalResponse):

    _linksBar = """ 
        <div>
            | <a href="/?json=1&ui=1">Home</a>
            | <a href="/serveragent/confFile?json=1&ui=1">Conf File</a>  
            | <a href="/serveragent/logLineParser?json=1&ui=1">Log Parser</a>  
            | <a href="errorLog?json=1&ui=1">Error Log</a>
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
        lineString.strip()  
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

        
   
    def home(self):

        self.body = self._htmlHeader +  self._linksBar + self._htmlFooter


    def parseLine(self,lineString= ""):
        lineString.strip()  
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


 
    def getImpressionLogLine(self,id=""):
 
        # search for log line 
 
        if ( int(request.query.ui) == 1 ):
            logLine_html_block =  self.getLogLine(id)
            self.content_type = 'text/html; charset=UTF-8'
            self.body = self._htmlHeader +  self._linksBar + logLine_html_block + self._htmlFooter

        elif ( int(request.query.ui) == 0 ):
            parsedLine =  self.getLogLine(id)
            self.content_type = 'text/plain; charset=us-ascii'
            self.body = parsedLine  
        return 0 

     

    def getLogLine(self,id=""):
        id.strip()
        result =""

        if (id):
            result = "the log line should come here" 
        else :
            result = "no such line found"
 
        #print "result " + result 

        contents = """
        <form >
          <input type="hidden" value="1" name="ui"> 
          <input type="hidden" value="0" name="json"> 
          <input type="text" name=id  size="50" rows=4 value=\" """ + str(id) + """  \">
          <input type="submit" value="submit">
        </form>
        </pre>
        </div>

        <div>
        <pre>
        """ +  result + """ \
        </pre>
        </div>
        """

        self.body = self._htmlHeader +  self._linksBar + contents + self._htmlFooter
        


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
    logLine = request.query.logLine
    res = ResponseClass() 
    res.parseLogLine(logLine)
    return res  


@route('/serveragent/confFile')
def confFile():
    res = ResponseClass() 
    res.getFileContents()
    return res  


    




run(host="0.0.0.0", port=28080, debug=True)


