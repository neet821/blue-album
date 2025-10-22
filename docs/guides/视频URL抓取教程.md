# 🎬 视频URL抓取完整教程

## 方法一：浏览器开发者工具（推荐）

### Chrome/Edge 步骤：

1. **打开开发者工具**
   - Windows: 按 `F12` 或 `Ctrl + Shift + I`
   - Mac: 按 `Cmd + Option + I`

2. **切换到 Network（网络）标签**
   - 点击顶部的 "Network" 标签
   - 勾选 "Preserve log"（保留日志）
   - 清空当前记录（点击 🚫 图标）

3. **过滤媒体资源**
   - 点击过滤栏的 "Media"（媒体）选项
   - 或在搜索框输入: `.m3u8` 或 `.mp4`

4. **播放视频**
   - 刷新页面并播放视频
   - 观察 Network 面板中的请求

5. **找到视频URL**
   - 查找以下特征的请求：
     - 文件名包含 `.mp4`, `.m3u8`, `.ts`, `.flv`
     - Type 列显示 `media` 或 `video`
     - Size 较大（通常几MB到几百MB）
   
6. **复制URL**
   - 右键点击该请求
   - 选择 "Copy" → "Copy link address"
   - 粘贴到同步观影的"视频链接"输入框

---

## 方法二：查看页面源代码

### 适用场景：
视频URL直接写在HTML中的简单网站

### 步骤：
1. 在视频页面右键 → "查看网页源代码"
2. 按 `Ctrl + F` 搜索关键词：
   - `mp4`
   - `m3u8`
   - `video`
   - `src="`
3. 找到类似这样的代码：
   ```html
   <video src="https://example.com/video.mp4">
   <source src="https://example.com/video.m3u8" type="application/x-mpegURL">
   ```
4. 复制 `src` 属性中的URL

---

## 方法三：使用浏览器插件

### 推荐插件：

#### 1. **Stream Video Downloader**
- Chrome 商店搜索安装
- 自动检测页面中的视频
- 点击插件图标即可看到视频URL

#### 2. **Video DownloadHelper**（Firefox）
- 支持多种视频网站
- 自动捕获视频流

#### 3. **Video Downloader Professional**
- 支持 Chrome/Edge
- 一键复制视频URL

---

## 方法四：视频平台的分享链接

### 支持的平台：

#### YouTube
```
普通链接：https://www.youtube.com/watch?v=VIDEO_ID
嵌入链接：https://www.youtube.com/embed/VIDEO_ID
```

#### Bilibili（B站）
```
普通链接：https://www.bilibili.com/video/BV1xx411c7xD
嵌入链接：https://player.bilibili.com/player.html?bvid=BV1xx411c7xD
```

#### Vimeo
```
普通链接：https://vimeo.com/123456789
嵌入链接：https://player.vimeo.com/video/123456789
```

#### 优酷/爱奇艺/腾讯视频
- 点击"分享"按钮
- 选择"复制链接"

---

## 方法五：使用命令行工具（高级）

### youtube-dl（支持上千个网站）

#### 安装：
```bash
# Windows
pip install youtube-dl

# 或使用 yt-dlp（更新更快）
pip install yt-dlp
```

#### 获取视频URL：
```bash
# 获取最佳质量的直链
youtube-dl -g "https://www.youtube.com/watch?v=VIDEO_ID"

# 或使用 yt-dlp
yt-dlp -g "https://www.bilibili.com/video/BV1xx411c7xD"
```

#### 输出示例：
```
https://r4---sn-ci5gup-qxay.googlevideo.com/videoplayback?expire=...
```

---

## 常见视频格式说明

| 格式 | 说明 | 浏览器支持 |
|------|------|------------|
| `.mp4` | 最常见的视频格式 | ✅ 所有浏览器 |
| `.m3u8` | HLS流媒体索引文件 | ✅ 现代浏览器 |
| `.ts` | HLS流媒体分片 | ⚠️ 需配合m3u8使用 |
| `.flv` | Flash视频格式 | ❌ 需转换 |
| `.webm` | 开源视频格式 | ✅ Chrome/Firefox |

---

## 针对同步观影功能的建议

