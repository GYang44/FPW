%% plot distance from course, return distance to the course and distance traveled respectively.
function [d, odm] = courseError(userPath, course)
if size(course,1) < 2
    error("course has to include at least 2 waypoints");
end
d = zeros([size(userPath, 1)-1,1]);
odm = zeros([size(userPath, 1),1]);
numWaypoint = userPath(1,7)+1;
for i=1:(size(userPath, 1)-1)
    nextWaypoint = numWaypoint - userPath(i,7);
    if nextWaypoint == 1
        d(i) = pointToLine(course(1,1:2),course(2,1:2),userPath(i,1:2));
    else
        d(i) = pointToLine(course(nextWaypoint-1,1:2),course(nextWaypoint,1:2),userPath(i,1:2));
    end
    odm(i+1) = odm(i) + sqrt(sum((userPath(i,1:2)-userPath(i+1,1:2)).^2));
end