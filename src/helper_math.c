#include "helper_math.h"

Matrix matmul(Matrix m, Matrix n) {
    Matrix result = {
        .xx = (m.xx * n.xx + m.xy * n.yx + m.xz * n.zx),
        .xy = (m.xx * n.xy + m.xy * n.yy + m.xz * n.zy),
        .xz = (m.xx * n.xz + m.xy * n.yz + m.xz * n.zz),

        .yx = (m.yx * n.xx + m.yy * n.yx + m.yz * n.zx),
        .yy = (m.yx * n.xy + m.yy * n.yy + m.yz * n.zy),
        .yz = (m.yx * n.xz + m.yy * n.yz + m.yz * n.zz),

        .zx = (m.zx * n.xx + m.zy * n.yx + m.zz * n.zx),
        .zy = (m.zx * n.xy + m.zy * n.yy + m.zz * n.zy),
        .zz = (m.zx * n.xz + m.zy * n.yz + m.zz * n.zz)
    };

    return result;
}

Vector vcross(Vector u, Vector v) {
    Vector w = {
        .x = (u.y * v.z - u.z * v.y),
        .y = -(u.x * v.z - u.z * v.x),
        .z = (u.x * v.y - u.y * v.x)
    };

    return w;
}

double vdot(Vector u, Vector v) {
    return (u.x * v.x + u.y * v.y + u.z * v.z);
}

Vector vadd(Vector u, Vector v) {
    Vector w = {
        .x = (u.x + v.x),
        .y = (u.y + v.y),
        .z = (u.z + v.z)
    };

    return w;
}

Vector vsubtract(Vector u, Vector v) {
    Vector w = {
        .x = (u.x - v.x),
        .y = (u.y - v.y),
        .z = (u.z - v.z)
    };

    return w;
}

Vector vscale(double scalar, Vector v) {
    v.x *= scalar;
    v.y *= scalar;
    v.z *= scalar;
    return v;
}

Vector vmatmul(Matrix m, Vector v) {
    Vector w = {
        .x = (m.xx * v.x + m.xy * v.y + m.xz * v.z),
        .y = (m.yx * v.x + m.yy * v.y + m.yz * v.z),
        .z = (m.zx * v.x + m.zy * v.y + m.zz * v.z)
    };

    return w;
}

double vmag(Vector v) {
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

void vunit(Vector *v) {
    double mag = vmag(*v);
    v->x /= mag;
    v->y /= mag;
    v->z /= mag;
}

Quaternion vtoq(Vector v) {
    Quaternion q = {
        .w = 0.0,
        .i = v.x,
        .j = v.y,
        .k = v.z
    };

    return q;
}

Vector qtov(Quaternion q) {
    Vector w = {
        .x = q.i,
        .y = q.j,
        .z = q.k
    };

    return w;
}

Matrix qtorot(Quaternion q) {
    Matrix m;
    return m;
}

Vector qrotate_vector(Quaternion q, Vector v) {
    // v* = q v q*
    // intermediate_q = (q v)
    // intermediate_q = (intermediate_q q*)
    // v* = <intermediate_q.i, intermediate_q.j, intermediate_q.k>
    Quaternion intermediate_q = vtoq(v);
    intermediate_q = qrotate_quaternion(q, intermediate_q);
    intermediate_q = qrotate_quaternion(intermediate_q, qconj(q));
    return qtov(intermediate_q);
}

double qmag(Quaternion q) {
    // skip conjugating and directly compute sqrt of sum of squares for mag, non-imaginary
    return sqrt(q.w * q.w + q.i * q.i + q.j * q.j + q.k * q.k);
}

Quaternion qrotate_quaternion(Quaternion p, Quaternion q) {
    Quaternion r = {
        .w = (p.w * q.w - p.i * q.i - p.j * q.j - p.k * q.k),
        .i = (p.w * q.i + p.i * q.w + p.j * q.k - p.k * q.j),
        .j = (p.w * q.j + p.j * q.w - p.i * q.k + p.k * q.i),
        .k = (p.w * q.k + p.k * q.w + p.i * q.j - p.j * q.i)
    };

    return r;
}

Quaternion qconj(Quaternion q) {
    Quaternion p = {
        .w = q.w,
        .i = -q.i,
        .j = -q.j,
        .k = -q.k
    };

    return p;
}

void qunit(Quaternion *q) {
    double mag = qmag(*q);
    q->w /= mag;
    q->i /= mag;
    q->j /= mag;
    q->k /= mag;
}