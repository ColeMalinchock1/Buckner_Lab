%Generate a vascular tree using a rapidly exploring random tree (RRT) algorithm
clear
clc

% Set number of branches
N = 10000; % Increase to lower resistance

% Set physical tree boundaries
S = 0.04*[1, 0; 0, 1]; % 4cm square

% Inlet location
x = [0, 0];

% Function to create a tree
function [p1, p2, m, Lc, lw, R, v] = create_tree(N, S, x)
    % Branch endpoint arrays
    p1 = zeros(N,2);
    p2 = zeros(N,2);

    % Init 1st branch
    p1(1, :) = rand(1, 2)*S;
    p2(1, :) = x;

    % Map showing topological connections between branches
    m = zeros(N, 1);

    % Add branches to tree
    for i = 2:1:N
        dmin = 0;
        k = 0;
        while dmin < 5*8e-6 && k < 1000
            p1(i, :) = rand(1, 2)*S;
            p4 = zeros(i-1, 2);
            p1x = p1(1:i-1, 1);
            p1y = p1(1:i-1, 2);
            p2x = p2(1:i-1, 1);
            p2y = p2(1:i-1, 2);
            p3x = p1(i, 1);
            p3y = p1(i, 2);
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
            [dmin, j] = min(d);
            k = k + 1;
        end
        if k >= 1000
            fprintf('Max endpoint iterations exceeded.\n')
        end    
        
        p2(i, :) = p4(j, :);
        m(i) =  j;
    end

    % Scaling ratios for length and diameter
    BR = 2;
    p_eps = 1; % Area-preserving: p_eps = 0, Murray's Law: p_eps = 1
    p_gam = 0; % Space-filling: p_gam = 0, Area-filling: p_gam = 1
    LR = BR^(-1/(3-p_gam));
    DR = BR^(-1/(2+p_eps));

    % Calculate crown lengths for each branch
    Lc = zeros(N,1);
    for i = N:-1:2
        Li = norm(p2(i,:)-p1(i,:), 2);
        if ~any(m == i)
            Lc(i) = BR*Li*LR;
        end
        Lc(m(i)) = Lc(m(i)) + Li + Lc(i);
    end

    % Scale width of each branch (8e-6 is chosen as pre-capillary size)
    lw_max = 8e-6/(min(Lc)./max(Lc)).^(3/7);
    lw = (Lc./max(Lc)).^(3/7)*lw_max;

    % Discard branches where the stem is completely obscured by another branch
    idx_keep = true(1, N);
    for i = 1:1:N
        d1 = distance_to_line(p1, p2, p1(i,:));
        idx = (d1 < 1.05*lw/2)';
        idx(i:end) = 0;
        idx_keep(i) = ~any(idx);
    end
    m = m(idx_keep);

    % Remap the tree after discarding obscured branches
    N = length(m);
    for i = 1:1:N
        m(i) = m(i) - sum(~(idx_keep(1:m(i)))); % Remap
    end
    p1 = p1(idx_keep,:);
    p2 = p2(idx_keep,:);

    % Recalculate crown length
    Lc = zeros(N,1);
    for i = N:-1:2
        Li = norm(p2(i,:)-p1(i,:), 2);
        if ~any(m == i)
            Lc(i) = BR*Li*LR;
        end
        Lc(m(i)) = Lc(m(i)) + Li + Lc(i);
    end

    % Recalculate branch widths
    lw_max = 10e-6/(min(Lc)./max(Lc)).^(3/7);
    lw = (Lc./max(Lc)).^(3/7)*lw_max;

    % Compute hydraulic resistance
    mu = 3.5e-3; % Dynamic viscosity [Pa-s]
    Rhyd = @(L, D) 8*mu*L./(pi*(D/2).^4); % Circular cross-section
    R = zeros(N, 1);
    v = zeros(N, 1);
    for i = N:-1:2
        Li = norm(p2(i,:)-p1(i,:), 2);
        if !any(m == i)
            v(i) = pi/4*(lw(i)*DR)^2*BR*Li*LR;
        end
        v(m(i)) = v(m(i)) + pi/4*lw(i)^2*Li + v(i);
        if R(m(i)) > 0
            R(m(i)) = 1/(1/R(m(i)) + 1/(Rhyd(Li, lw(i)) + R(i))); 
        else
            R(m(i)) = 1/(1/(Rhyd(Li, lw(i)) + R(i)));
        end
    end
end

% Generate arterial tree (black)
[p1_arteries, p2_arteries, m_arteries, Lc_arteries, lw_arteries, R_arteries, v_arteries] = create_tree(N, S, x);

% Generate venous tree (red)
[p1_veins, p2_veins, m_veins, Lc_veins, lw_veins, R_veins, v_veins] = create_tree(N, S, x + 0.04);

% Plot both trees
hTreeFigure = figure('Visible', 'off');
hold on

% Plot arteries
for k = 1:1:length(m_arteries)
    plot_channel(p1_arteries(k,:), p2_arteries(k,:), lw_arteries(k), 'k');
end
plot(p2_arteries(1,1), p2_arteries(1,2), 'b^', 'MarkerSize', 10, 'MarkerFaceColor', 'blue')

% Plot veins
for k = 1:1:length(m_veins)
    plot_channel(p1_veins(k,:), p2_veins(k,:), lw_veins(k), 'r');
end
plot(p2_veins(1,1), p2_veins(1,2), 'r^', 'MarkerSize', 10, 'MarkerFaceColor', 'red')

hold off
axis equal
hTreeFigure.Visible = 'on';

% Plot a branch of the tree
function plot_channel(p1, p2, w, color)
    l = norm(p2-p1, 2);
    u1 = (p2-p1)/l;
    u2 = [-u1(2), u1(1)];
    P = zeros(4, 2);
    P(1,:) = p1 + 0.7937*w/2*u2;
    P(2,:) = P(1,:) + l*u1 + (1-0.7937)*w/2*u2;
    P(3,:) = P(2,:) - w*u2;
    P(4,:) = P(3,:) - l*u1 + (1-0.7937)*w/2*u2;
    patch(P(:,1), P(:,2), color, 'EdgeColor', 'none');
end

% Compute normal distance between point p3 and the line between points p1 and p2
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
