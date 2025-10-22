# 前端依赖安装说明

## 安装同步观影功能所需依赖

```bash
npm install socket.io-client@^4.7.2
```

## 完整的 package.json 依赖 (仅供参考)

```json
{
  "name": "blue-local-frontend",
  "version": "1.0.0",
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.5.0",
    "element-plus": "^2.4.0",
    "marked": "^9.0.0",
    "socket.io-client": "^4.7.2"
  }
}
```

## 验证安装

```bash
npm list socket.io-client
```

应显示:
```
└── socket.io-client@4.7.2
```
