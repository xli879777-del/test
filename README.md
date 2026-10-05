# test

面向 `xli879777-del/test` 空仓库的 Python 命令行项目骨架。

## 技术栈假设

- 暂按本地数据处理工具设计；当前没有已确认的业务需求。
- Python 3.11 或以上，命令行入口 `python -m app`。
- 只用 Python 标准库，无第三方运行或测试依赖，无需执行 `pip install`。
- 示例功能：读取 CSV，汇总指定金额列，将结果输出为 JSON。
- 源码直接运行，不发布为 Python 安装包，因此暂不配置 `pyproject.toml`、构建后端或锁文件。

## 文件结构

| 路径 | 用途 |
| --- | --- |
| `README.md` | 使用说明 |
| `requirements.txt` | 明确当前没有第三方依赖 |
| `.gitignore` | 排除缓存、虚拟环境及本地数据 |
| `.gitattributes` | 统一文本换行符 |
| `app/__init__.py` | Python 包说明 |
| `app/__main__.py` | 命令行入口、参数解析与错误输出 |
| `app/core.py` | CSV 校验和汇总逻辑 |
| `examples/data.csv` | 可直接运行的虚构示例数据 |
| `tests/test_core.py` | 数据边界及命令行行为测试 |

## 环境和依赖

安装 Python 3.11+；提交代码另需 Git。`argparse`、`csv`、`decimal`、`json`、`pathlib` 和 `unittest` 均随 Python 提供。

以下命令都在包含本文件的项目根目录执行。macOS/Linux 使用 `python3`；Windows 可使用 `py -3` 替代命令中的 `python3`。请先用 `python3 --version` 或 `py -3 --version` 确认实际版本。

## 最快运行

先获取项目：

```bash
git clone https://github.com/xli879777-del/test.git
cd test
```

如果使用下载的文件包，解压后进入 `test-starter` 文件夹即可。然后运行：

```bash
python3 -m app --input examples/data.csv
```

预期输出：

```json
{
  "column": "amount",
  "rows": 3,
  "total": "140.75"
}
```

更多命令：

```bash
python3 -m app --help
python3 -m app --input examples/data.csv --column amount
python3 -m unittest discover -s tests -v
```

自定义数据放入本地 `data/` 目录后运行，例如：

```bash
python3 -m app --input data/my-data.csv --column amount
```

如需保存终端输出，可使用 shell 重定向：

```bash
python3 -m app --input examples/data.csv > result.json
```

重定向由 shell 处理，同名输出文件会被覆盖；不要将输出路径设为输入文件。

## 输入与输出约定

- CSV 使用逗号分隔、UTF-8 编码，兼容 UTF-8 BOM。Excel 文件请先另存为 CSV UTF-8；本示例不读取 `.xlsx`。
- 必须有非空、唯一的表头；表头按原文精确匹配，默认汇总 `amount` 列。
- 每条记录的字段数必须与表头一致。纯空行由 CSV 读取器忽略。
- 金额支持正负十进制数与科学计数法；不接受空值、货币符号、千分位逗号、NaN 或 Infinity。
- 逐行累加，使用 28 位有效数字精度；如果加法会丢失精度，直接报错，不默默舍入。不限定两位小数。
- `rows` 是有效数据记录数；只有表头时返回 `rows: 0`、`total: "0"`。
- `total` 是 JSON 字符串，保留十进制表示，避免下游立即转换成二进制浮点数。
- 成功退出码为 0；数据、文件或参数错误退出码为 2。错误写入标准错误，失败时不输出部分汇总结果。

## 最短本地提交并推送

下载文件包并解压，在 `test-starter` 文件夹中打开终端。以下步骤适用于该文件夹尚未初始化 Git，且 GitHub 远程仓库仍为空的情况：

```bash
git init -b main
git add .
git commit -m "chore: initialize Python CSV starter"
git remote add origin https://github.com/xli879777-del/test.git
git push -u origin main
```

如首次提交提示没有作者身份，先执行下列命令，替换为自己的名字与邮箱，再重新执行提交和推送：

```bash
git config user.name "你的名字"
git config user.email "你的邮箱"
```

HTTPS 推送需完成本机 GitHub 身份验证；账号具有仓库权限，不代表本机已经登录。若提示远程已有提交，先读取远程变更再合并，不要强制推送。若从 `git clone` 得到工作目录，则不需要再次执行 `git init` 或 `git remote add`。

## 扩展位置

在 `app/core.py` 添加数据处理逻辑，在 `app/__main__.py` 添加参数；新功能的输入输出边界放在 `tests/` 中验证。引入第三方依赖时再更新 `requirements.txt`。真实数据可放入已忽略的 `data/`，可提交的演示数据放入 `examples/`。

标准库参考：[argparse](https://docs.python.org/3.11/library/argparse.html)、[csv](https://docs.python.org/3.11/library/csv.html)、[decimal](https://docs.python.org/3.11/library/decimal.html)。
