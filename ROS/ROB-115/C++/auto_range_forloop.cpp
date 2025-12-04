#include <iostream>
#include <string>
using namespace std;

//check if number or string
void check_number(string str) 
{
	for (char i : str)
        cout << i << endl;
}

int main()
{
    string a = "hello";
    check_number(a);
    return 0;
}