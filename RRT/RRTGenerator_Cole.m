clear;
clc;

unsuccessful = true;

count = 1;

while unsuccessful
    fprintf("Attempt number %d\n", count);
    unsuccessful = main();
    count = count + 1;
end

fprintf("Complete");

function unsuccessful = main()
    % Number of generations
    N = 100;
    
    % Set the boundaries of the tree
    s = 0.04;
    S = s * [1, 0; 0, 1]; % 4cm square
    
    % Location of the inlet
    inlet = [0, 0];
    outlet = [1, 1] * s;
    
    % Arterial start points
    a1 = zeros(N, 2);
    
    % Venous start points
    v1 = zeros(N, 2);
    
    % Generate random points within the bounds
    joining_points = s * rand(N, 2);
    
    % Init 1st branch of artery by setting first start point
    a1(1, :) = inlet;
    
    % Init 1st branch of vein by setting first start point
    v1(1, :) = outlet;
    
    % Setting the first joint point for the first branch
    joining_points(1, :) = s * rand(1, 2);
    
    % Init 2nd branch of artery by setting the second start point
    %a1(2, :) = inlet;
    
    % Init 2nd branch of vein by setting the second start point
    %v1(2, :) = outlet;
    
    % Setting the second joint point for the second branch
    %joining_points(2, :) = inlet + [0, 1.0] * S;
    
    % Sets the MAX_TRIES for the loop that checks for conflicts
    MAX_TRIES = 9e5;
    
    % Loop through all the points in joining points
    for i = 2:N
        
        % Check to see if there is a conflict in the new point being used
        is_conflict = true;
        
        % Initializes the count before the while loop
        count = 0;
    
        % While loop that waits until there are no more conflicts detected
        while is_conflict
    
            % Gets the closest arterie point to the i-th joining point
            closest_point = find_closest_point(i, a1, joining_points);
        
            % Adds that closest point as the i-th arterie starting point
            a1(i, :) = closest_point;
    
            % Checks if there are any conflicts between the new arterie and any
            % existing veins
            is_conflict = check_conflicts(i, a1, v1, joining_points);
            
            % Checks if the conflict has already been caught
            if ~is_conflict
    
                % Gets the closest vein point to the i-th joining point
                closest_point = find_closest_point(i, v1, joining_points);
            
                % Adds that closest point as the i-th vein starting point
                v1(i, :) = closest_point;
                
                % Checks if there are any conflicts between the lines of arteries
                % and veins
                is_conflict = check_conflicts(i, v1, a1, joining_points);
            end
    
            % Checks if the count exceeds the max amount of retries
            % Quits the session if it exceeds the max retries
            if count > MAX_TRIES
                unsuccessful = true;
                return;
            end
            
            % Adds to count 
            count = count + 1;
    
            if is_conflict
                % If there is a new conflict make a new random point for that idx
                % in the joining points
                joining_points(i, :) = s * rand(1, 2);
            end
        end
    end
    
    % Plot the channels
    figure;
    hold on;
    
    % Plots all of the arteries and veins
    for i = 1:N
        
        plot_channel(a1(i, :), joining_points(i, :), 0.0001, 'r');
        plot_channel(v1(i, :), joining_points(i, :), 0.0001, 'b');
    end
    
    % Plot random points
    plot(joining_points(:, 1), joining_points(:, 2), 'k.', 'MarkerSize', 10);
    
    % Set axis limits for better visualization
    axis([0 s 0 s]);
    axis equal;
    grid on;
    xlabel('X-axis');
    ylabel('Y-axis');
    title('Arterial and Venous Branches with Random Points');
    
    hold off;

    unsuccessful = false;
end