### ✅ 推荐使用的URL类型：

1. **直链MP4**（最佳）
   ```
   https://example.com/video.mp4
   ```
   - 兼容性最好
   - 支持进度控制

2. **HLS流（.m3u8）**（推荐）
   ```
   https://example.com/playlist.m3u8
   ```
   - 支持自适应码率
   - 主流视频网站都用这种

3. **视频平台嵌入链接**（可用）
   ```
   https://www.youtube.com/embed/VIDEO_ID
   https://player.bilibili.com/player.html?bvid=BV_ID
   ```
   - 需要使用 iframe 嵌入
   - 可能受跨域限制

### ❌ 不推荐的URL：
- 需要登录才能访问的视频
- 有地区限制的视频
- 有防盗链的视频
- 需要付费的视频

---

## 实战示例：抓取B站视频URL

### 步骤详解：

1. **打开B站视频页面**
   ```
   https://www.bilibili.com/video/BV1xx411c7xD
   ```

2. **按F12打开开发者工具**

3. **切换到Network标签 → Media**

4. **播放视频**

5. **找到m3u8文件**
   - 查找类似 `index.m3u8` 的请求
   - URL类似：`https://cn-xxxxxx.bilivideo.com/xxxxx/index.m3u8`

6. **复制URL**
   - 右键 → Copy → Copy link address

7. **粘贴到同步观影的输入框**

---

## 测试视频URL是否有效

### 方法1：浏览器直接访问
- 在地址栏粘贴URL
- 如果能播放或下载，说明有效

### 方法2：使用video标签测试
```html
<video src="你的URL" controls></video>
```

### 方法3：用curl测试
```bash
curl -I "你的URL"
```
- 返回 200 OK 说明有效
- 返回 403/404 说明无效

---

## 常见问题排查

### ❌ 视频无法播放
**可能原因：**
1. **跨域限制（CORS）**
   - 症状：控制台显示 "CORS policy" 错误
   - 解决：使用相同域名的视频，或者使用代理

2. **防盗链**
   - 症状：单独访问URL返回403
   - 解决：需要带上正确的 Referer 请求头

3. **URL已过期**
   - 症状：之前能播放，现在不行了
   - 解决：重新抓取最新的URL

4. **需要认证**
   - 症状：返回401或跳转到登录页
   - 解决：使用公开的视频URL

### ✅ 解决方案
- 优先使用大型视频平台的公开视频
- 使用稳定的CDN直链
- 避免使用临时URL

---

## 推荐的测试视频URL

### 公开测试视频：
```
# Big Buck Bunny（开源测试视频）
https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4

# Sintel（开源电影）
http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4

# 4K测试视频
https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4
```

---

## 高级技巧：处理加密视频

### HLS加密视频（.m3u8 + AES）
- 视频被分成多个 .ts 文件
- 需要 key 才能解密
- 浏览器会自动处理，无需手动解密

### DRM加密视频（Widevine/FairPlay）
- 大型视频平台常用（Netflix、Disney+等）
- **无法直接抓取URL使用**
- 建议：使用平台提供的分享功能

---

## 总结

| 方法 | 难度 | 成功率 | 推荐度 |
|------|------|--------|--------|
| 浏览器开发者工具 | ⭐ | 90% | ⭐⭐⭐⭐⭐ |
| 查看源代码 | ⭐ | 60% | ⭐⭐⭐ |
| 浏览器插件 | ⭐ | 80% | ⭐⭐⭐⭐ |
| 平台分享链接 | ⭐ | 95% | ⭐⭐⭐⭐⭐ |
| youtube-dl | ⭐⭐⭐ | 85% | ⭐⭐⭐⭐ |

**最推荐：浏览器开发者工具 + 平台分享链接**

---

## 在同步观影中使用

1. **创建房间时选择"外部链接"模式**
2. **在"视频链接"输入框粘贴抓取的URL**
3. **点击"创建房间"**
4. **分享房间代码给朋友**
5. **一起享受同步观影！**

---

## 技术支持

如果遇到问题：
1. 检查浏览器控制台的错误信息
2. 确认视频URL是否有效
3. 尝试使用不同的视频源
4. 查看 Network 标签的详细请求信息
