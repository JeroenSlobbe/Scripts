#!/usr/bin/perl
# Description: This script searches for common used alliases like all and people etc.
# Dependencies: Needs file with mail alliases in same directory: common_aliases.txt
use Net::SMTP;
if ($ARGV[0] ne "")
{
	$smtp = Net::SMTP->new($ARGV[0],Hello => '',Timeout => 6000);
	$counter=0;
	open (DIRS, "common_aliases.txt") || die "File common_aliases.txt not found";
	while($addres = )
	{
			if($counter == 20)
			{
				$smtp = Net::SMTP->new($ARGV[0],Hello => '',Timeout => 6000);
				$counter = 0;
			}
			$vrfy = $smtp->verify($addres);
			if($vrfy eq "1")
			{
				print "Found: $addres";
				$smtp = Net::SMTP->new($ARGV[0],Hello => '',Timeout => 6000);
			}
			else
			{
				if($ARGV[1] eq "true")
				{
					print "Not found: $addres errorcode: $vrfy\n";
				}
			}
			$counter++;
	}
}
else
{
	print "This script tries to find common used mail adresses\n";
	print "Example: smtpenum  Optional: ";
}
