# build_site.py - 增加视频支持版本
import os
import glob
from pathlib import Path
import json
from datetime import datetime


def get_media_files(directory, media_types):
    """扫描目录中的媒体文件（图片和视频）"""
    media_files = []
    for pattern in media_types:
        full_pattern = os.path.join(directory, '**', pattern)
        media_files.extend(glob.glob(full_pattern, recursive=True))

    # 转换为相对路径并排序
    media_files = [os.path.relpath(f) for f in media_files]
    return sorted(media_files)


def is_video_file(filename):
    """检查文件是否为视频格式"""
    video_extensions = ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv')
    return filename.lower().endswith(video_extensions)


def is_image_file(filename):
    """检查文件是否为图片格式"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
    return filename.lower().endswith(image_extensions)


def generate_media_html(media_files, category):
    """为媒体文件列表生成HTML代码"""
    if not media_files:
        return f'<div class="empty-state">No {category} media found yet.</div>'

    html_parts = []

    for media_path in media_files:
        # 获取文件名（不含扩展名）作为默认描述
        filename = os.path.splitext(os.path.basename(media_path))[0]
        # 将下划线替换为空格并首字母大写
        description = filename.replace('_', ' ').title()

        if is_video_file(media_path):
            # 视频卡片
            media_html = f'''
            <div class="gallery-card video-card">
                <div class="card-image">
                    <video class="media-preview" preload="metadata">
                        <source src="{media_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="image-overlay">
                        <button class="play-btn" onclick="playVideo(this)">
                            <span class="play-icon">▶</span>
                            <span class="play-text">Play Video</span>
                        </button>
                        <div class="video-duration">0:00</div>
                    </div>
                    <div class="video-badge">VIDEO</div>
                </div>
                <div class="card-content">
                    <h3 class="media-title">{description}</h3>
                    <p class="media-date">Video • Added recently</p>
                </div>
            </div>
            '''
        else:
            # 图片卡片
            media_html = f'''
            <div class="gallery-card">
                <div class="card-image">
                    <img src="{media_path}" alt="{description}" class="media-preview" loading="lazy">
                    <div class="image-overlay">
                        <button class="view-btn" onclick="enlargeImage(this)">
                            <span>👁️</span> View
                        </button>
                    </div>
                </div>
                <div class="card-content">
                    <h3 class="media-title">{description}</h3>
                    <p class="media-date">Photo • Added recently</p>
                </div>
            </div>
            '''

        html_parts.append(media_html)

    return '\n'.join(html_parts)


def create_hp_integrated_html(hp_media_html, art_media_html, timestamp):
    """创建集成到Human Practices的HTML - 支持视频版"""
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

        .media-stats {{
            display: flex;
            gap: 2rem;
            justify-content: center;
            margin: 1rem 0 2rem 0;
            flex-wrap: wrap;
        }}

        .stat-item {{
            background: var(--mint);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            color: var(--green);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .stat-item.video {{
            background: var(--light-blue);
        }}

        .last-updated {{
            text-align: center;
            color: var(--accent-green);
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--mint);
        }}

        /* 视频特定样式 */
        .video-card .card-image {{
            position: relative;
        }}

        .video-badge {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(71, 142, 204, 0.9);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: bold;
            backdrop-filter: blur(10px);
        }}

        .play-btn {{
            background: rgba(255, 255, 255, 0.95);
            color: var(--blue);
            border: 2px solid rgba(255, 255, 255, 0.8);
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}

        .play-btn:hover {{
            background: var(--white);
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(71, 142, 204, 0.3);
        }}

        .play-icon {{
            font-size: 1.2rem;
        }}

        .video-duration {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.7rem;
            backdrop-filter: blur(5px);
        }}

        /* 视频模态框样式 */
        .video-modal {{
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .video-modal.show {{
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 1;
        }}

        .video-modal-content {{
            max-width: 90vw;
            max-height: 90vh;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            transform: scale(0.9);
            transition: transform 0.3s ease;
            background: #000;
        }}

        .video-modal.show .video-modal-content {{
            transform: scale(1);
        }}

        .video-modal video {{
            width: 100%;
            height: auto;
            max-height: 90vh;
            border-radius: 12px;
        }}

        .video-close-btn {{
            position: fixed;
            top: 20px;
            right: 30px;
            color: #ffffff;
            font-size: 40px;
            font-weight: 300;
            cursor: pointer;
            z-index: 10000;
            background: rgba(0, 0, 0, 0.5);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}

        .video-close-btn:hover {{
            background: rgba(220, 145, 123, 0.8);
            transform: rotate(90deg);
            border-color: rgba(255, 255, 255, 0.6);
        }}

        .video-modal-caption {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            text-align: center;
            background: rgba(71, 142, 204, 0.9);
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1rem;
            max-width: 80%;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .video-controls {{
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 1rem;
            align-items: center;
        }}

        .control-btn {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .control-btn:hover {{
            background: rgba(71, 142, 204, 0.8);
            transform: scale(1.1);
        }}
    </style>
</head>
<body>
    <div class="hp-gallery-container">
        <header class="gallery-header">
            <h1 class="gallery-title">Media Gallery</h1>
            <p class="gallery-subtitle">Documenting our Human Practices journey through photos and videos</p>

            <div class="media-stats" id="mediaStats">
                <!-- 统计数据将通过JavaScript动态生成 -->
            </div>
        </header>

        <section class="gallery-section">
            <h2 class="section-title">Human Practices Activities</h2>
            <p class="section-description">Capturing moments from our community engagement, stakeholder meetings, and outreach events.</p>

            <div class="gallery-grid" id="hp-gallery">
                {hp_media_html}
            </div>
        </section>

        <section class="gallery-section">
            <h2 class="section-title">Art & Design Works</h2>
            <p class="section-description">Creative visuals that communicate our project's story and scientific concepts.</p>

            <div class="gallery-grid" id="art-gallery">
                {art_media_html}
            </div>
        </section>

        <div class="last-updated">
            Gallery automatically updated: {timestamp}
        </div>
    </div>

    <!-- 图片模态框 -->
    <div id="imageModal" class="modal">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <button class="nav-btn prev-btn" onclick="navigateMedia(-1)">❮</button>
        <button class="nav-btn next-btn" onclick="navigateMedia(1)">❯</button>
        <div class="loading" id="modalLoading">Loading...</div>
        <img class="modal-content" id="modalImage" onload="mediaLoaded()">
        <div id="modalCaption" class="modal-caption"></div>
    </div>

    <!-- 视频模态框 -->
    <div id="videoModal" class="video-modal">
        <span class="video-close-btn" onclick="closeVideoModal()">&times;</span>
        <div class="video-modal-content">
            <video id="modalVideo" controls>
                Your browser does not support the video tag.
            </video>
        </div>
        <div id="videoModalCaption" class="video-modal-caption"></div>
        <div class="video-controls">
            <button class="control-btn" onclick="togglePlay()" id="playPauseBtn">⏸️</button>
            <button class="control-btn" onclick="toggleMute()" id="muteBtn">🔊</button>
            <button class="control-btn" onclick="toggleFullscreen()">⛶</button>
        </div>
    </div>

    <script>
        // 全局变量
        let currentMediaIndex = 0;
        let allMedia = [];
        let currentGallery = '';
        let isPlaying = false;

        // 初始化媒体数据
        function initMediaData() {{
            const hpMedia = Array.from(document.querySelectorAll('#hp-gallery .gallery-card'));
            const artMedia = Array.from(document.querySelectorAll('#art-gallery .gallery-card'));

            allMedia = [
                ...hpMedia.map((card, index) => ({{
                    element: card,
                    type: card.classList.contains('video-card') ? 'video' : 'image',
                    src: card.querySelector('.media-preview').src || card.querySelector('video source').src,
                    title: card.querySelector('.media-title').textContent,
                    gallery: 'hp',
                    index: index
                }})),
                ...artMedia.map((card, index) => ({{
                    element: card,
                    type: card.classList.contains('video-card') ? 'video' : 'image',
                    src: card.querySelector('.media-preview').src || card.querySelector('video source').src,
                    title: card.querySelector('.media-title').textContent,
                    gallery: 'art', 
                    index: index + hpMedia.length
                }}))
            ];

            // 更新统计数据
            updateMediaStats();
        }}

        // 更新媒体统计
        function updateMediaStats() {{
            const hpMedia = allMedia.filter(m => m.gallery === 'hp');
            const artMedia = allMedia.filter(m => m.gallery === 'art');

            const hpPhotos = hpMedia.filter(m => m.type === 'image').length;
            const hpVideos = hpMedia.filter(m => m.type === 'video').length;
            const artPhotos = artMedia.filter(m => m.type === 'image').length;

            const statsHTML = `
                <div class="stat-item">
                    <span>📸</span> {hpPhotos + artPhotos} Photos
                </div>
                <div class="stat-item video">
                    <span>🎥</span> {hpVideos} Videos
                </div>
                <div class="stat-item">
                    <span>📊</span> {allMedia.length} Total Media
                </div>
            `;

            document.getElementById('mediaStats').innerHTML = statsHTML;
        }}

        // 打开图片模态框
        function enlargeImage(btn) {{
            const card = btn.closest('.gallery-card');
            openMediaModal(card, 'image');
        }}

        // 播放视频
        function playVideo(btn) {{
            const card = btn.closest('.gallery-card');
            openMediaModal(card, 'video');
        }}

        // 打开媒体模态框
        function openMediaModal(card, mediaType) {{
            // 确定当前媒体在哪个图库
            currentGallery = card.closest('#hp-gallery') ? 'hp' : 'art';

            // 找到当前媒体的索引
            const cards = Array.from(document.querySelectorAll(`#${{currentGallery}}-gallery .gallery-card`));
            currentMediaIndex = allMedia.findIndex(m => m.element === card);

            if (mediaType === 'image') {{
                const modal = document.getElementById('imageModal');
                const modalImg = document.getElementById('modalImage');
                const caption = document.getElementById('modalCaption');
                const loading = document.getElementById('modalLoading');

                loading.style.display = 'block';
                modalImg.style.display = 'none';

                modal.classList.add('show');
                modalImg.src = allMedia[currentMediaIndex].src;
                caption.textContent = allMedia[currentMediaIndex].title;
            }} else if (mediaType === 'video') {{
                const modal = document.getElementById('videoModal');
                const modalVideo = document.getElementById('modalVideo');
                const caption = document.getElementById('videoModalCaption');

                modal.classList.add('show');
                modalVideo.src = allMedia[currentMediaIndex].src;
                modalVideo.load();
                caption.textContent = allMedia[currentMediaIndex].title;

                // 开始播放
                modalVideo.play().then(() => {{
                    isPlaying = true;
                    updatePlayPauseButton();
                }}).catch(e => {{
                    console.log('Autoplay prevented:', e);
                }});
            }}
        }}

        // 媒体加载完成
        function mediaLoaded() {{
            const loading = document.getElementById('modalLoading');
            const modalImg = document.getElementById('modalImage');

            loading.style.display = 'none';
            modalImg.style.display = 'block';
        }}

        // 关闭图片模态框
        function closeModal() {{
            const modal = document.getElementById('imageModal');
            modal.classList.remove('show');

            setTimeout(() => {{
                modal.style.display = 'none';
            }}, 300);
        }}

        // 关闭视频模态框
        function closeVideoModal() {{
            const modal = document.getElementById('videoModal');
            const video = document.getElementById('modalVideo');

            video.pause();
            isPlaying = false;
            modal.classList.remove('show');

            setTimeout(() => {{
                modal.style.display = 'none';
                video.src = ''; // 清除视频源
            }}, 300);
        }}

        // 导航媒体
        function navigateMedia(direction) {{
            if (allMedia.length === 0) return;

            currentMediaIndex += direction;

            // 循环导航
            if (currentMediaIndex >= allMedia.length) currentMediaIndex = 0;
            if (currentMediaIndex < 0) currentMediaIndex = allMedia.length - 1;

            const mediaData = allMedia[currentMediaIndex];

            if (mediaData.type === 'image') {{
                closeVideoModal();
                const modalImg = document.getElementById('modalImage');
                const caption = document.getElementById('modalCaption');
                const loading = document.getElementById('modalLoading');

                loading.style.display = 'block';
                modalImg.style.display = 'none';

                modalImg.src = mediaData.src;
                caption.textContent = mediaData.title;
            }} else {{
                closeModal();
                const modalVideo = document.getElementById('modalVideo');
                const caption = document.getElementById('videoModalCaption');

                modalVideo.src = mediaData.src;
                modalVideo.load();
                caption.textContent = mediaData.title;

                modalVideo.play().then(() => {{
                    isPlaying = true;
                    updatePlayPauseButton();
                }});
            }}

            currentGallery = mediaData.gallery;
        }}

        // 视频控制函数
        function togglePlay() {{
            const video = document.getElementById('modalVideo');
            if (isPlaying) {{
                video.pause();
                isPlaying = false;
            }} else {{
                video.play();
                isPlaying = true;
            }}
            updatePlayPauseButton();
        }}

        function toggleMute() {{
            const video = document.getElementById('modalVideo');
            const muteBtn = document.getElementById('muteBtn');
            video.muted = !video.muted;
            muteBtn.textContent = video.muted ? '🔇' : '🔊';
        }}

        function toggleFullscreen() {{
            const video = document.getElementById('modalVideo');
            if (!document.fullscreenElement) {{
                video.requestFullscreen().catch(err => {{
                    console.log(`Error attempting to enable fullscreen: ${{err.message}}`);
                }});
            }} else {{
                document.exitFullscreen();
            }}
        }}

        function updatePlayPauseButton() {{
            const playPauseBtn = document.getElementById('playPauseBtn');
            playPauseBtn.textContent = isPlaying ? '⏸️' : '▶️';
        }}

        // 事件监听
        document.getElementById('modalVideo').addEventListener('play', function() {{
            isPlaying = true;
            updatePlayPauseButton();
        }});

        document.getElementById('modalVideo').addEventListener('pause', function() {{
            isPlaying = false;
            updatePlayPauseButton();
        }});

        // 键盘导航
        document.addEventListener('keydown', function(event) {{
            const imageModal = document.getElementById('imageModal');
            const videoModal = document.getElementById('videoModal');

            if (imageModal.classList.contains('show') || videoModal.classList.contains('show')) {{
                if (event.key === 'Escape') {{
                    closeModal();
                    closeVideoModal();
                }} else if (event.key === 'ArrowRight') {{
                    navigateMedia(1);
                }} else if (event.key === 'ArrowLeft') {{
                    navigateMedia(-1);
                }} else if (event.key === ' ' && videoModal.classList.contains('show')) {{
                    event.preventDefault();
                    togglePlay();
                }}
            }}
        }});

        // 点击模态框背景关闭
        window.onclick = function(event) {{
            const imageModal = document.getElementById('imageModal');
            const videoModal = document.getElementById('videoModal');

            if (event.target === imageModal) {{
                closeModal();
            }}
            if (event.target === videoModal) {{
                closeVideoModal();
            }}
        }}

        // 初始化视频时长（需要页面加载完成后执行）
        function initVideoDurations() {{
            document.querySelectorAll('video.media-preview').forEach(video => {{
                video.addEventListener('loadedmetadata', function() {{
                    const duration = Math.floor(video.duration);
                    const minutes = Math.floor(duration / 60);
                    const seconds = duration % 60;
                    const durationElement = video.parentElement.querySelector('.video-duration');
                    if (durationElement) {{
                        durationElement.textContent = `${{minutes}}:${{seconds.toString().padStart(2, '0')}}`;
                    }}
                }});
            }});
        }}

        // 初始化
        document.addEventListener('DOMContentLoaded', function() {{
            initMediaData();
            initVideoDurations();
        }});
    </script>
</body>
</html>'''


def main():
    """主函数：构建网站"""
    print("🚀 Building Human Practices Gallery with Video Support...")

    # 定义媒体类型
    image_types = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
    video_types = ['*.mp4', '*.avi', '*.mov', '*.wmv', '*.flv', '*.webm', '*.mkv']
    all_media_types = image_types + video_types

    # 扫描媒体目录
    print("📁 Scanning for media files...")
    art_media = get_media_files('ART', all_media_types)
    hp_media = get_media_files('HP', all_media_types)

    # 统计信息
    art_images = len([m for m in art_media if is_image_file(m)])
    hp_images = len([m for m in hp_media if is_image_file(m)])
    hp_videos = len([m for m in hp_media if is_video_file(m)])

    print(f"🎨 Found {art_images} artwork images")
    print(f"📸 Found {hp_images} HP images")
    print(f"🎥 Found {hp_videos} HP videos")
    print(f"📊 Total: {len(art_media) + len(hp_media)} media files")

    # 生成媒体HTML
    art_html = generate_media_html(art_media, 'artworks')
    hp_html = generate_media_html(hp_media, 'hp')

    # 创建时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 生成集成版本HTML
    integrated_html = create_hp_integrated_html(hp_html, art_html, timestamp)

    # 写入文件
    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(integrated_html)

    print("✅ Human Practices Gallery with video support built successfully!")
    print("📄 Generated: gallery.html")


if __name__ == "__main__":
    main()