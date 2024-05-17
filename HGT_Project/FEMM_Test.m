clc;
clear;
close all;

addpath('C:\femm42\mfiles');

openfemm;
newdocument(0);
mi_probdef(0, 'millimeters', 'axi', 1E-8)

gap = 2.0;

h1 = 5.334;
r = 12.446;
h2 = h1 + gap;
material = 'N42';

m1 = [0, 0
    r, 0
    r, h1
    0, h1
    0, 0];

m2 = [0, h2
    r, h2
    r, h2 + h1
    0, h2 + h1
    0, h2];


DrawMagnets(m1)
DrawMagnets(m2)


mi_getmaterial(material);
mi_getmaterial('Air');

mi_addblocklabel(mean(m1(:,1)), mean(m1(:,2)));
mi_selectlabel(mean(m1(:,1)), mean(m1(:,2)));
mi_setblockprop(material, 0, 0, 'None', 90, 0, 0);
mi_clearselected();

mi_addblocklabel(mean(m2(:,1)), mean(m2(:,2)));
mi_selectlabel(mean(m2(:,1)), mean(m2(:,2)));
mi_setblockprop(material, 0, 0, 'None', 90, 0, 0);
mi_clearselected();

mi_addblocklabel(r + 0.1, 0.1);
mi_selectlabel(r + 0.1, 0.1);
mi_setblockprop('Air', 0, 0, 'None', 0, 0, 0);
mi_clearselected();


mi_refreshview()

mi_zoomnatural()

mi_saveas('C:\\Users\\malin\\Downloads\\Dr. Buckner Lab\\HGT\\Matlab\\femmFile.fem')

mi_analyze()

function DrawMagnets(m)

    for i = 1:size(m, 1) - 1
        mi_addnode(m(i,1), m(i,2));
    end
    
    for i = 1:size(m, 1) - 1
        mi_addsegment(m(i, 1), m(i, 2), m(i+1, 1), m(i+1,2));
    end
end
