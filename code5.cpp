#include <iostream>
#include <string>

// Folder 5 - C++ test file (code5.cpp)
std::string repeat(const std::string& text, int times) {
    std::string result;
    for (int i = 0; i < times; ++i) {
        result += text;
    }
    return result;
}

int main() {
    std::cout << "Folder 5 - code5.cpp test" << std::endl;
    std::cout << repeat("X", 5) << std::endl;
    return 0;
}


