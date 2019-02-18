function void = plotTrack(path, course, vectorRate, vectorLength)
% This function plot the path user took vs designated course path should be a n by 6 matrix, course should be a 3 by 6 matrix
hold on;
plot(path(:,1),path(:,2),'r');
dirX = cos(path(:,6)/180*pi+pi/2);
dirY = sin(path(:,6)/180*pi+pi/2);
quiver(path(1:vectorRate:end,1), path(1:vectorRate:end,2), dirX(1:vectorRate:end), dirY(1:vectorRate:end), vectorLength, 'r');
plot(course(:,1), course(:,2),'-b.','MarkerSize',12);
axis equal
hold off;
end