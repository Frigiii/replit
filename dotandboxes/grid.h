#pragma once

#include <array>
#include <stdexcept>
#include <vector>
#include <iostream>

// NOTE: You do not need to understand this code in order to
// work on your solution, but feel free to snoop around if
// you are interested.

class Grid {
public:
    int steps = 0;

    Grid(int numRows, int numCols) : mNumRows(numRows), mNumCols(numCols) {
        mFields.resize(numRows * numCols, ' ');
        mVertical.resize(numRows * (numCols + 1), {false});
        mHorizontal.resize((numRows + 1) * numCols, {false});
    }
    
    Grid(const Grid& g) : mNumRows(g.numRows()), mNumCols(g.numCols()){
        mFields = std::vector<char>(g.mFields);
        mVertical = std::vector<boolWrap>(g.mVertical);
        mHorizontal = std::vector<boolWrap>(g.mHorizontal);
    }
    
    // Get number of rows
    int numRows() const {
        return mNumRows;
    }
    
    // Get number of columns
    int numCols() const {
        return mNumCols;
    }
    
    // Access a token field
    char& fields(int row, int col) {
      if (row < 0 || row >= mNumRows || col < 0 || col >= mNumCols) {
          throw std::runtime_error{"Invalid board position."};
      }
      return mFields[row * mNumCols + col];
    }
    
    // Access a field for vertical lines
    bool& vertical(int row, int col) {
      if (row < 0 || row >= mNumRows || col < 0 || col > mNumCols) {
          throw std::runtime_error{"Invalid board position."};
      }
      return mVertical[row * (mNumCols + 1) + col].value;
    }
    
    // Access a field for horizontal lines
    bool& horizontal(int row, int col) {
      if (row < 0 || row > mNumRows || col < 0 || col >= mNumCols) {
          throw std::runtime_error{"Invalid board position."};
      }
      return mHorizontal[row * mNumCols + col].value;
    }
    
    // Print the game state
    void printGrid() {
        // Avoid unnecessary computations when no need to adjust the output to the number lengths
        if (mNumRows < 10 && mNumCols < 10) {
          
            std::cout << "Step #" << ++steps << '\n';
            std::cout << "  ";
            for (int col = 0; col <= mNumCols; ++col) {
                std::cout << col << ' ';
            }
            std::cout << '\n';
            for (int row = 0; row < mNumRows; ++row) {
                std::cout << row << ' '; 
                for (int col = 0; col < mNumCols; ++col) {
                    std::cout << '.' << (mHorizontal[row * mNumCols + col].value ? "—" : " ");
                }
                std::cout << ".\n  ";
                for (int col = 0; col < mNumCols; ++col) {
                    std::cout << (mVertical[row * (mNumCols + 1) + col].value ? '|' : ' ')
                              << mFields[row * mNumCols + col];
                }
                std::cout << (mVertical[row * (mNumCols + 1) + mNumCols].value ? '|' : ' ') << '\n';
            }
            std::cout << mNumRows << ' ';  
            for (int col = 0; col < mNumCols; ++col) {
                std::cout << '.' << (mHorizontal[mNumRows * mNumCols + col].value ? "—" : " ");
            }
            std::cout << ".\n";
            
        } else {
        
            int rowDigits = getDigits(mNumRows);
            int colDigits = getDigits(mNumCols);
            
            std::cout << "Step #" << ++steps << '\n';
            for (int posc = colDigits - 1; posc >= 0; --posc) {
                for (int posr = rowDigits + 1; posr > 0; --posr) {
                    std::cout << ' ';
                }
                for (int col = 0; col <= mNumCols; ++col) {
                    printDigit(col, posc);
                    std::cout << ' ';
                }
                std::cout << '\n';
            }
            for (int row = 0; row < mNumRows; ++row) {
                for (int posr = rowDigits - getDigits(row); posr > 0; --posr) {
                    std::cout << ' ';
                }
                std::cout << row << ' '; 
                for (int col = 0; col < mNumCols; ++col) {
                    std::cout << '.' << (mHorizontal[row * mNumCols + col].value ? "—" : " ");
                }
                std::cout << ".\n ";
                for (int posr = rowDigits; posr > 0; --posr) {
                    std::cout << ' ';
                }
                for (int col = 0; col < mNumCols; ++col) {
                    std::cout << (mVertical[row * (mNumCols + 1) + col].value ? '|' : ' ')
                              << mFields[row * mNumCols + col];
                }
                std::cout << (mVertical[row * (mNumCols + 1) + mNumCols].value ? '|' : ' ') << '\n';
            }
            std::cout << mNumRows << ' ';  
            for (int col = 0; col < mNumCols; ++col) {
                std::cout << '.' << (mHorizontal[mNumRows * mNumCols + col].value ? "—" : " ");
            }
            std::cout << ".\n";
            
        }
    }

private:

    // Helper function to get the number of digits in a number:
    // used for printing the board when width or height >= 10
    int getDigits(int n) {
        if (n < 10) {
            return 1;
        } else {
            int ctr = 0;
            while (n > 0) {
                n /= 10;
                ++ctr;
            }
            return ctr;
        }
    }
    
    // Used for printing column numbers vertically when width >= 10
    void printDigit(int n, int pos) {
      if (pos == 0) {
          std::cout << n % 10;
      } else {
          int e = 1;
          while (pos > 0) {
              e *= 10;
              --pos;
          }
          if (n / e == 0) std::cout << ' ';
          else std::cout << n / e % 10;
      }
    }

    // std::vector<bool> works different from other std::vectors
    // A wrapper enables usual std::vector functionality
    struct boolWrap {
        bool value;
    };
    
    int mNumRows;
    int mNumCols;
    std::vector<char> mFields;
    std::vector<boolWrap> mVertical;
    std::vector<boolWrap> mHorizontal;
    
};

#ifdef GRID_EXTERN
extern Grid grid;
#else
Grid grid{2, 2};
#endif