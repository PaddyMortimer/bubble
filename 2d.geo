// Gmsh project created on Tue Nov 05 17:10:43 2019

SetFactory("OpenCASCADE");

Mesh.Algorithm = 6;
Mesh.CharacteristicLengthMax = 0.1;

//+
Rectangle(1) = {0, 0, 0, 10, 1, 0};
//+

lc1=0.02;

//+
Point(5) = {4, 0.5, 0.0, lc1};
//+
Point(6) = {4, 0.6, 0.0, lc1};
//+
Point(7) = {4, 0.4, 0.0, lc1};
//+
Point(8) = {6, 0.5, 0.0, lc1};
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
Line Loop(7) = {1, 2, 3, 4};
//+
Curve Loop(8) = {-7, -6, -8, -5};
//+
Plane Surface(2) = {1, 8};

Delete{Surface{1};}
//+