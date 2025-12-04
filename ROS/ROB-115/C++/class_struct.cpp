#include <iostream>
using namespace std;

class Robot
{
public:
    Robot(string name) : robot_name(name)
    {
        for (int i = 0; i < 9; i++)
        {
            numbers[i] = i + 1;
        }
    }

    void print_numbers()
    {
        //print the array in one line
        cout << "Array Elements: ";
        for (auto num : numbers)
        {
            cout << num << " ";
        }
        cout << endl;

        // print each element with index
        for (int i = 0; i < 9; i++)
        {
            cout << "index[" << i << "] = " << numbers[i] << endl;
        }
    }

    void introduce()
    {
        string user_name;
        cout << "Enter your name:";
        //cin.ignore();
        getline(cin, user_name);
        //cing >> user_name;
        cout << "Hello " << user_name << ", I am " << robot_name << " the robot." << endl;
    }

private:
    string robot_name;
    int numbers[9];
};

// define a struct
struct Task
{
    string description;

    void perform()
    {
        cout << "Performing task: " << description << endl;
    }
};

int main()
{
    // create an instance of the class
    Robot my_robot("Rufus");
    Robot other_robot("Robert");

    // call the methods of the object
    cout << "======================" << endl;
    my_robot.introduce();
    cout << "======================" << endl;
    my_robot.print_numbers();
    cout << "======================" << endl;
    other_robot.introduce();
    cout << "======================" << endl;
    cout << "======================" << endl;
    cout << "======================" << endl;

    // create a task instance
    Task my_task = {"pick somethin up"};
    // call the method
    my_task.perform();

    return 0;
}