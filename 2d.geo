// Gmsh project created on Tue Nov 05 17:10:43 2019

SetFactory("OpenCASCADE");

Mesh.Algorithm = 6;
Mesh.CharacteristicLengthMax = 0.05;

//+
Rectangle(1) = {0, 0, 0, 10, 1, 0};
//+

lc1=0.005;
lc2=0.05;

//+
Point(5) = {4, 0.5, 0.0, lc2};
//+
Point(6) = {4, 0.6, 0.0, lc1};
//+
Point(7) = {4, 0.4, 0.0, lc1};
//+
Point(8) = {6, 0.5, 0.0, lc2};
//+
Point(9) = {6, 0.6, 0.0, lc1};
//+
Point(10) = {6, 0.4, 0.0, lc1};
//+
Circle(5) = {7, 5, 6};
//+
Circle(6) = {9, 8, 10};
//+
Line(7) = {7, 10};
//+
Line(8) = {6, 9};
//+
Line(22) = {5, 8};
//+
Line Loop(7) = {1, 2, 3, 4};
//+
Curve Loop(8) = {-7, -6, -8, -5};
//+
Plane Surface(2) = {1, 8};


Delete{Surface{1};}
//+
//+
Curve Loop(9) = {8, 6, -7, 5};
//+

Field[1] = Attractor;
Field[1].NodesList = {5, 8};
Field[2] = MathEval;
Field[2].F = "0.05*F1 + 0.001";

Background Field = 2;

Plane Surface(3) = {9};


// Point {5} In Surface {3};
// Point {8} In Surface {3};
