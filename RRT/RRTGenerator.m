% Notes
% When it detects an obstacle the first time, it still seems to go through
% it when going through the RRT algorithm and it misses one endpoint,
% sometimes

clear
clc

% Set number of branches
N = 1000; %Increase to lower resistance

% Set physical tree boundaries
s = 0.04;
S = s*[1, 0; 0, 1]; %4cm square

% Inlet location
x = [0, 0];

% Branch endpoint arrays
a1 = zeros(N,2);
a2 = zeros(N,2);

% Init 1st branch
a1(1, :) = rand(1, 2)*S;
a2(1, :) = x;

% Map showing topological connections between branches
m = zeros(N, 1);
S(1,1)
S(1,2)
S(2,1)
S(2,2)
% Add branches to tree
for i = 2:1:N
    
    % Initialize the d minimum and k
    dmin = 0; % The shortest distance
    k = 0; % The number of attempts
    boundary = 0.0008;

    % Loops while minimum distance is less than a minimum distance and k is
    % less than a max number of iterations
    while dmin < 5*8e-6 && k < 1000
        
        invalid_a1_point = true;

        while invalid_a1_point
            % Creates a random point within the bounds of the box to set at the
            % i-th position of the a1 array
            a1(i, :) = rand(1, 2)*S;
            if a1(i, 1) < (S(1,1) - boundary) && a1(i, 1) > (S(1,2) + boundary) && a1(i, 2) < (S(1,1) - boundary) && a1(i, 2) > (S(2,1) + boundary)
                invalid_a1_point = false;
            end
        end

        % Creates the array a4 with the size of i - 1 by 2 and all zeros
        a4 = zeros(i-1, 2);

        % Creates an array of the a1 x and y values from 1 to i - 1
        a1x = a1(1:i-1, 1);
        a1y = a1(1:i-1, 2);

        % Creates an array of the a2 x and y values from 1 to i - 1
        a2x = a2(1:i-1, 1);
        a2y = a2(1:i-1, 2);

        % Gets the x and y value of the a1 x and y at i
        a3x = a1(i, 1);
        a3y = a1(i, 2);

        % Gets the length between 2 points
        L12 = hypot(a1x-a2x, a1y-a2y); % 1 to 2
        L13 = hypot(a1x-a3x, a1y-a3y); % 1 to 3
        L23 = hypot(a2x-a3x, a2y-a3y); % 2 to 3
        L14 = (L13.^2 - L23.^2 + L12.^2)./(2*L12); % 1 to 4
        
        % Checks if the length from 1 to 4 is less than or equal to 0 for
        % all of the points on the array L14 and sets 
        idx1 = L14 <= 0;
        a4(idx1, :) = a1(idx1, :);

        idx2 = L14 >= L12;
        a4(idx2, :) = a2(idx2, :);
        idx3 = ~(idx1 | idx2);
        if any(idx3)
            r12 = [a2x - a1x, a2y - a1y];
            u12 = r12./hypot(r12(:,1), r12(:,2));
            a4(idx3, :) = a1(idx3,:) + L14(idx3).*u12(idx3,:);
        end
        d = hypot(a3x-a4(:,1), a3y-a4(:,2));
        [dmin, j] = min(d);
        k = k + 1;
    end
    if k >= 1000
        fprintf('Max endpoint iterations exceeded.\n')
    end    
    
    
    a2(i, :) = a4(j, :);
    m(i) =  j;
end


%Scaling ratios for length and diameter, see:
%   Y. Huo and G. S. Kassab, “Intraspecific scaling laws of vascular 
%       trees,” Journal of The Royal Society Interface, vol. 9, no. 66, pp.
%       190–200, Jan. 2012, doi: 10.1098/rsif.2011.0270.
%   G. S. Kassab, “Scaling laws of vascular trees: of form and function,” 
%       American Journal of Physiology-Heart and Circulatory Physiology, 
%       vol. 290, no. 2, pp. H894–H903, Feb. 2006, doi: 10.1152/ajpheart.00579.2005.
BR = 2;
p_eps = 1; %Area-preserving: p_eps = 0, Murray's Law: p_eps = 1
p_gam = 0; %Space-filling: p_gam = 0, Area-filling: p_gam = 1
LR = BR^(-1/(3-p_gam));
DR = BR^(-1/(2+p_eps));


