# MuMax3 x 方向磁滞回线示例

这是一个简洁的 MuMax3 示例仓库，用于生成 x 方向外场扫描下的准静态磁化数据，并绘制 `mx-B_extx (T)` 磁滞回线。

## 文件说明

- `demo1.mx3`：MuMax3 仿真脚本
- `demo1.out/`：当前仿真的输出目录
- `plot_hysteresis_x.py`：从 `demo1.out/table.txt` 绘制 x 方向磁滞回线

## 仿真设置

- 网格：`64 x 32 x 16`
- 尺寸：`128 nm x 64 nm x 32 nm`
- `Msat = 800e3 A/m`
- `Aex = 13e-12 J/m`
- `alpha = 0.02`
- `Ku1 = 0`
- `anisU = (1, 0, 0)`

外场沿 x 方向扫描：

- `Bmax = 0.5 T`
- `dB = 0.01 T`
- 从 `+0.5 T` 扫到 `-0.5 T`，再扫回 `+0.5 T`
- 每个场点使用 `Minimize()` 做准静态求解

## 运行方法

运行 MuMax3：

```powershell
mumax3 -f demo1.mx3
```

绘制磁滞回线：

```powershell
py plot_hysteresis_x.py
```

可选保存图片：

```powershell
py plot_hysteresis_x.py demo1.out/table.txt -o hysteresis_x.png
```

## 输出说明

`demo1.out/table.txt` 包含外场和磁化数据。`plot_hysteresis_x.py` 会读取其中的 `mx ()` 和 `B_extx (T)` 两列，并绘制 x 方向磁滞回线。
