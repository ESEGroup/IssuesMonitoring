#ifndef MATHBOX_H
#define MATHBOX_H

class MathBox {
public:
  MathBox();
  void add(double value);
  double getAverage();
  void clear();

private:
  int counter;
  double sum;
};

#endif // MATHBOX_H
