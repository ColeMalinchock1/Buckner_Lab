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

% Inlet and outlet location
inlet = [0, 0];
outlet = [s, s];

% Initializing capillary junctions
capillary_junctions = zeros(N, 2);

% Makes the first capillary junction the center 
capillary_junctions(1, :) = [s / 2, s / 2];

% Initialize generation 1 points
a1_gen1_1 = [0, s];
a2_gen1_1 = inlet;
a1_gen1_2 = [s, 0];
a2_gen1_2 = inlet;

v1_gen1_1 = [0, s];
v2_gen1_1 = outlet;
v1_gen1_2 = [s, 0];
v2_gen1_2 = outlet;

% Creating matrices of arteries and veins
% a1 and v1 refer to end points
% a2 and v2 refer to start points
a1 = [a1_gen1_1; a1_gen1_2];
a2 = [a2_gen1_1; a2_gen1_2];
v1 = [v1_gen1_1; v1_gen1_2];
v2 = [v2_gen1_1; v2_gen1_2];

%% Process for generating routes from capillaries to generation 1

% Plot channels
% figure('Renderer', 'painters')
hTreeFigure = figure('Visible', 'off');
hold on
for k = 1:1:size(a1, 1)
   plot_channel(a1(k,:), a2(k,:), 1, 'b');
end

for k = 1:1:size(v1, 1)
    plot_channel(v1(k, :), v2(k, :), 2, 'r')
end
plot(a2(1,1), a2(1,2), 'b^', 'MarkerSize', 10, 'MarkerFaceColor', 'blue')
plot(v2(1,1), v2(1, 2), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'red')
hold off
axis equal
hTreeFigure.Visible = 'on';

% Loops through all of the capillary junctions
for i = 1:N
    
    % Initializes the junction as incomplete
    incomplete_junction = true;
    
    % Loops until the junction is complete and receives a valid starts and
    % ends for the arteries and veins
    while incomplete_junction
        
        % Generates a new random if it is not the first one since the first
        % was preset as the center
        if i ~= 1
            capillary_junctions(i, :) = s * rand(1, 2);
        end
        
        % Gets the capillary junction from the i-th position of the
        % capillary junctions
        capillary_junction = capillary_junction(i, :);
        
        % Gets the starts and ends of the route generated from rrt for the
        % arterie
        [a_starts, a_ends] = rrt_algorithm(capillary_junction, a1, a2, v1, v2);
        
        % Checks if the a_starts and a_ends is empty and was an
        % unsuccessful route
        % If it was successful, continue the process
        if ~isempty(a_starts) && ~isempty(e_ends)
            % Adds the starts and ends to the temportary a1 and a2
            temp_a1 = [a1; a_starts];
            temp_a2 = [a2, a_ends];
    
            % Gets the starts and ends of the route generated from rrt for the
            % vein
            [v_starts, v_ends] = rrt_algorithm(capillary_junction, v1, v2, temp_a1, temp_a2);

            % Checks if the v_starts and v_ends is empty and was an
            % unsuccessful route
            % If is was successful, continue the process
            if ~isempty(v_starts) && ~isempty(v_ends)

                % Adds the starts and ends to a1, a2, v1, v2
                a1 = [a1; a_starts];
                a2 = [a2; a_ends];

                v1 = [v1; v_starts];
                v2 = [v2; v_ends];

                % Changes the incomplete junction to false so it goes to
                % the next capillary junction
                incomplete_junction = false;
            end
        end
    end

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
