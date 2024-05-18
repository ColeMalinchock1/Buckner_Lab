clear;
clc;

% Number of generations
N = 10000;

% Set the boudnaries of the tree
s = 0.04;
S = s * [1, 0; 0, 1]; %4cm square

% Location of the inlet
inlet = [0, 0];
outlet = [1, 1] * s;

% arterie endpoint arrays
a1 = zeros(N, 2);
a2 = zeros(N, 2);

% vein endpoint arrays
v1 = zeros(N, 2);
v2 = zeros(N, 2);

% Init 1st branch of arterie
a1(1, :) = inlet + [0.9, 0] * S;
a2(1, :) = inlet;

% Init 1st branch of vein
v1(1, :) = outlet;
v2(1, :) = outlet - [0.9, 0] * S;

% Init 2nd branch of arterie
%a1(2, :) = inlet + [0, 0.9] * S;
%a2(2, :) = inlet;

% Init 2nd branch of vein
v1(2, :) = outlet;
v2(2, :) = outlet - [0, 0.9] * S;

% Init
m = zeros(N, 1);

% Loop through all the generations
for i = 2:1:N

    % Initialize the minimum distance and k
    dmin = 0;
    k = 0;

    % Continue until 1000 points are made or the minimum distance is
    % reached
    while dmin < 5*8e-6 && k < 1000

        % Set the a1 to a random point (x,y) on the map
        a1(i, :) = rand(1, 2) * S;

        % Init a4 as the size of the i by 2
        a4 = zeros(i - 1, 2);

        % Get the a1 x, y and a2 x, y
        a1x = a1(1:i - 1, 1);
        a1y = a1(1:i - 1, 2);
        a2x = a2(1:i - 1, 1);
        a2y = a2(1:i - 1, 2);

        % Get the new random point x and y
        a3x = a1(i, 1);
        a3y = a1(i, 2);

        % Find the vectors between 1-2, 1-3, and 2-3
        L12 = hypot(a1x - a2x, a1y - a2y);
        L13 = hypot(a1x - a3x, a1y - a3y);
        L23 = hypot(a2x - a3x, a2y - a3y);

        % Find the vector between connection point and new point, 1-4
        L14 = (L13.^2 - L23.^2 + L12.^2)./(2 * L12);

        % Check that the vector is negative
        idx1 = L14 <= 0;

        % 
        a4(idx1, :) = a1(idx1, :);
        idx2 = L14 >= L12;
        a4(idx2, :) = a2(idx2, :);
        idx3 = ~(idx1 | idx2);
        if any(idx3)
            r12 = [a2x - a1x, a2y - a1y];
            u12 = r12./hypot(r12(:, 1), r12(:, 2));
            a4(idx3, :) = a1(idx3, :) + L14(idx3).*u12(idx3, :);
        end
        d = hypot(a3x - a4(:, 1), a3y-a4(:, 2));
        [dmin, j] = min(d);
        k = k + 1;
    end
    if k >= 1000
        fprintf('Max endpoint iterations exceeded.\n');
    end

    a2(i, :) = a4(j, :);
    m(i) = j;
end
        

BR = 2;
p_eps = 1;
p_gam = 0;
LR = BR^(-1/(3-p_gam));
DR = BR^(-1/(2+p_gam));

Lc = zeros(N, 1);
for i = N: -1: 2
    Li = norm(a2(i, :) - a1(i, :), 2);
    if ~any(m == i)
        Lc(i) = BR * Li * LR;
    end
    Lc(m(i)) = Lc(m(i)) + Li + Lc(i);
end

lw_max = 8e-6/(min(Lc)./max(Lc)).^(3/7);
lw = (Lc./max(Lc)).^(3/7)*lw_max;

idx_keep = true(1, N);
for i = 1:1:N
    d1 = distance_to_line(a1, a2, a1(i, :));
    idx = (d1 < 1.05*lw/2);
    idx(i: end) = 0;
    idx_keep(i) = ~any(idx);
end
m = m(idx_keep);

% Remap the tree after discarding obscured branches
N = length(m);
for i = 1:1:N
    m(i) = m(i) - sum(~(idx_keep(1:m(i))));
end
a1 = a1(idx_keep, :);
a2 = a2(idx_keep, :);

% Recalculate crown length
Lc = zeros(N, 1);
for i = N: -1: 2
    Li = norm(a2(i, :)-a1(i, :), 2);
    if ~any(m == i)
        Lc(i) = BR * Li * LR;
    end
    Lc(m(i)) = Lc(m(i)) + Li + Lc(i);
