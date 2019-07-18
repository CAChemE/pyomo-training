$Title  Sintesis de Procesos I

*Autor: Juan Javaloyes Anton.

$OFFSYMXREF
$OFFSYMLIST
option limrow = 0 ;
option limcol = 0;
option solprint = on;
option sysout = off;
option LP = CPLEX;
option MIP = CPLEX;
option NLP = CONOPT;
option MINLP = DICOPT;

*==============================================================================
*                   ***Sintesis de Procesos_I***
*                          [GAMS_2005/06]
*==============================================================================

* Sintesis de Procesos_I. Apartado A
Variable
         z  funcion objetivo

Positive Variables
         x1 Caudal de materia prima A
         x2
         x3 Caudal de B comprado
         x4 ,x5, x6, x7, x8
         c1, c2,c3;

Binary Variables
         y1, y2, y3;

Equations
         funob, ec1, ec2, ec3, ec4, ec5, ec6, ec7, ec8, ec9, ec10, ec11
         ec12, ec13,bal1, bal2;

funob.. z=E=x8*1800-(c1+c2+c3+x3*950+550*x1);

*Ecuaciones Disyuncion_1: Se produce B por el proceso I o no

ec1.. c1=E=1000*y1+250*x1;
ec2.. x2=E=0.9*x1;
ec3.. x1-16*y1=L=0;
ec4.. x2-16*0.9*y1=L=0;

*Ecuaciones Disyuncion_2: Se produce C por el proceso II o no
ec5.. y2+y3=E=1;
ec6.. c2=E=1500*y2+400*x4;
ec7.. x6=E=0.82*x4;
ec8.. x4-(10/0.82)*y2=L=0;
ec9.. x6-10*y2=L=0;

*Ecuaciones Disyuncion_3: Se produce C por el proceso III o no
ec10.. c3=E=2000*y3+550*x5;
ec11.. x7=E=0.95*x5;
ec12.. x5-(10/0.95)*y3=L=0;
ec13.. x7-10*y3=L=0;

*Balances de materia

bal1..x2+x3=E=x4+x5;
bal2..x6+x7=E=x8;


*Limites

x8.up=10;



model sintesis /all/;
solve sintesis using MIP maximizing z;

display z.l, y1.l, y2.l, y3.l, x1.l, x3.l, x4.l, x5.l, x8.l,c1.l,c2.l,c3.l