%Calculate crown lengths for each branch
Lc = zeros(N,1);
for i = N:-1:2
    
    Li = norm(a2(i,:)-a1(i,:), 2);
    if ~any(m == i)
        %Assume that terminal branches bifurcate one more time into two 
        %pre-capillaries. Each pre-capillary branch assumes a length of 
        %Li*LR. Adding up both pre-capillary branches give BR*Li*LR.
        Lc(i) = BR*Li*LR;
    end
    Lc(m(i)) = Lc(m(i)) + Li + Lc(i);
end


%Scale width of each branch (8e-6 is chosen as pre-capillary size)
lw_max = 8e-6/(min(Lc)./max(Lc)).^(3/7);
lw = (Lc./max(Lc)).^(3/7)*lw_max;


%Discard branches where the stem is completely obscured by another branch
idx_keep = true(1, N);
for i = 1:1:N
    
    d1 = distance_to_line(a1, a2, a1(i,:));
    idx = (d1 < 1.05*lw/2)';
    idx(i:end) = 0;
    idx_keep(i) = ~any(idx);
end
m = m(idx_keep);


%Remap the tree after discarding obscured branches
N = length(m);
for i = 1:1:N
   m(i) = m(i) - sum(~(idx_keep(1:m(i)))); %Remap
end

a1 = a1(idx_keep,:);
a2 = a2(idx_keep,:);


%Recalculate crown length
Lc = zeros(N,1);
for i = N:-1:2
    
    Li = norm(a2(i,:)-a1(i,:), 2);
    if ~any(m == i)
        %Assume that terminal branches bifurcate one more time into two 
        %pre-capillaries. Each pre-capillary branch assumes a length of 
        %Li*LR. Adding up both pre-capillary branches give BR*Li*LR.
        Lc(i) = BR*Li*LR;
    end
    Lc(m(i)) = Lc(m(i)) + Li + Lc(i);
end


%Recalculate branch widths
lw_max = 10e-6/(min(Lc)./max(Lc)).^(3/7);
lw = (Lc./max(Lc)).^(3/7)*lw_max;


%Compute hydraulic resistance
mu = 3.5e-3;                    %Dynamic viscosity [Pa-s]
% Rhyd = @(L, w, h) 12*mu*L./(w.*h.^3.*(1-0.630*h./w)); %Rectangular cross-section (w >> h)
Rhyd = @(L, D) 8*mu*L./(pi*(D/2).^4); %Circular cross-section
si2pru = @(x) x/133.322e6;
pru2si = @(x) x*133.322e6;
R = zeros(N, 1);
v = zeros(N, 1);
for i = N:-1:2
    
    Li = norm(a2(i,:)-a1(i,:), 2);
    if ~any(m == i)
        %Assume that terminal branches bifurcate one more time into two 
        %pre-capillaries. Each pre-capillary branch assumes a length of 
        %Li*LR. Adding up both pre-capillary branches give BR*Li*LR. The
        %pre-capillary diameters are similarly lw(i)*DR.
        v(i) = pi/4*(lw(i)*DR)^2*BR*Li*LR;
    end
    v(m(i)) = v(m(i)) + pi/4*lw(i)^2*Li + v(i);
    if R(m(i)) > 0
        R(m(i)) = 1/(1/R(m(i)) + 1/(Rhyd(Li, lw(i)) + R(i))); 
    else
        R(m(i)) = 1/(1/(Rhyd(Li, lw(i)) + R(i)));
    end
end
fprintf('Tree resistance: %.0f PRU\n', si2pru(R(1)))

% Initializes the capillary point array
capillary_points = [];

% Loops 1 to the size of a1
for i = 1:size(a1, 1)

    % Initialize check
    check = true;

    % Loops 1 to the size of a2
    for j = 1:size(a2, 1)

        % Checks if the i-th point in a1 is equal to the j-th a2
        % If it is then it sets check as false because that means a start
        % is the same as an end and therefore is not a capillary
        if isequal(a1(i, :), a2(j, :))
            check = false;
            break;
        end
    end

    % If check add the capillary point as the i-th a1
    if check
        capillary_points = [capillary_points; a1(i, :)];
    end
