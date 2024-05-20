clear;
clc;

% Number of generations
N = 100;

% Set the boudnaries of the tree
s = 0.04;
S = s * [1, 0; 0, 1]; %4cm square

% Location of the inlet
inlet = [0, 0];
outlet = [1, 1] * s;

% arterie endpoint arrays
a1 = zeros(N, 2);
a2 = zeros(N, 2);

% Init 1st branch of arterie
a1(1, :) = inlet + [0.99, 0] * S;
a2(1, :) = inlet;

% Init 2nd branch of arterie
a1(2, :) = inlet + [0, 0.99] * S;
a2(2, :) = inlet;

% Filter points
for i = 3:N
    a1(i, :) = rand(1, 2) * S;
    x = a1(i, 1);
    y = a1(i, 2);
    while y >= -x + 0.04
        a1(i, :) = rand(1, 2) * S;
        x = a1(i, 1);
        y = a1(i, 2);
    end
end

% Plot the results for visualization
figure;
hold on;
plot(a1(:, 1), a1(:, 2), 'ro');  % Original points in redlue
plot([0, s], [0, s], 'k-');  % Diagonal line
xlabel('x');
ylabel('y');
title('Points Filtering Based on Diagonal');
axis equal;
hold off;
