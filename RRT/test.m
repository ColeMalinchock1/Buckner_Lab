% Define the arrays
array1 = [1, 2; 3, 4; 5, 6; 7,8; 9,10;11,12;13,14;15,16;17,18];
array2 = [3, 4; 5, 6; 7, 8;9,10;11,12;13,14;15,16;17,18;19,20];

% Initialize the figure
figure;
hold on;

% Loop through each pair of points
for i = 1:size(array1, 1)
    % Get the corresponding points from each array
    point1 = array1(i, :);
    point2 = array2(i, :);
    
    % Plot the points and draw a line between them
    plot([point1(1), point2(1)], [point1(2), point2(2)], 'b-o', 'LineWidth', 2);
    pause(1.0);
end

% Set axis labels and title for better visualization
xlabel('X-axis');
ylabel('Y-axis');
title('Lines between corresponding points in array1 and array2');
axis equal; % Set equal scaling for both axes
grid on; % Add grid for better visibility

hold off;
