# Feishu Knowledge Import

适用：将文章链接、Markdown 草稿或文件夹扫描结果导入飞书知识库。

## 标准流程

1. **先统一输入**
   - 先把外部内容整理成共享的 `ImportDraft`
   - 不要把来源解析逻辑直接写进目标端适配器

2. **再构造飞书负载**
   - 目标端只负责把 `ImportDraft` 转成飞书可接受的结构
   - 保留标题、正文、标签、来源、图片相关信息

3. **最后做一次同步记录**
   - 成功后记录 `source_id`、`content_hash`、`remote_id`、`remote_url`
   - 这样一次性导入和增量同步都能复用同一套状态

## 推荐环境变量

- `FEISHU_IMPORT_ENDPOINT`
  - 飞书知识库导入接口地址
- `FEISHU_ACCESS_TOKEN`
  - 如果接口需要 Bearer token
- `FEISHU_APP_ID`
  - 如果后续要补 OAuth / app auth
- `FEISHU_APP_SECRET`
  - 如果后续要补 OAuth / app auth

## 备注

- 第一版优先保留可配置传输层，不把接口写死在源代码里
- 如果飞书官方插件的导入形态变化，只需要替换 transport 和 payload builder，不要重写来源层
