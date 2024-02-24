#assert False, ('请用 pip install vhmap numpy scipy 命令安装必要的依赖包， 然后直接删掉这行代码')

import numpy as np
from scipy.integrate import ode
from UTIL.tensor_ops import distance_matrix, repeat_at, delta_matrix

N体 = 3
引力常量G = 1
时间步长 = 0.005

大小 = [0.05 for _ in range(N体)]
颜色 = ['Red', 'Blue', 'Green']
位置 = np.array([  [-1, 0,0],  [1, 0,0],  [0,0,0]]); assert N体==3
v1 = 0.6150407229; v2 = 0.5226158545
速度 = np.array([[v1, v2,0], [v1, v2,0], [-2*v1, -2*v2,0]])
质量 = np.array([1 for _ in range(N体)])
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
        if 计数%6 == 0:
            for 天体编号 in range(N体):
                可视化桥.发送几何体(
                    'sun|%d|%s|%.2f'%(天体编号,颜色[天体编号], 大小[天体编号]),
                    位置_[天体编号, 0], 位置_[天体编号, 1], 位置_[天体编号, 2], 0, 0, 0, # 物体的六自由度信息
                    track_n_frame = 1200 # 绘制物体轨迹，（1000关键帧）
                )
            可视化桥.结束关键帧()
        print('\r %.4f'%(积分器.t + 时间步长), end='', flush=True ) 