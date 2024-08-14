% 定义每个basin的K值
K_values = [
3.11E-06,
4.40E-06,
5.53E-06,
2.29E-06,
2.94E-06,
4.32E-06,
2.42E-06,
1.38E-06,
2.03E-06,
2.68E-06,
1.77E-06,
1.84E-06,
4.67E-06,
2.99E-06,
1.10E-06,
7.94E-06,
5.24E-06,
6.25E-06,
3.14E-06,
4.60E-06,
2.51E-06,
1.48E-06,
2.11E-06,
4.08E-06,
];

Ao = 1;
mn = 0.42;

% 定义Excel文件名
excelFileName = 'D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\Min-inversion\new inversion 0604\反演结果.xlsx';

% 初始化存储结果的单元数组
AllResults = cell(24, 1);
figure(1)
t = tiledlayout(5, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
set(gcf,'Position', [100, 100, 800, 4000]);
figureCount = 1;  % 记录当前的图形窗口数量
subplotCount = 0;  % 记录当前图形窗口中的子图数量

% 循环遍历每个basin
for i = 1:24
    % 动态构造变量名字符串
    varName = sprintf('DEMc_%d', i);

    % 使用eval动态引用变量
    DEM = eval(varName);
    DEM = fillsinks(DEM)

    % 调用linear_inversion_block_uplift函数,使用对应的DEM文件
    [A,Umod,S,Schi,chi_steps,res] = linear_inversion_block_uplift(DEM, 'n_inc', 15, 'mn', 0.42, 'crita',1e6);

    % 创建一个结构体存储所有相关数据
    results_struct = struct('A', A, 'Umod', Umod, 'S', S, 'Schi', Schi, 'chi_steps', chi_steps, 'res', res);

    % 保存结果到单元数组
    AllResults{i} = results_struct;

    % 从结构体中读取数据
    K = K_values(i);
    xData = AllResults{i}.chi_steps ./ (K * Ao^mn) ./ 1e6;
    yData = AllResults{i}.Umod .* (K * Ao^mn) .* 1000;

    % 如果当前图形窗口中的子图数量超过5，就创建一个新的图形窗口
    if subplotCount > 5
        figureCount = figureCount + 1;
        figure(figureCount);
        subplotCount = 1;
    end 
    %绘制第i行第1列子图,observed and best-fit model results
    nexttile(t, i*2-1);
    Sz = DEM.Z(S.IXgrid);
    table = sortrows([Sz,Schi]);
    z_vec = table(:,1)-min(table(:,1));
    chi_vec = table(:,2);
    plot(chi_vec,z_vec,'.','color',[0.5 0.5 0.5]); hold on
    plot(chi_vec,A*Umod,'k.');%,'color',Pcols(k,:));
    set(gca, 'linewidth', 1.5, 'fontsize', 12, 'FontAngle', 'italic')
    xlabel('\chi','FontWeight','bold','FontAngle','italic'); 
    ylabel('elevation (m)','FontAngle','italic');
    lgd = legend({'observed','modeled'});
    set(lgd,'box','off')
    set(lgd, 'location', 'northwest')
    title(['basin ',num2str(i)]);


    %绘制第i行第2列子图,tau vs. uplift rate
    ax(i)= nexttile(t,i*2)
    stairs(chi_steps./(K*Ao^mn)./1e6, Umod.*(K*Ao^mn).*1000,'color',[0 0 0],'lineWidth',2);
    xlabel('\tau (Myr)','FontAngle','italic'); 
    ylabel('Uplift rate (mm/yr)','FontAngle','italic');
    xlim(ax(i), [0, 2]);
    ylim(ax(i), [0, 1.8]);
    % 只显示左侧和下侧的刻度
    set(ax(i), 'linewidth', 1.5, 'fontsize', 12, 'FontAngle', 'italic')
    set(ax(i), 'Box', 'off'); 
    set(ax(i), 'YTickMode', 'auto', 'XTickMode', 'auto');  % 自动刻度
    ax(i).XAxisLocation = 'bottom';  % 确保X轴只在底部显示
    ax(i).YAxisLocation = 'left';    % 确保Y轴只在左侧显示
    %创建双y轴
    yyaxis right
    plot(chi_steps, Umod, 'Color', 'none', 'LineWidth', 2);  % 在右侧y轴上绘制Umod数据
    set(ax(i), 'YColor', 'k');  % 设置右侧y轴的颜色
    ylabel('Ksn','FontAngle','italic','Color','k');  % 设置右侧y轴的标签
    set(ax(i),'Box','off');  % 关闭右侧y轴的边框
    %链接左右两个y轴的范围
    linkprop([ax(i), ax(i).YAxis.Parent], 'YLim')
    % 创建一个新的坐标轴，共享 y 轴，但有不同的 x 轴
    ax(i*2) = axes('Position', ax(i).Position, 'XAxisLocation', 'top', 'Color', 'none', 'YTick', []);
    linkprop([ax(i), ax(i*2)], 'YLim');  % 链接两个坐标轴的 Y 轴范围
    ax(i*2).XLim = [min(chi_steps) max(chi_steps)];  % 设置上方 x 轴的范围为 chi_steps 的范围
    line(chi_steps, Umod.*(K*Ao^mn).*1000, 'Parent', ax(i*2), 'Color', 'none');  % 绘制相同的数据，但不显示
    xlabel(ax(i*2), '\chi','FontWeight','bold');  % 设置上方 x 轴的标签
    set(ax(i*2), 'linewidth', 1.5, 'fontsize', 12, 'FontAngle', 'italic')
    % 将上方 x 轴的标签移动到轴下方
    ax(i*2).XLabel.Position(2) = 1*ax(i*2).YLim(2); 
    ax(i*2).XLabel.VerticalAlignment = 'top';  % 调整垂直对齐方式
    subplotCount = subplotCount + 1;

    % 创建数据数组
    data= [xData(:), yData(:)];

    % 创建并更新结构体以存储所有相关数据和新生成的数据
    results_struct = struct('A', A, 'Umod', Umod, 'S', S, 'Schi', Schi, 'chi_steps', chi_steps, 'res', res, 'xData', xData, 'yData', yData, 'data', data);
    
    % 保存结果到单元数组
    AllResults{i} = results_struct;

    % 动态生成每个basin的工作表名
    sheetName = sprintf('basin_%d', i);
    
    % 将数据写入Excel文件，每个basin一个工作表
    writematrix(AllResults{i}.data, excelFileName, 'Sheet', sheetName);
end
print(figure(1),'D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\Min-inversion\new inversion 0604\inversion.svg', '-dsvg', '-r300','-painters');
