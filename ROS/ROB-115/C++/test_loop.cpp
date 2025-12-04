#include <iostream>
#include <string>
#include <vector>
using namespace std;

//check if number or string
// void check_number(string str) 
// {
// 	for (char i : str)
//         cout << i << endl;
// }

// int main()
// {
//     int my_array[] = {1,2,3,4,5,6,6,4,6};
//     for (auto i: my_array)
//         cout << i << endl;

//         return 0;
// }

int main() {
    vector<int> my_vector = {1,2,3,4,5,6,6,4,6};

    // Loop through elements using range-based for loop
    for (auto i : my_vector)
        cout << i << endl;

    // Adding an element dynamically
        cout << "============================="<< endl;
        // push_back(value)	Adds an element to the end
        // pop_back()	Removes the last element
        // size()	Returns the number of elements
        // clear()	Removes all elements
        // at(index)	Accesses element safely with bounds checking
        cout << "============================="<< endl;

    my_vector.push_back(10);  

    cout << "After adding 10:" << endl;

    for (auto i : my_vector)
        cout << i << endl;

    return 0;
}