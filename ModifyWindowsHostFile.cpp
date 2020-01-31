#include <fstream>;
#include <iostream>;
#include <Windows.h>;

using namespace std;

BOOL IsProcessElevated()
{
	BOOL fIsElevated = FALSE;
	HANDLE hToken = NULL;
	TOKEN_ELEVATION elevation;
	DWORD dwSize;

	if (!OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &hToken))
	{
		printf("\n Failed to get Process Token :%d.", GetLastError());
		goto Cleanup;  // if Failed, we treat as False
	}


	if (!GetTokenInformation(hToken, TokenElevation, &elevation, sizeof(elevation), &dwSize))
	{
		printf("\nFailed to get Token Information :%d.", GetLastError());
		goto Cleanup;// if Failed, we treat as False
	}

	fIsElevated = elevation.TokenIsElevated;

Cleanup:
	if (hToken)
	{
		CloseHandle(hToken);
		hToken = NULL;
	}
	return fIsElevated;
}

int main(int argc, char** argv)
{
	/* Check if we get an IP and a Hostname*/
	if (argc < 3)
	{
		std::cout << "Syntax: ModifyHostFile [ip-address] [hostname]";
		return 1;
	}
	else
	{
		/* Ensure program is running with administrator rights*/
		if (IsProcessElevated())
		{
			string line = string(argv[1]) + " " + string(argv[2]) + "\n";
			ofstream f("C:\\Windows\\System32\\drivers\\etc\\hosts", std::ios_base::app);
			f << line;
			f.close();
			std::cout << "Added line to windows hosts file!\n";
		}
		else
		{
			std::cout << "This program requires Administrator rights as it's modifying the windows host file \n";
		}
	}
}
