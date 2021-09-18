# This tool imports all vulnerabilities from ICS-CERT
# The vulnerabilities will be classified by vendor and for each vulnerability the exploitability, affected product and vulnerability will be stored in a CSV

import re
from urllib.request import urlopen,Request

def getExploitability(input,link):

	result = "unkown"
	
	# List that indicates unknown (not to be coded as this is default
	# Public exploits may exist that could target this vulnerability.
	
	# List of explicit mentioning of no exploit code
	ne1 = "No known public exploits specifically target this vulnerability"
	ne2 = "No known public exploits specifically target these vulnerabilities"
	ne4 = "No known exploits specifically target this vulnerability."
	ne5 = "No known exploits specifically target these vulnerable components."
	ne7 = "No known exploits specifically target these vulnerabilities."
	ne8 = "No known public exploits specifically target the other"
	ne11 = "No known public exploits have targeted this vulnerability."
	ne12 = "No known exploits are specifically targeting this vulnerability."
	ne16 = "No known public exploits exist that target these vulnerabilities."
	ne20 = "No known publicly available exploit exists"
	ne23 = "No known public exploits specifically target this vulnerability"
	ne25 = "No publicly available exploits are known to specifically target this vulnerability."
	ne26 = "No known public exploit specifically targets this vulnerability."
	ne27 = "No known public exploits specifically target these products"
	ne28 = "No known public exploits specifically target this vulnerability "
	ne31 = "No known public exploits exist that target this vulnerability."
	
	ne10 = "No publicly available exploit is known to exist."
	ne3 = "No publicly available exploits are known to exist for this vulnerability."
	ne13 = "No publicly known exploits specifically target these vulnerabilities"
	ne18 = "No publicly available exploit code is known to exist that specifically targets this vulnerability."
	ne24 = "No publicly known exploits specifically target this vulnerability."
	ne32 = "No publicly available exploits specifically targeting these vulnerabilities are known to exist."
	
	ne15 = "No exploits are known specifically to target this vulnerability."
	ne30 = "No exploits are known that target this vulnerability."
	ne9 = "No exploits are known that specifically target this vulnerability"
	
	ne17 = "Exploits that target these vulnerabilities are not publicly available."
	ne19 = "Exploits that target this vulnerability are not known to be publicly available."
	
	ne6 = "There are currently no publicly known exploits specifically targeting this vulnerability."
	ne29 = "There are currently no known exploits specifically targeting these vulnerabilities."
	ne21 = "There are currently no known exploits specifically targeting this vulnerability."
	ne22 = "ICS-CERT is unaware of any exploits that target this vulnerability."
	ne14 = "Currently, no known exploits are specifically targeting this vulnerability."
	
	
	
	# List of explicit mentioning of exploit code
	e1 = "Public exploits are known to target this vulnerability."
	e11 = "Public exploits are known to target these vulnerabilities."
	e6 = "public exploits are available"
	e12 = "Public exploits are available."
	e8 = "publicly available exploit code is known to exist that targets these vulnerabilities."
	e17 = "Public exploits are known to exist that target these vulnerabilities."
	e27 = "Public exploits are known that target these vulnerabilities."
	e29 = "Public exploits are known that specifically target this vulnerability."
	
	e7 = "Exploits that target this vulnerability are known to be publicly available."
	e2 = "Exploits that target these vulnerabilities are publicly available."
	e10 = "Exploits that target this vulnerability are publicly available."
	e4 = "Exploit code is publicly available for each of the vulnerabilities"
	e5 = "Exploit code is publicly available for these vulnerabilities."
	e15 = "Exploits that target these vulnerabilities exist and are publicly available."
	e16 = "Exploits that target some of these vulnerabilities are known to be publicly available."
	e18 = "Exploit code specifically targeting this vulnerability has been released"
	e22 = "Exploits that target some of these vulnerabilities are publicly availabl"
	e24 = "Exploits that target some vulnerabilities are publicly available."
	e28 = "Exploit code for this vulnerability is publicly available"
	e30 = "Exploit code for this vulnerability has been recently published."
	
	e3 = "An exploit that targets one of these vulnerabilities is publicly available"
	e9 = "An exploit of this vulnerability has been posted publicly."
	e13 = "Publicly released PoC code exists for these vulnerabilities."
	e14 = "Public exploit(s) are known to target these vulnerabilities."
	e19 = "An exploit targeting this vulnerability is publicly available."
	e20 = "This exploit is publicly known and available."
	e21 = "An exploit for this vulnerability is publicly available."
	e23 = "Publicly available exploits are known to specifically target vulnerabilities"
	e25 = "Known exploits are now targeting this vulnerability."
	e26 = "The researcher has publicly released exploits that specifically target these vulnerabilities."
	
	# List of exploit demonstrated but not disclosed
	nde1 = "Exploitation of vulnerabilities has been publicly demonstrated; however, exploit code is not publicly available."
	nde2 = "General exploits are publicly available that utilize this attack vector"
	nde3 = "No known public exploits specifically target this vulnerability, but information regarding this vulnerability has been publicly disclosed."
	nde4 = "No exploit code is known to exist beyond the test code developed by the researcher"
	nde5 = "Detailed vulnerability information is publicly available that could be used to develop an exploit that targets these vulnerabilities."
	nde6 = "Detailed vulnerability information is publicly available that could be used to develop an exploit that targets this vulnerability."
	nde7 = "Proof-of-concept code is expected to be made public by the researcher."
	nde8 = "No known public exploits specifically target this vulnerability; however, common techniques may be used to exploit."
	nde9 = "Exploits that target these vulnerabilities are potentially available"
	nde10 = "Public exploits that target these vulnerabilities may exist."
	
	# Metasploit / easy tool available
	ae1 = "A Metasploit module is publicly available."
	ae2 = "Tools are publicly available that aid in exploiting this cross-site scripting vulnerability."
	ae3 = "Malware and public exploits are known to target this vulnerability."
	ae4 = "Tools are publicly available that could aid in exploiting this"
	
	if input.count(ne32) + input.count(ne31) + input.count(ne30) + input.count(ne29) + input.count(ne28) + input.count(ne27) + input.count(ne26) + input.count(ne25) + input.count(ne24) + input.count(ne23) + input.count(ne22) + input.count(ne21) + input.count(ne20) + input.count(ne19) + input.count(ne18) + input.count(ne17) + input.count(ne16) + input.count(ne15) + input.count(ne14) + input.count(ne13) + input.count(ne12) + input.count(ne11) + input.count(ne10) + input.count(ne9) + input.count(ne8) + input.count(ne7) + input.count(ne6) + input.count(ne1) + input.count(ne2) + input.count(ne3) + input.count(ne4) + input.count(ne5) > 0:
		result = "no"
	elif input.count(ae4) + input.count(ae3) + input.count(ae2) + input.count(ae1):
		result="yes, autoexploit"
	elif input.count(e30) + input.count(e29) + input.count(e28) + input.count(e27) + input.count(e26) + input.count(e25) + input.count(e24) + input.count(e23) + input.count(e22) + input.count(e21) + input.count(e20) + input.count(e19) + input.count(e18) + input.count(e17) + input.count(e16) + input.count(e15) + input.count(e14) + input.count(e13) + input.count(e12) + input.count(e1) + input.count(e2) + input.count(e3) + input.count(e4) + input.count(e5) + input.count(e6) + input.count(e7) + input.count(e8) + input.count(e9) + input.count(e10) + input.count(e11) > 0:
		result = "yes"
	elif input.count(nde10) + input.count(nde9) + input.count(nde8) + input.count(nde7) + input.count(nde6) + input.count(nde5) + input.count(nde4) + input.count(nde3) + input.count(nde2) + input.count(nde1) > 0:
		result = "Partialy"
	else:
		# print(link) #DEBUG
		result = "unkown"
	
	return result