end

% Recalculate branch widths
lw_max = 10e-6/(min(Lc)./max(Lc)).^(3/7);
lw = (Lc./max(Lc)).^(3/7)*lw_max;

mu = 3.5e-3;
Rhyd = @(L, D) 8*mu*L./(pi*(D/2).^4);
si2pru = @(x) x/133.322e6;
pru2si = @(x) x*133.322e6;
R = zeros(N, 1);
v = zeros(N, 1);
for i = N: -1: 2
    Li = norm(a2(i, :) - a1(i, :), 2);
    if ~any(m == i)
        v(i) = pi/4 * (lw(i) * DR)^2 * BR * Li * LR;
    end
    v(m(i)) = v(m(i)) + pi/4 * lw(i)^2 * Li + v(i);
    if R(m(i)) > 0
        R(m(i)) = 1/(1/R(m(i)) + 1/(Rhyd(Li, lw(i)) + R(i)));
    else
        R(m(i)) = 1/(1/(Rhyd(Li, lw(i)) + R(i)));
    end
end
fprintf('Tree resistance: %.0f PRU\n', si2pru(R(1)))

hTreeFigure = figure('Visible','off');
hold on;
for k = 1: 1: N
    plot_channel(a1(k, :), a2(k, :), lw(k));
end
plot(a2(1, 1), a2(1, 2), 'b^', 'MarkerSize', 10, 'MarkerFaceColor', 'blue');
hold off;
axis equal;
hTreeFigure.Visible = 'on';

D_norm = lw/lw(1);
Lc_norm = Lc/Lc(1);
V_norm = v/v(1);
figure
subplot(1, 2, 1)
loglog(D_norm, V_norm, '.b')
p = polyfit(log10(D_norm), log10(V_norm), 1);
hold on
plot(sort(D_norm), 10^p(2)*sort(D_norm).^p(1), '-g', 'LineWidth', 1)
hold off
title(sprintf('[V_c/(V_c)_{max}] \\propto [D_s/(D_s)_{max}]^{%.3f}', p(1)))
xlabel('D_s/(D_s)_{max}')
ylabel('V_c/(V_c)_{max}')
subplot(1, 2, 2)
loglog(Lc_norm, D_norm, '.b')
p = polyfit(log10(Lc_norm), log10(D_norm), 1);
hold on
plot(sort(Lc_norm), 10^p(2)*sort(Lc_norm).^p(1), '-g', 'LineWidth', 1);
hold off
title(sprintf('[D_s/(D_s)_{max}] \\propto [L_c/(L_c)_{max}]^{%.3f}', p(1)))
xlabel('L_c/(L_c)_{max}')
ylabel('D_s/(D_s)_{max}')

function d = distance_to_line(p1, p2, p3)
    N = length(p1);
    p4 = zeros(N, 2);
    p1x = p1(:, 1);
    p1y = p1(:, 2);
    p2x = p2(:, 1);
    p2y = p2(:, 2);
    p3x = p3(1);
    p3y = p3(2);
    L12 = hypot(p1x-p2x, p1y-p2y);
    L13 = hypot(p1x-p3x, p1y-p3y);
    L23 = hypot(p2x-p3x, p2y-p3y);
    L14 = (L13.^2 - L23.^2 + L12.^2)./(2*L12);
    idx1 = L14 <= 0;
    p4(idx1, :) = p1(idx1, :);
    idx2 = L14 >= L12;
    p4(idx2, :) = p2(idx2, :);
    idx3 = ~(idx1 | idx2);
    if any(idx3)
        r12 = [p2x - p1x, p2y - p1y];
        u12 = r12./hypot(r12(:,1), r12(:,2));
        p4(idx3, :) = p1(idx3,:) + L14(idx3).*u12(idx3,:);
    end
    d = hypot(p3x-p4(:,1), p3y-p4(:,2));
end

function plot_channel(p1, p2, w)
    l = norm(p2-p1, 2);
    u1 = (p2-p1)/l;
    u2 = [-u1(2), u1(1)];
    P = zeros(4, 2);
    P(1, :) = p1 + 0.7937 * w / 2 * u2;
    P(2, :) = P(1, :) + l * u1 + (1 - 0.7937) * w / 2 * u2;
    P(3, :) = P(2, :) - w * u2;
    P(4, :) = P(3, :) - l * u1 + (1 - 0.7937) * w / 2 * u2;
    patch(P(:, 1), P(:, 2), 'k', 'EdgeColor', 'none');
end



