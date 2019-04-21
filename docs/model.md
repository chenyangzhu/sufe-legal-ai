
## law.model
#### `class` law.model.basemodel()
所有的model都使用了basemodel作为底层，实现以下功能：
- `fit(X,y)`
- `predict(X)`
- `store()` 存储已经训练过的模型
- `read()`读取先前训练过的模型