end    

%% Process for getting the routes of the veins to the capillaries

% Initialize the veins
v1 = [];
v2 = [];

% Set the outlet
outlet = [S(2, 2), S(1, 1)];
v2 = [v2; outlet];

direct_connections = zeros(size(capillary_points, 1), 1);

%capillary_points = capillary_points(direct_connections == 0, :);

distances = sqrt(sum((capillary_points - outlet).^2, 2));

[~, sorted_indices] = sort(distances);

capillary_points = capillary_points(sorted_indices, :);

capillary_points_remaining = capillary_points;

for i = 1:size(capillary_points, 1)

    capillary_point = capillary_points_remaining(1, :);

    % If it is the first route, connect it to the outlet
    if i == 1
        v1 = [v1; capillary_point];
        capillary_points_remaining = capillary_points_remaining(2:end, :);
    else
        starts = [];
        ends = [];
    
        while isempty(starts) && isempty(ends)
            [starts, ends] = rrt_algorithm(capillary_point, v1, v2, a1, a2);
            
            % If the starts and ends are empty when returned, the capillary
            % points remaining is reshuffled
            % Else it removes the capillary point from the remaining capillary
            % points and adds starts and ends to v1 and v2
            if isempty(starts) && isempty(ends)
                
                capillary_points_remaining = [capillary_points_remaining(2:end, :); capillary_point];
                
                capillary_point = capillary_points_remaining(1, :);
            else
                idx = ismember(capillary_points_remaining, capillary_point, 'rows');
                capillary_points_remaining = capillary_points_remaining(2:end, :);
                v1 = [v1; starts];
                v2 = [v2; ends];
            end
    
        end
    end

end

%Plot channels
% figure('Renderer', 'painters')
hTreeFigure = figure('Visible', 'off');
hold on
for k = 1:1:size(a1, 1)
   plot_channel(a1(k,:), a2(k,:), lw(k), 'b');
end

for k = 1:1:size(v1, 1)
    plot_channel(v1(k, :), v2(k, :), lw(1), 'r')
end
plot(a2(1,1), a2(1,2), 'b^', 'MarkerSize', 10, 'MarkerFaceColor', 'blue')
plot(v2(1,1), v2(1, 2), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'red')
hold off
axis equal
hTreeFigure.Visible = 'on';


%Verify and plot dimensional scaling
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
plot(sort(Lc_norm), 10^p(2)*sort(Lc_norm).^p(1), '-g', 'LineWidth', 1)
hold off
title(sprintf('[D_s/(D_s)_{max}] \\propto [L_c/(L_c)_{max}]^{%.3f}', p(1)))
xlabel('L_c/(L_c)_{max}')
ylabel('D_s/(D_s)_{max}')


%Compute normal distance between point p3 and the line between points p1
%and p2
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

