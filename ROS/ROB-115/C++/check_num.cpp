#include <iostream>
using namespace std;

//check if number or string
bool check_number(string str) 
{
	for (int i = 0; i < str.length(); i++)
		if (isdigit(str[i]) == false)
			return false;
	return true;
}
int main() 
{
	string str = "11sun";
	if (check_number(str))
		cout << str << " is an integer" << endl;
	else
		cout << str << " is a string" << endl;
	str = "1234";
	if (check_number(str))
		cout << str << " is an integer" << endl;
	else
		cout << str << " is a string" << endl;
}