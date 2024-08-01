
% Number of generations
N = 55;

% Set the boundaries of the tree
s = 0.04;

% Location of the inlet and outlet
inlet = [0, 0];
outlet = [1, 1] * s;

% Generate random points within the bounds
capillari_points = s * rand(N, 2);

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

%% Finds the distance between two points
function d = distance(point1, point2)
    d = sqrt((point2(1) - point1(1))^2 + (point2(2) - point1(2))^2);
end

%% Function to plot the channel between two points
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