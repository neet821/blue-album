-- ================================================
-- 多人同步观影功能 - 数据库迁移脚本
-- 创建日期: 2025-10-19
-- 描述: 创建同步观影所需的3个表
-- 数据库: blue_local_db
-- ================================================

-- 使用正确的数据库
USE blue_local_db;

-- 1. 创建同步观影房间表
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

-- 2. 创建房间成员表
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

-- 3. 创建房间聊天消息表
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

-- ================================================
-- 验证表创建
-- ================================================
USE blue_local_db;

SELECT 
    'sync_rooms' as table_name, 
    COUNT(*) as row_count 
FROM sync_rooms
UNION ALL
SELECT 
    'sync_room_members' as table_name, 
    COUNT(*) as row_count 
FROM sync_room_members
UNION ALL
SELECT 
    'sync_room_messages' as table_name, 
    COUNT(*) as row_count 
FROM sync_room_messages;

-- ================================================
-- 示例数据 (可选,用于测试)
-- ================================================

-- 插入测试房间 (需要先有用户数据)
-- INSERT INTO sync_rooms (room_code, room_name, host_user_id, control_mode, mode, video_source)
-- VALUES 
--     ('ABC123', '周末观影室', 1, 'host_only', 'link', 'https://www.w3schools.com/html/mov_bbb.mp4'),
--     ('XYZ789', '朋友聚会', 1, 'all_members', 'link', 'https://www.w3schools.com/html/movie.mp4');

-- 查看房间列表
-- SELECT 
--     r.id,
--     r.room_code,
--     r.room_name,
--     u.username as host_name,
--     r.control_mode,
--     r.mode,
--     r.is_active,
--     COUNT(m.id) as member_count
-- FROM sync_rooms r
-- LEFT JOIN users u ON r.host_user_id = u.id
-- LEFT JOIN sync_room_members m ON r.id = m.room_id
-- GROUP BY r.id;

-- ================================================
-- 清理命令 (谨慎使用)
-- ================================================

-- DROP TABLE IF EXISTS sync_room_messages;
-- DROP TABLE IF EXISTS sync_room_members;
-- DROP TABLE IF EXISTS sync_rooms;
