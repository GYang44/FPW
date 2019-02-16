function d = pointToLine(a, b, p)
    if a == b
        error('a, b are the same point')
    end
    if size(a) == size(b) & size(b) == size(p) & size(a) == size(p)
        if size(a) == [1,2]
            a = [a,0];
            b = [b,0];
            p = [p,0];
        elseif size(a) == [1,3]

        else
            error('a,b,p must be 1by2 or 1by3 vectors');
        end
    else
        error('a,b,p must have same dimession');
    end
    % finish checking prerequisite 
    if abs((a-p)* transpose(b-p)) == sqrt(sum((a-p).^2) * sum((b-p).^2))
        d = 0;
    else
        aSubb = a-b;
        aSubp = a-p;
        k = sum(aSubp .* aSubb)/sum(aSubb.^2);
        d = sqrt(sum((k*(b-a)+a-p).^2));
    end
    
end