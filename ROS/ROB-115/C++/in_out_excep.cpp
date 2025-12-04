#include <iostream>
#include <string>
using namespace std;

void checkint(string str)
{
    for (char i : str)
        if (isdigit(i) == false)
            throw 1;
}

string getinput()
{
    string userinput;
    cout << "Please enter an Integer" << endl << "      :";
    cin >> userinput;
    checkint(userinput);
    return userinput;
}

int main()
{
    try
    {
        string xstr = getinput();
        string ystr = getinput();
        int x = stoi(xstr);
        int y = stoi(ystr);
        int z = x + y;
        cout << "  " << x << " + " << y << " = " << z << endl;
    }
    catch(int e)
    {
        cout << "COME ON MAN" << endl;
        main();
    }
    return 0;
}