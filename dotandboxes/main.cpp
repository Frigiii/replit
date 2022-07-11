#include "grid.h"
#include <iostream>

// change row and col to receive real Fun ;)
const int row_global = 1000;
const int col_global = 1000;


Grid customGrid(row_global, col_global);


// Check if no more tokens can be placed
bool isGridFull() {
    for (int row = 0; row < row_global - 1; ++row) {
        for (int col = 0; col < col_global - 1; ++col) {
            if (customGrid.fields(row, col) == ' ') {
                return false;
            }
        }
    }
    return true;
}

//counts each players points
int countfields(char player){ 
  int count = 0;
  for (int row = 0; row < row_global - 1; ++row) {
        for (int col = 0; col < col_global -1; ++col) {
            if (customGrid.fields(row, col) == player) {
                ++count;
            }
        }
    }
  return count;
}

//Place a vertical or horizontal line, depending on direction
void drawLine(int row, int col, char direction) {
  
  if(direction == 'd'){
    customGrid.vertical(row, col) = true;
  } else {
    customGrid.horizontal(row, col) = true;
  }
}

//checks wether the input is in a valid range or not
bool validInput(int row, int col, char direction){
  if (direction == 'd'){
    if (row >= 0 && row < row_global - 1 && col >= 0 && col < col_global ) {
      return true;
    }
  } else if (direction == 'r'){
    if (col >= 0 && col < col_global - 1 && row >= 0 && row < row_global) {
      return true;
    }
  } 
  return false;
}

//Does adding a line result in drawing an unclaimed box?
bool shouldPlaceToken(int row, int col) {
  
  if (customGrid.fields(row, col) != ' ' || customGrid.vertical(row, col) == false || customGrid.horizontal(row, col) == false || customGrid.vertical(row, col + 1) == false || customGrid.horizontal(row + 1, col) == false) {
    return false;
  } else {
    return true;
  }
}

//place a Token
bool placeToken(char player){
  bool set = false;
   for (int row = 0; row < row_global - 1; ++row) {
        for (int col = 0; col < col_global - 1; ++col) {
            if (shouldPlaceToken(row, col)) {
                customGrid.fields(row, col) = player;
                set = true;
            }
        }
    }
  return set;
}

//print the Grid
void printGrid_special(int lap){
  std::cout << "Step #" << lap << std::endl;
  if (row_global > 10){
    std::cout << ' '; //correct the print of the grid for 10-99 rows
  }
  for (int row = 0; row <= col_global; ++row){
    if(row){
      std::cout << row - 1;
    } else {
      std::cout << ' ';
    }
    std::cout << ' ';
  }
  std::cout << std::endl;
  for (int row = 0; row < 2 * row_global - 1; ++row){
    for (int col = 0; col < 2 * col_global + 2; ++col){
      if(row%2){
          if (col == 0 && row_global > 10){
            std::cout << ' '; // correct the print of the grid for 10-99 rows
          }
          if (col == 0 || col == 1){
            std::cout << ' ';
          } else if (col % 2) {
            if (col == col_global * 2 + 1){
              std::cout << "\n";
            } else {
              std::cout << customGrid.fields(row / 2, (col - 3) / 2);
            }
          } else {
            if (customGrid.vertical(row / 2, (col - 2) / 2) == true){
              std::cout << '|';
            } else {
              std::cout << ' ';
            }
          }
        
      } else {
        if (col == 0){
          std::cout << row / 2;
          if (row_global > 10 && row < 20 ){
              std::cout << ' '; //correct the print of the grid for 10-99 rows
          }
        } else if (col == 1){
          std::cout << ' ';
        } else if (col % 2){
          if (col == col_global * 2 + 1){
            std::cout << "\n";
          } else {
            if (customGrid.horizontal(row / 2, (col - 3) / 2) == true){
              std::cout << "—";
            } else {
              std::cout << ' ';
            }
          }
        } else {
          std::cout << '.';
        }
      }
    }
  }
  std::cout << std::endl;
}

int main() {
  int row, col;
  char direction;
  char player = 'A';
  bool occupied;
  int lap = 1;
  
  printGrid_special(lap);
  
  while (!isGridFull()){
    
    do {
      std::cin >> row >> col >> direction;
      
      if (direction == 'u'){ //convert u to d and l to r to save lines :)
        --row;
        direction = 'd';
      } else if (direction == 'l'){
        --col;
        direction = 'r';
      }
      
      occupied = false;
      
      if (validInput (row, col, direction)) {
        if((direction == 'd' && customGrid.vertical(row, col) == true) || (direction == 'r' && customGrid.horizontal(row, col) == true )){
        std::cout << "Invalid move!" << std::endl;
        occupied = true;
        }
        drawLine (row, col, direction);
      } else {
        std::cout << "Invalid move!" << std::endl;
        occupied = true;
      }
      
    } while (occupied);
    
    if (placeToken(player) == false){
      if (player == 'A'){
        player = 'B';
      } else {
        player = 'A';
      }
    }
    
    ++lap;
    
    printGrid_special(lap); 
  }
 
  if (countfields('A') == countfields('B')){
    std::cout << "Draw!" << std::endl;
  } else if (countfields('A') > countfields('B')){
    std::cout << "A won!" << std::endl;
  } else {
    std::cout << "B won!" << std::endl;
  }
}