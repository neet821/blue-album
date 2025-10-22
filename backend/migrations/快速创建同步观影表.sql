-- ================================================
-- 快速检查和创建同步观影表
-- 数据库: blue_local_db
-- ================================================

-- 1. 使用正确的数据库
USE blue_local_db;

-- 2. 检查表是否已存在
SELECT 
    TABLE_NAME,
    TABLE_ROWS,
    CREATE_TIME
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'blue_local_db' 
  AND TABLE_NAME IN ('sync_rooms', 'sync_room_members', 'sync_room_messages');

-- 3. 如果表不存在，执行以下创建语句
-- （如果表已存在，下面的语句不会执行，因为有 IF NOT EXISTS）

-- 创建同步观影房间表
CREATE TABLE IF NOT EXISTS sync_rooms (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '房间ID',
    room_code VARCHAR(20) UNIQUE NOT NULL COMMENT '房间代码(6位)',
    room_name VARCHAR(100) NOT NULL COMMENT '房间名称',
    host_user_id INT NOT NULL COMMENT '房主用户ID',
    control_mode VARCHAR(20) DEFAULT 'host_only' NOT NULL COMMENT '控制模式: host_only=仅房主, all_members=全员',
    mode VARCHAR(20) DEFAULT 'link' NOT NULL COMMENT '播放模式: link=外链, upload=上传, local=本地',
    video_source TEXT COMMENT '视频源: URL链接或文件路径',
    video_hash VARCHAR(64) COMMENT '视频文件哈希值(SHA256,用于模式二校验)',
    current_time INT DEFAULT 0 COMMENT '当前播放时间(秒)',
    is_playing BOOLEAN DEFAULT FALSE COMMENT '播放状态',
    is_active BOOLEAN DEFAULT TRUE COMMENT '房间是否活跃',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (host_user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_room_code (room_code),
    INDEX idx_host_user (host_user_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='同步观影房间表';

-- 创建房间成员表
CREATE TABLE IF NOT EXISTS sync_room_members (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '成员记录ID',
    room_id INT NOT NULL COMMENT '房间ID',
    user_id INT NOT NULL COMMENT '用户ID',
    nickname VARCHAR(50) COMMENT '房间内昵称',
    is_verified BOOLEAN DEFAULT TRUE COMMENT '是否通过哈希校验(用于模式二)',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    FOREIGN KEY (room_id) REFERENCES sync_rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_room_member (room_id, user_id),
    INDEX idx_room_member (room_id, user_id),
    INDEX idx_user_rooms (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房间成员表';

-- 创建房间聊天消息表
CREATE TABLE IF NOT EXISTS sync_room_messages (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '消息ID',
    room_id INT NOT NULL COMMENT '房间ID',
    user_id INT NOT NULL COMMENT '发送者用户ID',
    message TEXT NOT NULL COMMENT '消息内容',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    FOREIGN KEY (room_id) REFERENCES sync_rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_room_messages (room_id, created_at),
    INDEX idx_user_messages (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='房间聊天消息表';

-- 4. 再次验证表创建结果
SELECT 
    TABLE_NAME,
    TABLE_ROWS,
    CREATE_TIME,
    '✅ 已创建' as STATUS
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'blue_local_db' 
  AND TABLE_NAME IN ('sync_rooms', 'sync_room_members', 'sync_room_messages')
ORDER BY TABLE_NAME;

-- 5. 显示表结构
SHOW CREATE TABLE sync_rooms;
SHOW CREATE TABLE sync_room_members;
SHOW CREATE TABLE sync_room_messages;
