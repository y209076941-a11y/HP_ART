# build_site.py - 集成到Human Practices的版本
import os
import glob
from pathlib import Path
import json
from datetime import datetime


def get_image_files(directory, extensions=('*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp')):
    """扫描目录中的图片文件"""
    image_files = []
    for ext in extensions:
        pattern = os.path.join(directory, '**', ext)
        image_files.extend(glob.glob(pattern, recursive=True))

    # 转换为相对路径并排序
    image_files = [os.path.relpath(f) for f in image_files]
    return sorted(image_files)


def generate_image_html(image_files, category):
    """为图片列表生成HTML代码"""
    if not image_files:
        return f'<div class="empty-state">No {category} images found yet.</div>'

    html_parts = []

    for img_path in image_files:
        # 获取文件名（不含扩展名）作为默认描述
        filename = os.path.splitext(os.path.basename(img_path))[0]
        # 将下划线替换为空格并首字母大写
        description = filename.replace('_', ' ').title()

        img_html = f'''
        <div class="gallery-card">
            <div class="card-image">
                <img src="{img_path}" alt="{description}" class="gallery-image" loading="lazy">
                <div class="image-overlay">
                    <button class="view-btn" onclick="enlargeImage(this)">
                        <span>👁️</span> View
                    </button>
                </div>
            </div>
            <div class="card-content">
                <h3 class="image-title">{description}</h3>
                <p class="image-date">Added recently</p>
            </div>
        </div>
        '''
        html_parts.append(img_html)

    return '\n'.join(html_parts)


def create_hp_integrated_html(hp_images_html, art_images_html, timestamp):
    """创建集成到Human Practices的HTML"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Gallery - Human Practices | iGEM Team</title>
    <link rel="stylesheet" href="gallery-style.css">
    <style>
        /* 集成页面的特定样式 */
        .hp-gallery-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}

        .gallery-header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 1.5rem;
            border-bottom: 2px solid var(--mint);
        }}

        .gallery-title {{
            color: var(--green);
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        .gallery-subtitle {{
            color: var(--accent-green);
            font-size: 1.2rem;
            font-style: italic;
        }}

        .section-title {{
            color: var(--green);
            border-left: 4px solid var(--green);
            padding-left: 1rem;
            margin: 3rem 0 1.5rem 0;
            font-size: 1.8rem;
        }}

        .last-updated {{
            text-align: center;
            color: var(--accent-green);
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--mint);
        }}
    </style>
</head>
<body>
    <div class="hp-gallery-container">
        <header class="gallery-header">
            <h1 class="gallery-title">Media Gallery</h1>
            <p class="gallery-subtitle">Documenting our Human Practices journey through visuals</p>
        </header>

        <section class="gallery-section">
            <h2 class="section-title">Human Practices Activities</h2>
            <p class="section-description">Capturing moments from our community engagement, stakeholder meetings, and outreach events.</p>

            <div class="gallery-grid" id="hp-gallery">
                {hp_images_html}
            </div>
        </section>

        <section class="gallery-section">
            <h2 class="section-title">Art & Design Works</h2>
            <p class="section-description">Creative visuals that communicate our project's story and scientific concepts.</p>

            <div class="gallery-grid" id="art-gallery">
                {art_images_html}
            </div>
        </section>

        <div class="last-updated">
            Gallery automatically updated: {timestamp}
        </div>
    </div>

    <!-- 图片放大模态框 -->
    <div id="imageModal" class="modal">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImage">
        <div id="modalCaption" class="modal-caption"></div>
    </div>

    <script>
        // 图片放大功能
        function enlargeImage(btn) {{
            const card = btn.closest('.gallery-card');
            const img = card.querySelector('.gallery-image');
            const title = card.querySelector('.image-title').textContent;

            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            const caption = document.getElementById('modalCaption');

            modal.style.display = "block";
            modalImg.src = img.src;
            caption.textContent = title;
        }}

        function closeModal() {{
            document.getElementById('imageModal').style.display = "none";
        }}

        // 点击模态框外部关闭
        window.onclick = function(event) {{
            const modal = document.getElementById('imageModal');
            if (event.target == modal) {{
                closeModal();
            }}
        }}

        // ESC键关闭
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Escape') {{
                closeModal();
            }}
        }});
    </script>
</body>
</html>'''


def create_embed_snippet(hp_images_html, art_images_html):
    """创建可直接嵌入的HTML片段"""
    return f'''
    <div class="integrated-gallery">
        <div class="gallery-section">
            <h3 style="color: #255A3B; border-bottom: 2px solid #81B095; padding-bottom: 0.5rem;">
                📸 Human Practices Gallery
            </h3>
            <div class="gallery-grid compact">
                {hp_images_html if hp_images_html else '<p class="no-images">No Human Practices images yet.</p>'}
            </div>
        </div>

        <div class="gallery-section">
            <h3 style="color: #255A3B; border-bottom: 2px solid #81B095; padding-bottom: 0.5rem;">
                🎨 Art & Design Gallery
            </h3>
            <div class="gallery-grid compact">
                {art_images_html if art_images_html else '<p class="no-images">No artwork images yet.</p>'}
            </div>
        </div>
    </div>
    '''


def main():
    """主函数：构建网站"""
    print("🚀 Building Human Practices Gallery...")

    # 扫描图片目录
    print("📁 Scanning for images...")
    art_images = get_image_files('ART')
    hp_images = get_image_files('HP')

    print(f"🎨 Found {len(art_images)} artwork images")
    print(f"👥 Found {len(hp_images)} HP images")

    # 生成图片HTML
    art_html = generate_image_html(art_images, 'artworks')
    hp_html = generate_image_html(hp_images, 'hp')

    # 创建时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 生成集成版本HTML
    integrated_html = create_hp_integrated_html(hp_html, art_html, timestamp)

    # 生成嵌入片段
    embed_html = create_embed_snippet(hp_html, art_html)

    # 写入文件
    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(integrated_html)

    with open('gallery_snippet.html', 'w', encoding='utf-8') as f:
        f.write(embed_html)

    # 生成数据文件
    gallery_data = {
        'last_updated': timestamp,
        'artworks': art_images,
        'human_practices': hp_images,
        'stats': {
            'total_hp': len(hp_images),
            'total_art': len(art_images),
            'total_all': len(hp_images) + len(art_images)
        }
    }

    with open('gallery_data.json', 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, indent=2)

    print("✅ Human Practices Gallery built successfully!")
    print(f"📊 Statistics: {len(hp_images)} HP + {len(art_images)} Art = {len(hp_images) + len(art_images)} total")
    print("📄 Generated files:")
    print("   - gallery.html (Full integrated page)")
    print("   - gallery_snippet.html (Embeddable snippet)")
    print("   - gallery_data.json (Image data)")


if __name__ == "__main__":
    main()