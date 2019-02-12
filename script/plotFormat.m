plotTrack(JWhelan2, path, 30, 0.5);
xlim([-10,40]);
ylim([-10,15]);

graph = gca
figure = gcf
graph.FontSize = 9
graph.FontWeight = 'normal'
graph.TitleFontWeight = 'normal'
xlabel ('Meter')
legend('path','heading','course','Location','northwest')
title('Test Subject 4')
grid on;
set(gcf, 'position', [0,0,450,250]);
