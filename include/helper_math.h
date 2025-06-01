#ifndef HELPER_MATH_H
#define HELPER_MATH_H

#include <math.h>

// Create the base types

typedef struct {
    double x, y, z;
} Vector;

typedef struct {
    double w, i, j, k;
} Quaternion;

typedef struct {
    double xx, xy, xz;
    double yx, yy, yz;
    double zx, zy, zz;
} Matrix;

// Define the operations

// Matrix ops
Matrix matmul(Matrix m, Matrix n); // Apply m to n

// Vector ops
Vector vcross(Vector u, Vector v); // u x v
double vdot(Vector u, Vector v);
Vector vadd(Vector u, Vector v);
Vector vsubtract(Vector u, Vector v);
Vector vscale(double scalar, Vector v);
Vector vmatmul(Matrix m, Vector v); // m transforms v
double vmag(Vector v);
void vunit(Vector *v);

// Interoperability between vector and quaternion
Quaternion vtoq(Vector v); // zero real part quat
Vector qtov(Quaternion q); // cut off real, extract vector part
Matrix qtorot(Quaternion q); // compute rotation matrix from quaternion
Vector qrotate_vector(Quaternion q, Vector v);

// Quaternion ops
double qmag(Quaternion q); // get mag of quaternion
Quaternion qrotate_quaternion(Quaternion p, Quaternion q); // apply p to q
Quaternion qconj(Quaternion q); // get conjugate quaternion, inverts signs of imaginary parts only
void qunit(Quaternion *q);

#endif