# 如何将 omniedge 上传到 PyPI

## 前置准备

1. **注册 PyPI 账号**
   - 访问 https://pypi.org/account/register/ 注册账号
   - 如果要在测试环境先测试，访问 https://test.pypi.org/account/register/

2. **安装必要的工具**
   ```bash
   pip install build twine
   ```

3. **配置 API Token（推荐）**
   - 登录 PyPI 后，访问 https://pypi.org/manage/account/token/
   - 创建一个新的 API Token
   - 保存 token（格式：`pypi-...`）

## 构建和上传步骤

### 1. 构建分发包

```bash
# 清理之前的构建文件
rm -rf dist/ build/ *.egg-info

# 构建分发包
python -m build
```

这会在 `dist/` 目录下生成 `.whl` 和 `.tar.gz` 文件。

> 使用 `make` 一键执行：
> ```bash
> make build   # 自动清理并构建
> ```

### 2. 检查分发包（可选但推荐）

```bash
# 检查分发包是否有问题
twine check dist/*
```

### 3. 上传到 PyPI

#### 方法一：使用 API Token（推荐）

```bash
# 上传到正式 PyPI
twine upload dist/*

# 或者先上传到测试 PyPI 进行测试
twine upload --repository testpypi dist/*
```

系统会提示输入：
- Username: `__token__`
- Password: 你的 API Token（以 `pypi-` 开头）

> 推荐先运行 `make publish-test` 验证流程，通过后使用 `make publish` 发布到正式 PyPI。

#### 方法二：使用用户名和密码

```bash
twine upload dist/*
```

系统会提示输入 PyPI 的用户名和密码。

> 如果已经配置好 API Token，直接运行 `make publish` 即可完成清理、构建、检查和正式上传。

### 4. 验证上传

上传成功后，你的包将可以在以下地址访问：
- https://pypi.org/project/omniedge/

用户可以通过以下命令安装：
```bash
pip install omniedge
```

## 更新版本

每次更新版本时：

1. 在 `pyproject.toml` 中更新 `version` 字段
2. 在 `omniedge/__init__.py` 中更新 `__version__`
3. 重新执行构建和上传步骤

## 注意事项

- 确保版本号遵循 [语义化版本](https://semver.org/) 规范
- 上传到正式 PyPI 后，版本号不能重复使用
- 建议先在测试 PyPI 上测试：`twine upload --repository testpypi dist/*`
- 测试安装：`pip install -i https://test.pypi.org/simple/ omniedge`

