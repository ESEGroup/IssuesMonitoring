#include "MathBox.h"

MathBox::MathBox() {
  clear();
}

void MathBox::add(double value) {
  sum += value;
  counter ++;
}

double MathBox::getAverage() {
  if (counter != 0) {
    return sum / counter;
  }

  return 0;
}

void MathBox::clear() {
  sum = 0;
  counter = 0;
}