% Uses an rrt algorithm to reach the outlet
function [starts, ends] = rrt_algorithm(route_start, goal_1, goal_2, barrier_1, barrier_2)
    
    % Initialize keep searching as true
    keep_searching = true;

    % Initialze the max distance between each step
    MAX_STEP_SIZE = 0.01;
    MIN_STEP_SIZE = 0.0001;
    MAX_ROUTE_SIZE = 25;
    MIN_THETA = 30;
    MAX_RETRIES = 5;

    % Initialize the temporary routes
    route_to = [];
    route_from = [];
    retries = 0;
    cla;

    size(goal_1)
    size(goal_2)
    % Loops until it finds a route from start to goal
    while keep_searching
        
        % Initialize the endpoint as invalid
        invalid_to_point = true;

        % Loop until it finds a valid endpoint
        while invalid_to_point
            
            % Initialize duplicate as true
            duplicate = true;

            % Gets a random end point that is not a duplicate
            while duplicate

                % Randomly selects a to point
                % More efficient way to do this would be to dynamically
                % change the area that the random point can be selected
                % from based on the bounds of the current from points
                current_to_point = rand(1, 2)*0.04;
                if isempty(route_to)
                    duplicate = false;
                elseif isempty(find(route_to(:, 1) == current_to_point(1) & route_to(:, 2) == current_to_point(2), 1))
                    duplicate = false;
                end
                
            end

            % Initializes the shortest distance
            shortest_distance = 6e5;
            
            % Checks if the route from list is empty and if it is, it sets
            % the to and from point and the distance between them
            if isempty(route_from)
                shortest_distance = distance(current_to_point, route_start);
                to_point = current_to_point;
                from_point = route_start;
            else
                % Loops through all of the start points
                for p = 1:size(route_to, 1)
                    
                    point = route_to(p, :);
    
                    % Gets the distance from the start point to the current end
                    % point
                    d = distance(point, current_to_point);
    
                    % Checks if the distance is less than the current shortest
                    % distance
                    if d < shortest_distance
    
                        % Sets the new shortest disatnce, end point, and start
                        % point
                        shortest_distance = d;
                        to_point = current_to_point;
                        from_point = point;
                    end
                end
            end
            if isempty(route_to)
                theta = 180;
            else
                % Gets the angle between the to and from point in degrees
                [~, idx] = ismember(from_point, route_to, 'rows');
    
                previous_from_point = route_from(idx, :);
    
                theta = get_angle(to_point, from_point, previous_from_point);
            end

            % Checks if the shortest distance is between the max and min
            % step size
            if shortest_distance < MAX_STEP_SIZE && shortest_distance > MIN_STEP_SIZE && theta > MIN_THETA && theta 
                
                % Checks that there is no conflict between any of the
                % current lines and then exits the loop if it is valid
                if ~is_conflict(to_point, from_point, barrier_1, barrier_2) && ~is_conflict(to_point, from_point, route_to, route_from)
                    invalid_to_point = false;
                end
            end
        end

        
        % If there is a conflict between the start and end and a goal
        % segment, finish routing
        if is_conflict(to_point, from_point, goal_1, goal_2)
            to_point = get_intersection(to_point, from_point, goal_1, goal_2);
            keep_searching = false;
        end

        % Adds the current end point and start point to the to and from
        route_to = [route_to; to_point];
        route_from = [route_from; from_point];
        
        
        hold on;

        for j = 1:size(goal_1, 1)
            point1 = goal_1(j, :);
            point2 = goal_2(j, :);
            plot([point1(1), point2(1)], [point1(2), point2(2)], 'r-', 'LineWidth', 1);
        end

        for j = 1:size(barrier_1, 1)
            point1 = barrier_1(j, :);
            point2 = barrier_2(j, :);
            plot([point1(1), point2(1)], [point1(2), point2(2)], 'b-', 'LineWidth', 1);
        end

        % Plot the new branch
        for j = 1:size(route_to, 1)
            point1 = route_to(j, :);
            point2 = route_from(j, :);

            plot([point1(1), point2(1)], [point1(2), point2(2)], 'g-', 'LineWidth', 1);
            pause(0.01);
        end
        hold off;

        if MAX_ROUTE_SIZE < size(route_from, 1)
            route_from = [];
            route_to = [];
            retries = retries + 1
            cla;
        end
        
        % If reaching max retries return -1
        if retries == MAX_RETRIES
            starts = [];
            ends = [];
            return
        end

    end

    % Retraces the end (where it intersects a vein) to the beginning (the
    % capillary)
    
    % Initializes the starts and ends of the points to retrace the steps
    % back from the intersection to the capillary
    starts = [];
    ends = [];
    
    % Set the first point for the start as what was previously the end and
    % vice versa
    starts = [starts; to_point];
    ends = [ends; from_point];

    % Loops until the last point in ends is the same as the capillary
    while ~isequal(ends(end, :), route_start)

        % Gets the last point in ends (most recently added point)
        last_ends_point = ends(end, :);
        
        % Finds where that point is in route to
        route_to
        last_ends_point
        idx = find(route_to(:, 1) == last_ends_point(1) & route_to(:, 2) == last_ends_point(2));
        
        % Sets the ends as 
        ends = [ends; route_from(idx, :)];

        % Sets the next end as the corresponding index of the temp route 2
        starts = [starts; last_ends_point];
    end
    
end

function theta = get_angle(A, B, C)
    a = distance(B, C);
    b = distance(A, C);
    c = distance(A, B);

    theta = rad2deg(acos((b^2 - a^2 - c^2) / (-2 * a * c))); 

end

