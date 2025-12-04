#include <iostream>
#include <vector>

using namespace std;

// Iterates through the vector using a range-based for loop.
// Preferred when index access is not required for clarity and readability.
void range_based_loop(const vector<int>& my_array) 
{
    for (auto i : my_array)  
        cout << i << " ";  
    cout << endl;
}

// Iterates through the vector using an indexed for loop.
// Useful when index-based operations or modifications are needed.
void standard_loop(const vector<int>& my_array) 
{
    for (size_t i = 0; i < my_array.size(); i++)  
        cout << my_array[i] << " ";  
    cout << endl;
}

int main()
{
    vector<int> my_array = {1, 2, 3, 4, 5, 6, 6, 4, 6};

    range_based_loop(my_array);

    cout << "==============" << endl;

    standard_loop(my_array);

    return 0;
}
