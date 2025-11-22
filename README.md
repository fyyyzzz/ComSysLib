# GraphRAG 使用说明

## 1. 简介
基于微软开源的 **GraphRAG**（Graph-based Retrieval-Augmented Generation）构建，结合本地大模型服务，实现文档的知识抽取、图结构索引构建与基于图的问答检索。

项目结构如下：
- **graphrag/** ：GraphRAG 源码目录


---

## 2. 使用流程

### 2.1 启动本地大模型服务（Ollama）
```bash
ollama serve
```
保持该终端运行即可

### 2.2 新建终端，进入源码目录
新建终端后：

```bash
cd /media/inspur/disk/yzfeng_workspace/code/graphrag
```

### 2.3 激活虚拟环境
```bash
conda activate graphrag10
```

### 2.4 创建输入文件夹，初始化项目
> ⚠️ **注意**
>
> 2.4 和2.5 索引部分比较耗时，因此已经在 `rageng` 下完成了一次索引（即完成了GraphRAG前期实体关系提取、社区挖掘、摘要生成，索引的文档是《A Christmas Carol》）。  
> 测试或演示时可以直接跳到 2.6 进行查询。  
> 
> 如果想检索或索引新的文档，请按照 2.4/2.5 的流程，创建新的项目文件夹（如 `test`）进行索引。

创建输入文件夹，用于存放待处理的文档：
```bash
mkdir -p ./rageng/input
```
将待处理的文档放入input目录下即可

初始化项目：
```bash
python -m graphrag init --root ./rageng
```

初始化后，graphrag会在 `rageng` 目录下自动生成：
- **settings.yaml** ：检索、索引等过程的参数配置，后面主要在这里修改索引、检索设置
- **prompts/** ：存放使用大模型进行实体提取、社区挖掘、问题回复的提示词

之后索引的到的实体、关系等都会存放在 `rageng` 目录下

### 2.5 构建索引
实现对input文档的实体关系提取、社区挖掘、摘要生成。

执行索引命令：
```bash
python -m graphrag index --root ./rageng
```

GraphRAG 在索引过程中会自动生成以下目录：
- **rageng/output/** ：检索、索引等过程的参数配置，后面主要在这里修改索引、检索设置。该目录包含以下文件：
  - **documents.parquet**: 输入目录 (`input`) 下的原始文档
  - **text_units.parquet**: 文本单元划分结果，每个文档被拆分为多个小片段
  - **entities.parquet**: 抽取的实体信息
  - **relationships.parquet**: 抽取的实体关系信息
  - **communities.parquet**: 社区划分结果，每个实体/文本单元所属社区
  - **community_reports.parquet**: 社区摘要

- **rageng/cache/** ：索引过程中的缓存
- **rageng/logs/** ：索引过程中的日志

### 2.6 查询
GraphRAG 提供两种查询方式：

| 查询方式 | 参数值 | 特点 |
|---------|---------|---------|
| **local**  | `--method local`  | 基于底层知识图谱，检索相关实体、社区、文本块 |
| **global** | `--method global` | 检索高层社区摘要 |

#### 示例1（local 查询）

```bash
graphrag query --root ./rageng --method local --query "Who is Scrooge, and what are his main relationships?"
```
#### 示例2（global 查询）

```bash
graphrag query --root ./rageng --method global --query "What are the top themes in this story?"
```