function point = get_intersection(p1, p2, n1, n2)
    
    closest_intersection = NaN(1,2);

    for i = 1:size(n1, 1)
        point_1 = n1(i, :);
        point_2 = n2(i, :);
        
        x1 = p1(1);
        y1 = p1(2);
        x2 = p2(1);
        y2 = p2(2);
        x3 = point_1(1);
        y3 = point_1(2);
        x4 = point_2(1);
        y4 = point_2(2);
        
        % Get the slope between point 1 and 2
        if x1 == x2
            m12 = 5e-10;
        elseif y1 == y2
            m12 = 5e10;
        else
            m12 = (y1 - y2) / (x1 - x2);
        end

        % Get the slope between point 3 and 4
        if x3 == x4
            m34 = 5e-10;
        elseif y3 == y4
            m34 = 5e10;
        else
            m34 = (y3 - y4) / (x3 - x4);
        end

        b12 = y1 - m12 * x1;

        b34 = y3 - m34 * x3;

        x_intersect = (b12 - b34) / (m34 - m12);

        y_intersect = m12 * x_intersect + b12;
        
        d12 = distance([x1, y1], [x2, y2]);
        d_intersection = distance([x1, y1], [x_intersect, y_intersect]);
        if (x_intersect > min([x3, x4]) && x_intersect < max([x3, x4])) && (y_intersect > min([y3, y4]) && y_intersect < max([y3, y4])) && (d_intersection < d12)
            
            % Need to fix this so it goes to the closest intersection
            if isnan(closest_intersection(1, 1))
                closest_intersection = [x_intersect, y_intersect];
            else
                current_shortest_distance = distance(closest_intersection, [x1, x2]);
                if current_shortest_distance > d_intersection
                    closest_intersection = [x_intersect, y_intersect];
                end
            end

        end

    end
    point = closest_intersection;
end

% Checks if there are any conflicts when trying to reach a point
function conflict = is_conflict(p1, p2, n1, n2)
    
    conflict = false;

    for i = 1:size(n1, 1)
        point_1 = n1(i, :);
        point_2 = n2(i, :);
        
        x1 = p1(1);
        y1 = p1(2);
        x2 = p2(1);
        y2 = p2(2);
        x3 = point_1(1);
        y3 = point_1(2);
        x4 = point_2(1);
        y4 = point_2(2);
        
        % Get the slope between point 1 and 2
        if x1 == x2
            m12 = 5e-10;
        elseif y1 == y2
            m12 = 5e10;
        else
            m12 = (y1 - y2) / (x1 - x2);
        end

        % Get the slope between point 3 and 4
        if x3 == x4
            m34 = 5e-10;
        elseif y3 == y4
            m34 = 5e10;
        else
            m34 = (y3 - y4) / (x3 - x4);
        end

        b12 = y1 - m12 * x1;

        b34 = y3 - m34 * x3;

        x_intersect = (b12 - b34) / (m34 - m12);

        y_intersect = m12 * x_intersect + b12;
        
        d12 = distance([x1, y1], [x2, y2]);
        d_intersection = distance([x1, y1], [x_intersect, y_intersect]);

        if (x_intersect > min([x3, x4]) && x_intersect < max([x3, x4])) && (y_intersect > min([y3, y4]) && y_intersect < max([y3, y4])) && (d_intersection < d12)
            conflict = true;
        else
            conflict = false;
        end

        if conflict
            break
        end
    end
    
end

% Finds the distance between two points
function d = distance(p1, p2)
    d = sqrt((p1(1) - p2(1))^2 + (p1(2) - p2(2))^2);
end

%Plot a branch of the tree
function plot_channel(p1, p2, w, c)
    l = norm(p2-p1, 2);
    u1 = (p2-p1)/l;
    u2 = [-u1(2), u1(1)];
    P = zeros(4, 2);
    P(1,:) = p1 + 0.7937*w/2*u2;
    P(2,:) = P(1,:) + l*u1 + (1-0.7937)*w/2*u2;
    P(3,:) = P(2,:) - w*u2;
    P(4,:) = P(3,:) - l*u1 + (1-0.7937)*w/2*u2;
    patch(P(:,1), P(:,2), c, 'EdgeColor', 'none');
end
