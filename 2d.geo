// Gmsh project created on Tue Nov 05 17:10:43 2019

SetFactory("OpenCASCADE");

Mesh.Algorithm = 6;
Mesh.CharacteristicLengthMin = 0.1;
Mesh.CharacteristicLengthMax = 0.1;

//+
Rectangle(1) = {0, 0, 0, 10, 1, 0}; 
//+

Curve Loop(2) = {1, 2, 3, 4};
//+


lc1=0.2;

//+
Point(5) = {4, 0.5, 0, lc1};
//+
Point(6) = {4, 0.6, 0, lc1};
//+
Point(7) = {4, 0.4, 0, 0.05};
//+
Point(8) = {6, 0.5, 0, 0.05};
//+
Point(9) = {6, 0.6, 0, 1.0};
//+
Point(10) = {6, 0.4, 0, 1.0};
//+
Circle(5) = {7, 5, 6};
//+
Circle(6) = {9, 8, 10};
//+
Line(7) = {7, 10};
//+
Line(8) = {6, 9};
//+
Curve Loop(3) = {7, -6, -8, -5};
//+
Curve Loop(4) = {1, 2, 3, 4};
//+
Curve Loop(5) = {7, -6, -8, -5};
//+
Curve Loop(6) = {1, 2, 3, 4};
//+
Curve Loop(7) = {1, 2, 3, 4};
//+
Curve Loop(8) = {7, -6, -8, -5};
//+
Plane Surface(2) = {7, 8};

Delete{Surface{1};}
