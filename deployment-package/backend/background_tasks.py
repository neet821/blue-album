"""
后台定时任务 - 自动清理空房间

每隔一段时间自动清理无人的房间
"""
import asyncio
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database import SessionLocal
from backend import sync_room_crud
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def cleanup_task(interval_minutes: int = 5, empty_timeout_minutes: int = 10):
    """定时清理空房间任务
    
    Args:
        interval_minutes: 检查间隔（分钟）
        empty_timeout_minutes: 空房间超时时间（分钟）
    """
    logger.info(f"空房间清理任务启动 - 检查间隔:{interval_minutes}分钟, 超时阈值:{empty_timeout_minutes}分钟")
    
    while True:
        try:
            db = SessionLocal()
            
            # 执行清理
            deleted_count = sync_room_crud.cleanup_empty_rooms(db, empty_timeout_minutes)
            
            if deleted_count > 0:
                logger.info(f"✅ 清理了 {deleted_count} 个空房间")
            else:
                logger.debug(f"⏭️  没有需要清理的空房间")
            
            db.close()
            
        except Exception as e:
            logger.error(f"❌ 清理任务出错: {str(e)}")
        
        # 等待下次执行
        await asyncio.sleep(interval_minutes * 60)

if __name__ == "__main__":
    # 可以通过命令行参数自定义间隔时间
    import argparse
    
    parser = argparse.ArgumentParser(description='同步观影空房间清理服务')
    parser.add_argument('--interval', type=int, default=5, help='检查间隔（分钟），默认5分钟')
    parser.add_argument('--timeout', type=int, default=10, help='空房间超时时间（分钟），默认10分钟')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 同步观影空房间清理服务")
    print("=" * 60)
    print(f"检查间隔: {args.interval} 分钟")
    print(f"超时阈值: {args.timeout} 分钟")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("按 Ctrl+C 停止服务")
    print()
    
    try:
        asyncio.run(cleanup_task(args.interval, args.timeout))
    except KeyboardInterrupt:
        print("\n\n服务已停止")
