import sys
import os
import re

#Very very basic PHP code analysis tool

def printResults(reg,mcolor,nmcolor,data):
	if(reg.search(data) == None):
		f.write('<td bgcolor="' + nmcolor + '">X</td>')
	else:
		f.write('<td bgcolor="' + mcolor + '">' + str(len(reg.findall(data))) + '</td>')

def analyseFile(inpFile):
        fd = open(inpFile,'r')
        data = fd.read()
        fd.close()
        fd = open(inpFile,'r')
        lineCount = len(fd.readlines())
        fd.close()

        re_direct_access = re.compile("or die\('No direct script access.'\);|or die\('No direct access allowed.'\);")
        re_c_execute = re.compile("system\(|exec\(|passthru\(|pcntl_exec\(|shell_exec\(")
        re_upload = re.compile("\$\_FILES")
        re_write = re.compile("echo|print|Arr::get",re.IGNORECASE)
        re_write_filter = re.compile("htmlspecialchars|specialchars", re.IGNORECASE)
        re_wget = re.compile("wget|fopen", re.IGNORECASE)
        re_phpinfo = re.compile("phpinfo\(",re.IGNORECASE)

        f.write('<tr><td>' + inpFile + '</td>')

        printResults(re_direct_access,"green","red",data)
        printResults(re_c_execute,"red","green",data)
        printResults(re_upload,"red","green",data)
        printResults(re_write,"yellow","green",data)
        printResults(re_write_filter,"green","yellow",data)
        printResults(re_wget,"red","green",data)
        printResults(re_phpinfo,"red","green",data)

        f.write('<td>')
        f.write(str(lineCount))
        f.write('</td>')
        f.write('</tr>')

def process(dir):
        baseDir = dir
        subDirList = []
        for item in os.listdir(dir):
                if os.path.isfile(os.path.join(baseDir,item)):
                         if(len(item) > 4):
                                if(it         analyseFile(baseDir + "/" + item)
                else:
                         if((item != "modules") and (item != "test") and (item != "system")):
                                subDirList.append(os.path.join(baseDir, item))
        for subdir in subDirList:
                 process(subdir)
em[-4:] == ".php"):
                               

# Preprocess
f = open('output.html','w')
f.write('<html><head><title>Analysis</title></head><body>')
f.write('<h1>Static php source code analyser</h1><hr>')
f.write('1=Direct access,')
f.write('2=command execution')
f.write('3=$_FILES, 4=writeToScreen,5=specialchars,6=wget/fopen,7=phpinfo')
f.write('7=lineCount')
f.write('<hr><table>')
f.write('<tr><td>File</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr>')
# main

process('scadir')
f.write('</table></body><html>')
f.close()
