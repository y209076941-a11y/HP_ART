import os
import glob
from pathlib import Path
import re


def rename_media_files():
    """重命名图片和视频文件为 SYPHU-CHINA-iGEM-编号 格式"""

    # 定义支持的媒体文件类型
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']

    # 定义目录
    base_dir = Path(__file__).parent
    art_dir = base_dir / "ART"
    hp_dir = base_dir / "HP"

    print("🔄 开始重命名媒体文件...")
    print(f"工作目录: {base_dir}")
    print(f"ART目录: {art_dir}")
    print(f"HP目录: {hp_dir}")

    # 检查目录是否存在
    if not art_dir.exists():
        print(f"❌ ART目录不存在: {art_dir}")
        return
    if not hp_dir.exists():
        print(f"❌ HP目录不存在: {hp_dir}")
        return

    # 重命名ART目录中的文件
    print("\n🎨 处理ART目录...")
    art_count = rename_files_in_directory(art_dir, image_extensions + video_extensions, "ART")

    # 重命名HP目录中的文件
    print("\n📊 处理HP目录...")
    hp_count = rename_files_in_directory(hp_dir, image_extensions + video_extensions, "HP")

    print(f"\n✅ 重命名完成!")
    print(f"ART目录: {art_count} 个文件已重命名")
    print(f"HP目录: {hp_count} 个文件已重命名")
    print(f"总计: {art_count + hp_count} 个文件")


def rename_files_in_directory(directory, extensions, category):
    """重命名指定目录中的文件"""
    count = 0

    # 获取目录中所有指定扩展名的文件
    files = []
    for ext in extensions:
        pattern = str(directory / f"*{ext}")
        files.extend(glob.glob(pattern, recursive=False))
        # 同时检查大写扩展名
        pattern_upper = str(directory / f"*{ext.upper()}")
        files.extend(glob.glob(pattern_upper, recursive=False))

    # 移除重复的文件（由于大小写扩展名可能重复）
    files = list(set(files))

    if not files:
        print(f"  📭 在 {category} 目录中没有找到媒体文件")
        return 0

    print(f"  📁 找到 {len(files)} 个媒体文件")

    # 按文件修改时间排序，确保顺序一致
    files.sort(key=lambda x: os.path.getmtime(x))

    # 重命名文件
    for i, file_path in enumerate(files, 1):
        try:
            old_path = Path(file_path)

            # 获取文件扩展名（小写）
            ext = old_path.suffix.lower()

            # 确定文件类型
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
                file_type = "IMAGE"
            elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
                file_type = "VIDEO"
            else:
                file_type = "FILE"

            # 生成新文件名
            new_name = f"SYPHU-CHINA-iGEM-{category}-{i:03d}{ext}"
            new_path = directory / new_name

            # 如果目标文件已存在，先删除（避免重命名冲突）
            if new_path.exists():
                new_path.unlink()

            # 重命名文件
            old_path.rename(new_path)

            print(f"  ✅ 重命名: {old_path.name} -> {new_name} [{file_type}]")
            count += 1

        except Exception as e:
            print(f"  ❌ 重命名失败 {old_path.name}: {e}")

    return count


def preview_renaming():
    """预览重命名操作（不实际执行）"""

    # 定义支持的媒体文件类型
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']

    # 定义目录
    base_dir = Path(__file__).parent
    art_dir = base_dir / "ART"
    hp_dir = base_dir / "HP"

    print("👀 预览重命名操作...")
    print(f"工作目录: {base_dir}")

    # 检查目录是否存在
    if not art_dir.exists():
        print(f"❌ ART目录不存在: {art_dir}")
        return
    if not hp_dir.exists():
        print(f"❌ HP目录不存在: {hp_dir}")
        return

    print("\n🎨 ART目录预览:")
    preview_files_in_directory(art_dir, image_extensions + video_extensions, "ART")

    print("\n📊 HP目录预览:")
    preview_files_in_directory(hp_dir, image_extensions + video_extensions, "HP")


def preview_files_in_directory(directory, extensions, category):
    """预览目录中的文件重命名"""

    # 获取目录中所有指定扩展名的文件
    files = []
    for ext in extensions:
        pattern = str(directory / f"*{ext}")
        files.extend(glob.glob(pattern, recursive=False))
        # 同时检查大写扩展名
        pattern_upper = str(directory / f"*{ext.upper()}")
        files.extend(glob.glob(pattern_upper, recursive=False))

    # 移除重复的文件
    files = list(set(files))

    if not files:
        print(f"  📭 没有找到媒体文件")
        return

    print(f"  📁 找到 {len(files)} 个媒体文件")

    # 按文件修改时间排序
    files.sort(key=lambda x: os.path.getmtime(x))

    # 预览重命名
    for i, file_path in enumerate(files, 1):
        old_path = Path(file_path)
        ext = old_path.suffix.lower()

        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
            file_type = "IMAGE"
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
            file_type = "VIDEO"
        else:
            file_type = "FILE"

        new_name = f"SYPHU-CHINA-iGEM-{category}-{i:03d}{ext}"
        print(f"  📄 {old_path.name} -> {new_name} [{file_type}]")


def main():
    """主函数"""
    print("=" * 60)
    print("🔄 SYPHU-CHINA-iGEM 媒体文件重命名工具")
    print("=" * 60)

    while True:
        print("\n请选择操作:")
        print("1. 预览重命名（不实际执行）")
        print("2. 执行重命名")
        print("3. 退出")

        choice = input("\n请输入选择 (1-3): ").strip()

        if choice == "1":
            preview_renaming()
        elif choice == "2":
            # 确认操作
            confirm = input("\n⚠️  确定要执行重命名操作吗？此操作不可撤销！(y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                rename_media_files()
            else:
                print("❌ 操作已取消")
        elif choice == "3":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main()