% Checks for conflicts after the new vessel is added
function is_conflict = check_conflicts(idx, p1, p2, joining_points)
    
    % Assumes no conflict until one is caught
    is_conflict = false;

    % Get the linear equation of p1
    m1 = (p1(idx, 2) - joining_points(idx, 2)) / (p1(idx, 1) - joining_points(idx, 1));
    b1 = p1(idx, 2) - m1 * p1(idx, 1);
    
    % Loop through all of the vessels in p2 to see if they intersect with
    % the new p1 vessel. Excludes idx because they should be intersecting
    % at their joint
    for i = 1:idx - 1
            
            % Get the linear equation of the vein at that index
            m2 = (p2(i, 2) - joining_points(i, 2)) / (p2(i, 1) - joining_points(i, 1));
            b2 = p2(i, 2) - m2 * p2(i, 1);
            
            % Checks that the slopes are not parallel
            if abs(m1 - m2) > 1e-6

                % Finds the point where the two lines intersect
                intersection_x = (b2 - b1) / (m1 - m2);
                intersection_y = m1 * intersection_x + b1;
                
                % Setting the tolerance of the bounds check
                tolerance = 1e-4;

                % Checks if the x, y point is within the two points of the
                % line and will then return true and break the for loop
                if (intersection_x <= max(p1(idx, 1), joining_points(idx, 1)) + tolerance) && ...
               (intersection_x >= min(p1(idx, 1), joining_points(idx, 1)) - tolerance) && ...
               (intersection_y <= max(p1(idx, 2), joining_points(idx, 2)) + tolerance) && ...
               (intersection_y >= min(p1(idx, 2), joining_points(idx, 2)) - tolerance)
                    is_conflict = true;
                    break;
                end
            end
           
    end

end

% Gives the closest point from a current arterie or vein to the joining
% point at the specified index
function closest_point = find_closest_point(idx, p1, joining_points)
    
    % Initialize the shortest distance as a distance futher than what is
    % possible in the box
    closest_distance = 0.04 + 1.0;
    
    % Loops through all of the possible vessels that could be the closest
    % to the joint excluding the last one
    for i = 1:idx - 1

        % Gets the linear equation from start to joint of i-th vessel
        % Checks if the slope is infinite
        m1 = (p1(i, 2) - joining_points(i, 2)) / (p1(i, 1) - joining_points(i, 1));
    
        if abs(m1) == inf
            m1 = 999999;
        end

        b1 = p1(i, 2) - m1 * p1(i, 1);

        % Gets the linear equation of the line that is perpendicular to
        % line 1 and goes through the joint being assessed
        m2 = -1/m1;

        if abs(m2) == inf
            m2 = 9999999;
        end

        b2 = joining_points(idx, 2) - m2 * joining_points(idx, 1);
        
        % Finds the point where the two lines intersect
        intersection_x = (b1 - b2) / (m2 - m1);
        intersection_y = m1 * intersection_x + b1;
        
        tolerance = 1e-4;

        % Checks if the x, y point is within the two points of line 1
        % Else sets the closest point as the joining point
        if (intersection_x <= max([p1(i, 1), joining_points(i, 1)]) + tolerance) && ...
           (intersection_x >= min([p1(i, 1), joining_points(i, 1)]) - tolerance) && ...
           (intersection_y <= max([p1(i, 2), joining_points(i, 2)]) + tolerance) && ...
           (intersection_y >= min([p1(i, 2), joining_points(i, 2)]) - tolerance)
            % Checks if the distance is less than the current closest
            % distance
            d = distance([intersection_x, intersection_y], joining_points(idx, :));
            if d < closest_distance

                % Sets the new closest distance and closest point
                closest_distance = d;
                current_closest_point = [intersection_x, intersection_y];
            end
        else

            % Checks if the distance is less than the current closest
            % distance
            d = distance(joining_points(i, :), joining_points(idx, :));
            if d < closest_distance

                % Sets the new closest distance and closest point
                closest_distance = d;
                current_closest_point = joining_points(i, :);
            end
        end
    
    end
    
    % Sets the current closest point as the closest point that is returned
    closest_point = current_closest_point;

end

% Finds the distance between two points
function d = distance(point1, point2)
    d = sqrt((point2(1) - point1(1))^2 + (point2(2) - point1(2))^2);
end

% Function to plot the channel
function plot_channel(p1, p2, w, c)
    l = norm(p2-p1, 2);
    u1 = (p2-p1)/l;
    u2 = [-u1(2), u1(1)];
    P = zeros(4, 2);
    P(1, :) = p1 + 0.7937 * w / 2 * u2;
    P(2, :) = P(1, :) + l * u1 + (1 - 0.7937) * w / 2 * u2;
    P(3, :) = P(2, :) - w * u2;
    P(4, :) = P(3, :) - l * u1 + (1 - 0.7937) * w / 2 * u2;
    patch(P(:, 1), P(:, 2), c, 'EdgeColor', 'none');
end
