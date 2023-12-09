// C++ program for demonstrating 
// similaritites 
#include <ctime> 
#include <iostream> 
#include <random> 
using namespace std; 

int main() 
{ 
// Initializing the sequence 
// with a seed value 
// similar to srand() 
std::random_device rseed;
mt19937  rgen_ = std::mt19937(rseed());
std::uniform_int_distribution<int> idist_;
idist_ = std::uniform_int_distribution<int>(0, 999999);

// Printing a random number 
// similar to rand() 
cout << std::to_string(idist_(rgen_)) << '\n'; 
return 0; 
}