def getCVSS(input,link):
	result = ""
	if(len(re.findall("CVSS",input, re.IGNORECASE)) > 0):
				CVSSOption1 = "CVSS V2 base score of ([0-9]*\.?[0-9])"
				CVSSOption2 = "CVSS v3 ([0-9]*\.?[0-9])"
				CVSSOption3 = "CVSS v3 base score of ([0-9]*\.?[0-9])"
				CVSSregex = CVSSOption1 + "|" + CVSSOption2 + "|" + CVSSOption3
				CVSS = re.findall(CVSSregex,input, re.IGNORECASE)
				for item in CVSS:
					result = max(item)
	else:
		result = "unspecified"
		#print("No CVSS specified for: " + link) #DEBUG

	return result
	

def getAffectedVersions(input,link):
	result = ""
	affectedVersions = ""
	# Versions: Based on website structure, products are in list items after header2. First and last contain generic stuff (so lets remove that). Afterthat clean up the data.
	
	rav1 = "<h2>Affected Products</h2>(.*?)<h2"
	rav2 = "AFFECTED PRODUCTS</h3>(.*?)<h3"
	rav3 = "<h2>AFFECTED PRODUCTS</h2>(.*?)<h2"

	rav = rav1 + "|" + rav2 + "|" + rav3 
	
	affectedVersionsList = re.findall(rav, input)
	for item in affectedVersionsList:
		if(len(re.findall("<li>",max(item), re.IGNORECASE)) > 0):
			affectedVersions = max(item).split("<li>")[1:]
			for itemAV in affectedVersions:
				result = result + itemAV.replace('</li>','').replace('</ul>','') + ";"
		elif(len(re.findall("<li class=\"BodyTextBlack",max(item), re.IGNORECASE)) > 0):
			affectedVersions = max(item).split("<li")[1:]
			for itemAV in affectedVersions:
				result = result + itemAV.replace('</li>','').replace('</ul>','') + ";"
		elif(len(re.findall("<li class=\"MsoListBullet",max(item), re.IGNORECASE)) > 0):
			affectedVersions = max(item).split("<li")[1:]
			for itemAV in affectedVersions:
				result = result + itemAV.replace('</li>','').replace('</ul>','').replace(' class="MsoListBullet">','') + ";"	
		elif(len(re.findall("<li class=\"margin-left: 40px;",max(item), re.IGNORECASE)) > 0):
			affectedVersions = max(item).split("<li")[1:]
			for itemAV in affectedVersions:
				result = result + itemAV.replace('</li>','').replace('</ul>','').replace(' style="margin-left: 40px;">','') + ";"	
		elif(len(re.findall("<p>(.*?)</p>",max(item), re.IGNORECASE)) > 0):
			result = re.findall("<p>(.*?)</p>",max(item), re.IGNORECASE)[0]
		
		# Improve data quality
		g1 = 'class="BodyTextBlack" style="margin: 6pt 0in;">'
		g2 = '<ul style="margin-left: 40px;">'
		g3 = "</p>"
		g4 = "<p>"
		g5 = "<ul>"
		g6 = '<font face="Times New Roman"><font face="Times New Roman">'
		g7 = "</font></font>;"
		g8 = '<p class="red_title">>'
		g9 = '<h4>'
		g10 = "</h4>"
		g11 = '<p class="red_title">><strong>3</strong><strong> --------</strong>From CIMPLICITY 6.1 forward, users have been advised that S90 drivers were no longer supported and an alternate tool was provided. CIMPLICITY 9.5 removed the drivers from the product.<p class="red_title"><strong>--------- End Update A Part 1 of 3 ----------</strong>'
		g12 = '<ul style="list-style-type:circle">'
		g17 = '<ul style="list-style-type:circle;">'
		g13 = '<h3 style="color:red;">></h3>'
		g14 = '<div class="red_title"><strong>--------- End Update C Part 1 of 2 ---------</strong></div>'
		g15 = '<h3 class="red_title">></h3>'
		g16 = '<div class="red_title"><strong>--------- End Update A Part 2Â of 4Â ---------</strong></div>'
		g19 = '<div class="red_title"><strong>--------- End Update A Part 3 of 5 --------</strong></div>'
		g18 = '<h3 style="color: red;">></h3>'
		g20 = '<h3 style="color:red;">></h3>'
		
		try:
			start = 0
			stop = 0
			if(len(re.findall("<strong>",max(item),re.IGNORECASE)) > 0):
				start = result.find('<strong>')
				stop = result.find('</strong>') + 8
				result = result[:start] + result[stop:]
		
			if(len(re.findall("<em>",max(item),re.IGNORECASE)) > 0):
				start = result.find('<em>')
				stop = result.find('</em>') + 5
				result = result[:start] + result[stop:]		

			if(len(re.findall('<div class="red_title">',max(item),re.IGNORECASE)) > 0):
				start = result.find('<div class="red_title">')
				stop = result.find('</div>') + 6
				result = result[:start] + result[stop:]		
				
			result = result.replace(g20,'').replace(g19,'').replace(g18,'').replace(g17,'').replace(g16,'').replace(g15,'').replace(g14,'').replace(g1,'').replace(g2,'').replace(g3,'').replace("<br />",';').replace(g4,'').replace(g5,'').replace(g6,'').replace(g7,'').replace(g8,'').replace(g9,'').replace(g10,'').replace(g11,'').replace(g12,'').replace(g13,'')
		except:
			print(link)
			pass
			
	return(result)	


