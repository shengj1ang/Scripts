import numpy as np
from scipy.integrate import ode
from UTIL.tensor_ops import distance_matrix, repeat_at, delta_matrix

N体 = 59 # 79
引力常量G = 16
时间步长 = 0.001

大小 = [0.2 for _ in range(N体)]
颜色 = ['Red', 'Blue', 'Green'] + ["lightpink", "pink", "crimson", "lavenderblush", "palevioletred", "hotpink", "deeppink", "mediumvioletred", "orchid", "thistle", "plum", "violet", "magenta", "fuchsia", "darkmagenta", "purple", "mediumorchid", "darkorchid", "indigo", "blueviolet", "mediumpurple", "mediumslateblue", "slateblue", "darkslateblue", "lavender", "ghostwhite", "blue", "mediumblue", "midnightblue", "darkblue", "navy", "royalblue", "cornflowerblue", "lightsteelblue", "lightslategray", "slategray", "aliceblue", "steelblue", "lightskyblue", "skyblue", "deepskyblue", "lightblue", "powderblue", "cadetblue", "azure", "lightcyan", "paleturquoise", "cyan", "aqua", "darkturquoise", "darkslategray", "darkcyan", "teal", "mediumturquoise", "lightseagreen", "turquoise", "mediumaquamarine", "mediumspringgreen", "mintcream", "springgreen", "seagreen", "honeydew", "lightgreen", "palegreen", "darkseagreen", "limegreen", "lime", "forestgreen", "green", "darkgreen", "chartreuse", "lawngreen", "greenyellow", "olivedrab", "beige", "lightgoldenrodyellow", "ivory", "lightyellow", "yellow", "olive", "darkkhaki", "lemonchiffon", "khaki", "gold", "goldenrod", "floralwhite", "oldlace", "wheat", "moccasin", "orange", "papayawhip", "blanchedalmond", "navajowhite", "antiquewhite", "bisque", "darkorange", "linen", "peru", "peachpuff", "sandybrown", "chocolate", "saddlebrown", "seashell", "sienna", "lightsalmon", "coral", "orangered", "darksalmon", "tomato", "mistyrose", "salmon", "snow", "lightcoral", "rosybrown", "indianred", "red", "brown", "firebrick", "darkred", "maroon", "white", "whitesmoke", "gainsboro", "lightgrey", "silver", "darkgray", "gray", "dimgray", "black", ]

dTheta = 2 *np.pi /(N体-1)
相位 = [dTheta*i for i in range(N体-1)] + [0]
位置 = [[np.cos(相位[i]), np.sin(相位[i]), (-1)**i] for i in range(N体-1)] + [[0,0,0]]; 位置 = np.array(位置)*20
速度 = [[np.cos(相位[i]+np.pi/2), np.sin(相位[i]+np.pi/2), 0] for i in range(N体-1)] + [[0,0,0]]; 速度 = np.array(速度)*7
质量 = [1.5 for _ in range(N体-1)] + [200]; 质量 = np.array(质量)

# 位置 = (np.random.rand(N体, 3) * 2 - 1) * 5   # 3维, [-1~1]
# 速度 = (np.random.rand(N体, 3) * 2 - 1) * 1

整合状态向量 = lambda 位置, 速度: np.concatenate((位置.reshape(-1), 速度.reshape(-1)))
分离状态向量 = lambda 向量: 向量.reshape(2, N体, 3)

def 状态方程(时间, 状态向量):
    位置, 速度 = 分离状态向量(状态向量)
    # 众所周知，牛顿万有引力公式为 F = G*M*m / r^2, 加速度为 a = F/m
    # 第一步 计算r^2矩阵
    距离矩阵 = distance_matrix(位置) # 一个 N体*N体 矩阵
    距离矩阵平方 = 距离矩阵 * 距离矩阵.T # 距离矩阵的转置依然是自己
    # 第二步 计算M*m矩阵
    质量矩阵 = repeat_at(tensor=质量, insert_dim=-1, n_times=N体)
    Mm矩阵 = 质量矩阵 * 质量矩阵.T  # 转置，相乘
    # 第三步 计算引力（标量）： F = G*M*m / r^2
    引力标量矩阵 = 引力常量G * Mm矩阵 / (距离矩阵平方 + 1e-10) # 防止除零错误
    for i in range(N体): 引力标量矩阵[i,i] = 0 # 忽略天体对自己的引力
    # 第四步 计算加速度（向量）
    引力方向 = delta_matrix(位置)   # 需要归一化 -> 引力方向的单位向量
    引力方向 = 引力方向 / (np.linalg.norm(引力方向, axis=-1, keepdims=True) + 1e-10) # 防止除零错误
    引力 = 引力方向 * repeat_at(tensor=引力标量矩阵, insert_dim=-1, n_times=3)  # 这里的 3 指3维空间！
    引力合力 = 引力.sum(1) # 力的合成 （矢量加法）
    加速度 = 引力合力 / repeat_at(tensor=质量, insert_dim=-1, n_times=3)  # 这里的 3 指3维空间！
    assert (质量 != 0).any()  # 防止除零错误
    位置导数 = 速度
    速度导数 = 加速度
    return 整合状态向量(位置导数, 速度导数)

计数 = 0

if __name__ == '__main__':
    from VISUALIZE.mcom import mcom
    可视化桥 = mcom(path='./TEMP/', draw_mode='Threejs')
    可视化桥.初始化3D()
    可视化桥.设置样式('many star')
    可视化桥.其他几何体之旋转缩放和平移('sun', 'SphereGeometry(1)',  0,0,0,  1,1,1,  0,0,0)
    # 初始化积分器
    积分器 = ode(状态方程).set_integrator('dop853')

    初始状态向量 = 整合状态向量(位置, 速度)
    积分器.set_initial_value(初始状态向量, 0)

    while 积分器.successful() and 积分器.t < 100:
        新状态向量 = 积分器.integrate(积分器.t + 时间步长); 计数 += 1
        位置, 速度 = 分离状态向量(新状态向量)
        位置_ = 位置.real # 取出复数的实部
        if 计数%16 == 0:
            for 天体编号 in range(N体):
                可视化桥.发送几何体(
                    'sun|%d|%s|%.2f'%(天体编号,颜色[天体编号], 大小[天体编号]),
                    位置_[天体编号, 0], 位置_[天体编号, 1], 位置_[天体编号, 2], 0, 0, 0, # 物体的六自由度信息
                    track_n_frame = 2560 # 绘制物体轨迹，（1000关键帧）
                )
            可视化桥.结束关键帧()
        print('\r %.4f'%(积分器.t + 时间步长), end='', flush=True )
