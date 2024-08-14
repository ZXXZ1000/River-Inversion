DEM=GRIDobj("D:\OneDrive - zju.edu.cn\文档\ArcGIS\COPDEM_MIN_UTM_clip4.tif");
DEM=resample(DEM,round(DEM.cellsize),'bicubic');
S = shaperead("D:\OneDrive - zju.edu.cn\文档\MATLAB 代码\河流反演\test1\basin_shp.shp");

% 循环处理每个多边形
for i = 1:length(S)

% 提取当前多边形的坐标
% 将地理坐标转换为像素坐标。这可能需要根据DEM的地理参考系统调整
x = S(i).X;
y = S(i).Y;

% 移除NaN值
validIndices = ~isnan(x) & ~isnan(y);
x = x(validIndices);
y = y(validIndices);

% 转换经纬度坐标到像素坐标（这里需要根据实际DEM的地理参考来调整）
col = (x - DEM.refmat(3,1)) / DEM.cellsize;
row = (y - DEM.refmat(3,2)) / -DEM.cellsize;

% 使用poly2mask创建掩模。注意：poly2mask要求坐标是行列格式，并且是图像坐标系统（左上角为原点）
% 需要DEM的尺寸来确定掩模的大小
MASK = poly2mask(col, row, DEM.size(1), DEM.size(2));

% 应用掩模并裁剪
DEMc = DEM;
DEMc.Z(~MASK) = NaN;

% 动态创建变量名并保存裁剪后的DEM数据
    varName = ['DEMc_', num2str(i)];
    eval([varName, ' = crop(DEMc);']);

    figure;
    imageschs(eval(varName));
    title(['DEMc_', num2str(i)]);

end
close all