def getVulType(input,link):
	result = ""
	
	# Vuln types are based on CVE types: https://cwe.mitre.org/data/definitions/1008.html
	mitrefile = open("mitredefinitions.source",'r')
	rv = ""
	for line in mitrefile:
		rv = rv + re.escape(line.split(' - (')[0]) + "|"
	
	vulnTypes = re.findall(rv, input, re.IGNORECASE)
	tmpArray = []
	
	
	for v in vulnTypes:
		if (v.strip() and (v.lower() not in tmpArray)):
			tmpArray.append(v.lower())
			result = result + v + ";"
	
	return(result)
	

def mainProgram():
	textfile = open("data.txt", 'r')
	crawler = {'User-Agent': "ICS-Info-Crawler"}
	#fullList = urlopen(Request(url="https://ics-cert.us-cert.gov/advisories-by-vendor", headers=crawler)).read().decode('ISO-8859-1')
	#vendorChunk = str(((fullList.split('<div class="view-content">')[1]).split('</div></section>')[0]).encode("utf-8","ignore"))
	
	staticURL = "https://www.us-cert.gov/ics/advisories-by-vendor?page="
	currentVendor = ""
	advisories = ""
	link = ""
	product = ""
	CVSS = ""
	exploitability = ""
	versions = ""
	vultypes = ""
	result = ""
	
	for x in range(0, 12):
		tmpUrl = staticURL + str(x)

		tmpList = urlopen(Request(url=tmpUrl, headers=crawler)).read().decode('ISO-8859-1')
		tmpVendors = tmpList.split('<div class="view-content">')[1].split('<nav class="pager-nav text-center"')[0].replace('<div class="item-list">','').split('<h3>')
		
		
		for tmpVendor in tmpVendors:
			currentVendor = tmpVendor.split("</h3>")[0]
			advisories = re.findall("<a href=\"(.*)</a>", tmpVendor)
			
			for advisory in advisories:
				tmpLinkProduct = "https://www.us-cert.gov/" + advisory.replace('" hreflang="en','')
				link = tmpLinkProduct.split(">")[0].replace('"','')
				product = tmpLinkProduct.split(">")[1]
				vulnerabilityDetails = urlopen(Request(url=link, headers=crawler)).read().decode('ISO-8859-1')
				
				CVSS = getCVSS(vulnerabilityDetails, link)
				exploitability = getExploitability(vulnerabilityDetails, link)
				versions = getAffectedVersions(vulnerabilityDetails, link)
				vultypes = getVulType(vulnerabilityDetails,link)
			
				result = str(currentVendor).replace(',','') + "," + str(link).replace(',','')  + "," + str(CVSS).replace(',','')  + "," + str(exploitability).replace(',','')  + "," + str(versions).replace(',','')  + "," + str(vultypes).replace(',','')
			
				print(result.encode("utf-8","ignore"))	

# Main program
print("Vendor, product, advisoryLink,CVSS, public exploit, affected versions, vulnerability type")
mainProgram()

