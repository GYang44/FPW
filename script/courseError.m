%% plot distance from course, return distance to the course and distance traveled respectively.
function [d, odm] = courseError(userPath, course)
d = zeros([size(userPath, 1)-1,1]);
odm = zeros([size(userPath, 1),1]);
wayPointIndex = 1;
for i=1:(size(userPath, 1)-1)
    d(i) = pointToLine([course(wayPointIndex,:)],[course(wayPointIndex+1,:)],userPath(i,1:3));
    odm(i+1) = odm(i) + sqrt(sum((userPath(i,1:3)-userPath(i+1,1:3)).^2));
    if sum((course(wayPointIndex+1,:) - userPath(i,1:3)).^2) < 1.5
        if wayPointIndex < size(course,1) - 1
            wayPointIndex = wayPointIndex + 1;
        end
    end
end