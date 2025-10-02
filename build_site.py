# build_site.py - 增强科学元素和Nature学术风格
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
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff')
    return filename.lower().endswith(image_extensions)


def generate_media_html(media_files, category):
    """为媒体文件列表生成HTML代码 - 增强科学风格"""
    if not media_files:
        return f'''
        <div class="empty-state">
            <div class="empty-icon">🔬</div>
            <h3>No {category} Data Available</h3>
            <p>Add experimental documentation to the {category.upper()}/ folder to see them displayed here.</p>
        </div>
        '''

    html_parts = []

    for media_path in media_files:
        # 获取文件名（不含扩展名）作为默认描述
        filename = os.path.splitext(os.path.basename(media_path))[0]
        # 将下划线替换为空格并首字母大写
        description = filename.replace('_', ' ').title()

        # 获取文件创建时间
        file_time = os.path.getctime(media_path)
        from datetime import datetime
        date_str = datetime.fromtimestamp(file_time).strftime("%b %d, %Y")

        if is_video_file(media_path):
            # 视频卡片 - 增强科学风格
            media_html = f'''
            <div class="media-card video-card">
                <div class="media-thumbnail">
                    <video class="media-preview" preload="metadata" aria-label="Experimental video: {description}">
                        <source src="{media_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="media-overlay">
                        <button class="media-action-btn play-btn" onclick="playVideo(this)" aria-label="Play experimental video: {description}">
                            <span class="action-icon">🎬</span>
                            <span class="action-text">Analyze Video</span>
                        </button>
                        <div class="media-badge video-badge">
                            <i class="fas fa-microscope"></i> EXPERIMENT
                        </div>
                        <div class="media-duration">0:00</div>
                    </div>
                </div>
                <div class="media-info">
                    <h3 class="media-title">{description}</h3>
                    <div class="media-meta">
                        <span class="media-type"><i class="fas fa-video"></i> Experimental Recording</span>
                        <span class="media-date">• {date_str}</span>
                    </div>
                    <div class="media-description">
                        <p><i class="fas fa-flask"></i> Documentation of experimental procedure with detailed protocol analysis.</p>
                    </div>
                </div>
            </div>
            '''
        else:
            # 图片卡片 - 增强科学风格
            media_html = f'''
            <div class="media-card">
                <div class="media-thumbnail">
                    <img src="{media_path}" alt="{description}" class="media-preview" loading="lazy">
                    <div class="media-overlay">
                        <button class="media-action-btn view-btn" onclick="enlargeImage(this)" aria-label="Analyze image: {description}">
                            <span class="action-icon">🔍</span>
                            <span class="action-text">Analyze Data</span>
                        </button>
                    </div>
                </div>
                <div class="media-info">
                    <h3 class="media-title">{description}</h3>
                    <div class="media-meta">
                        <span class="media-type"><i class="fas fa-image"></i> Research Documentation</span>
                        <span class="media-date">• {date_str}</span>
                    </div>
                    <div class="media-description">
                        <p><i class="fas fa-dna"></i> Visual documentation of research activities and experimental results analysis.</p>
                    </div>
                </div>
            </div>
            '''

        html_parts.append(media_html)

    return '\n'.join(html_parts)


def create_hp_integrated_html(hp_media_html, art_media_html, timestamp):
    """创建集成到Human Practices的HTML - 增强科学元素和动态效果"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Research Media Archive - Scientific Documentation | iGEM Team</title>
    <meta name="description" content="Advanced scientific archive of research documentation, experimental procedures, and scientific analysis.">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* ====== ENHANCED NATURE JOURNAL STYLE ====== */
        :root {{
            /* Enhanced Scientific Color Palette */
            --nature-dark: #0d1b2a;
            --nature-primary: #1b263b;
            --nature-secondary: #415a77;
            --nature-accent: #778da9;
            --nature-light: #e0e1dd;

            /* Scientific Element Colors */
            --dna-blue: #3498db;
            --protein-purple: #9b59b6;
            --enzyme-green: #27ae60;
            --substrate-orange: #f39c12;
            --reaction-red: #e74c3c;
            --membrane-gold: #f1c40f;

            /* Enhanced Background Colors */
            --bg-white: #ffffff;
            --bg-light: #f8fafc;
            --bg-lighter: #f1f5f9;
            --border-color: #e2e8f0;
            --border-light: #f1f5f9;

            /* Enhanced Typography */
            --font-primary: 'Georgia', 'Times New Roman', serif;
            --font-accent: 'Arial', 'Helvetica Neue', Helvetica, sans-serif;
            --font-scientific: 'Courier New', monospace;

            /* Enhanced Spacing */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-xxl: 4rem;
            --space-xxxl: 6rem;

            /* 新增：圆角变量 */
            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            --radius-xxl: 24px;

            /* Enhanced Effects */
            --shadow-sm: 0 2px 8px rgba(13, 27, 42, 0.08);
            --shadow-md: 0 4px 16px rgba(13, 27, 42, 0.12);
            --shadow-lg: 0 8px 32px rgba(13, 27, 42, 0.16);
            --glow-blue: 0 0 20px rgba(52, 152, 219, 0.4);
            --glow-green: 0 0 20px rgba(39, 174, 96, 0.4);
            --glow-purple: 0 0 20px rgba(155, 89, 182, 0.4);
        }}

        /* ====== BASE ENHANCEMENTS ====== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
            background: linear-gradient(135deg, var(--nature-light) 0%, var(--bg-white) 50%, var(--bg-light) 100%);
        }}

        body {{
            font-family: var(--font-primary);
            font-size: 18px;
            line-height: 1.7;
            color: var(--nature-primary);
            background: transparent;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            position: relative;
            overflow-x: hidden;
            min-height: 100vh;
        }}

        /* ====== ENHANCED SCIENTIFIC BACKGROUND ====== */
        .scientific-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 15% 20%, rgba(52, 152, 219, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 30%, rgba(39, 174, 96, 0.06) 0%, transparent 45%),
                radial-gradient(circle at 25% 80%, rgba(155, 89, 182, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 75% 70%, rgba(241, 196, 15, 0.04) 0%, transparent 35%),
                linear-gradient(135deg, rgba(224, 225, 221, 0.1) 0%, transparent 50%);
            z-index: -3;
            pointer-events: none;
        }}

        /* ====== ENHANCED SCIENTIFIC DECORATIONS ====== */
        .science-element {{
            position: fixed;
            z-index: -1;
            opacity: 0.25;
            pointer-events: none;
            filter: blur(1px);
            animation-timing-function: ease-in-out;
        }}

        /* Enhanced DNA Helix */
        .dna-helix {{
            top: 10%;
            left: 5%;
            width: 120px;
            height: 300px;
            animation: float-dna 20s ease-in-out infinite;
        }}

        .dna-strand {{
            position: absolute;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, 
                transparent, 
                var(--dna-blue), 
                var(--protein-purple), 
                var(--enzyme-green),
                transparent);
            left: 50%;
            transform: translateX(-50%);
            opacity: 0.8;
            box-shadow: var(--glow-blue);
        }}

        .dna-base {{
            position: absolute;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 3px solid rgba(255,255,255,0.6);
            animation: pulse-base 3s ease-in-out infinite;
            box-shadow: 0 0 15px currentColor;
        }}

        .dna-base.blue {{ background: var(--dna-blue); color: var(--dna-blue); }}
        .dna-base.green {{ background: var(--enzyme-green); color: var(--enzyme-green); }}
        .dna-base.purple {{ background: var(--protein-purple); color: var(--protein-purple); }}

        /* Enhanced Cell Structure */
        .cell-structure {{
            bottom: 10%;
            right: 8%;
            width: 200px;
            height: 200px;
            animation: rotate-cell 40s linear infinite;
        }}

        .cell-membrane {{
            position: absolute;
            width: 100%;
            height: 100%;
            border: 4px solid var(--membrane-gold);
            border-radius: 50%;
            opacity: 0.8;
            box-shadow: var(--glow-green);
            animation: pulse-membrane 8s ease-in-out infinite;
        }}

        .nucleus {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 70px;
            height: 70px;
            background: radial-gradient(circle, var(--protein-purple), transparent);
            border-radius: 50%;
            animation: pulse-nucleus 6s ease-in-out infinite;
            box-shadow: var(--glow-purple);
        }}

        .organelle {{
            position: absolute;
            border-radius: 50%;
            opacity: 0.7;
            animation: float-organelle 15s ease-in-out infinite;
            box-shadow: 0 0 12px currentColor;
        }}

        .mitochondria {{ 
            width: 35px; 
            height: 60px; 
            background: var(--enzyme-green); 
            color: var(--enzyme-green);
            animation-delay: 2s;
        }}
        .ribosome {{ 
            width: 20px; 
            height: 20px; 
            background: var(--reaction-red); 
            color: var(--reaction-red);
            animation-delay: 4s;
        }}
        .golgi {{ 
            width: 45px; 
            height: 30px; 
            background: var(--substrate-orange); 
            color: var(--substrate-orange);
            animation-delay: 6s;
        }}

        /* Molecular Structures */
        .molecule-cluster {{
            top: 20%;
            right: 10%;
            width: 150px;
            height: 150px;
            animation: float-molecule 25s ease-in-out infinite;
        }}

        .molecule {{
            position: absolute;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 10px currentColor;
            animation: bond-vibration 4s ease-in-out infinite;
        }}

        .atom-large {{ 
            width: 25px; 
            height: 25px; 
            background: var(--dna-blue); 
            color: var(--dna-blue);
        }}
        .atom-medium {{ 
            width: 18px; 
            height: 18px; 
            background: var(--enzyme-green); 
            color: var(--enzyme-green);
        }}
        .atom-small {{ 
            width: 12px; 
            height: 12px; 
            background: var(--reaction-red); 
            color: var(--reaction-red);
        }}

        .chemical-bond {{
            position: absolute;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--nature-accent), transparent);
            transform-origin: left center;
            animation: bond-rotation 8s linear infinite;
        }}

        /* Protein Folding Animation */
        .protein-folding {{
            bottom: 25%;
            left: 8%;
            width: 120px;
            height: 120px;
            animation: fold-protein 30s ease-in-out infinite;
        }}

        .protein-chain {{
            position: absolute;
            width: 80%;
            height: 80%;
            border: 2px solid var(--protein-purple);
            border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
            animation: morph-protein 15s ease-in-out infinite;
            opacity: 0.8;
            box-shadow: var(--glow-purple);
        }}

        .amino-acid {{
            position: absolute;
            width: 10px;
            height: 10px;
            background: var(--protein-purple);
            border-radius: 50%;
            animation: blink-amino 2s ease-in-out infinite;
            box-shadow: 0 0 10px var(--protein-purple);
        }}

        /* Enhanced Animation Keyframes */
        @keyframes float-dna {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg) scale(1); }}
            25% {{ transform: translateY(-20px) rotate(90deg) scale(1.1); }}
            50% {{ transform: translateY(10px) rotate(180deg) scale(1); }}
            75% {{ transform: translateY(-15px) rotate(270deg) scale(1.05); }}
        }}

        @keyframes pulse-base {{
            0%, 100% {{ opacity: 0.6; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.4); }}
        }}

        @keyframes pulse-membrane {{
            0%, 100% {{ opacity: 0.6; transform: scale(1); }}
            50% {{ opacity: 0.9; transform: scale(1.05); }}
        }}

        @keyframes float-organelle {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            25% {{ transform: translate(15px, -10px) rotate(90deg); }}
            50% {{ transform: translate(5px, 15px) rotate(180deg); }}
            75% {{ transform: translate(-10px, 5px) rotate(270deg); }}
        }}

        @keyframes float-molecule {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            33% {{ transform: translate(25px, -15px) rotate(120deg); }}
            66% {{ transform: translate(-15px, 20px) rotate(240deg); }}
        }}

        @keyframes bond-vibration {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.2); }}
        }}

        @keyframes bond-rotation {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        @keyframes fold-protein {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            25% {{ transform: translate(10px, -15px) scale(1.1); }}
            50% {{ transform: translate(-5px, 10px) scale(0.9); }}
            75% {{ transform: translate(15px, 5px) scale(1.05); }}
        }}

        @keyframes morph-protein {{
            0% {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; transform: rotate(0deg); }}
            33% {{ border-radius: 70% 30% 30% 70% / 70% 70% 30% 30%; transform: rotate(120deg); }}
            66% {{ border-radius: 50% 50% 50% 50% / 50% 50% 50% 50%; transform: rotate(240deg); }}
            100% {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; transform: rotate(360deg); }}
        }}

        @keyframes blink-amino {{
            0%, 100% {{ opacity: 0.4; }}
            50% {{ opacity: 1; }}
        }}

        /* ====== ENHANCED TYPOGRAPHY ====== */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-primary);
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: var(--space-lg);
            color: var(--nature-dark);
            letter-spacing: -0.02em;
        }}

        h1 {{
            font-size: 3.5rem;
            background: linear-gradient(135deg, var(--nature-dark), var(--protein-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 2px 2px 4px rgba(13, 27, 42, 0.1);
        }}

        h2 {{
            font-size: 2.5rem;
            border-bottom: 3px solid var(--enzyme-green);
            padding-bottom: var(--space-md);
            margin-bottom: var(--space-xxl);
            position: relative;
        }}

        h2::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 100px;
            height: 3px;
            background: var(--protein-purple);
        }}

        h3 {{
            font-size: 1.5rem;
            font-weight: 600;
        }}

        .lead {{
            font-size: 1.25rem;
            font-weight: 400;
            color: var(--nature-secondary);
            line-height: 1.8;
            font-style: italic;
        }}

        .scientific-term {{
            font-family: var(--font-scientific);
            background: var(--bg-lighter);
            padding: 2px 6px;
            border-radius: var(--radius-sm);
            border-left: 3px solid var(--enzyme-green);
            font-weight: 600;
        }}

        /* ====== ENHANCED LAYOUT ====== */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 var(--space-xl);
            position: relative;
            z-index: 1;
        }}

        .page-header {{
            background: linear-gradient(135deg, var(--bg-light) 0%, var(--bg-lighter) 100%);
            border-bottom: 3px solid var(--border-light);
            padding: var(--space-xxxl) 0;
            margin-bottom: var(--space-xxxl);
            position: relative;
            z-index: 1;
            box-shadow: var(--shadow-md);
        }}

        .page-title {{
            text-align: center;
            margin-bottom: var(--space-lg);
            position: relative;
        }}

        .page-title::before {{
            content: '🔬';
            position: absolute;
            left: -60px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 2rem;
            opacity: 0.3;
        }}

        .page-subtitle {{
            text-align: center;
            font-size: 1.5rem;
            color: var(--nature-secondary);
            max-width: 800px;
            margin: 0 auto;
            font-style: italic;
            line-height: 1.6;
        }}

        .section {{
            margin-bottom: var(--space-xxxl);
            padding: var(--space-xxl) 0;
            position: relative;
            z-index: 1;
        }}

        .section-header {{
            margin-bottom: var(--space-xxl);
            text-align: center;
            position: relative;
        }}

        .section-title {{
            display: inline-block;
            position: relative;
            padding-bottom: var(--space-md);
        }}

        .section-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 25%;
            width: 50%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--enzyme-green), transparent);
        }}

        .section-description {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
            color: var(--nature-secondary);
            font-size: 1.1rem;
        }}

        /* ====== ENHANCED MEDIA GRID ====== */
        .media-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: var(--space-xxl);
            margin: var(--space-xxl) 0;
        }}

        .media-card {{
            background: var(--bg-white);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: var(--shadow-sm);
            position: relative;
        }}

        .media-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--dna-blue), var(--enzyme-green), var(--protein-purple));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .media-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-lg);
            border-color: var(--enzyme-green);
        }}

        .media-card:hover::before {{
            opacity: 1;
        }}

        .media-thumbnail {{
            position: relative;
            height: 280px;
            overflow: hidden;
            background: linear-gradient(135deg, var(--bg-lighter), var(--bg-light));
        }}

        .media-preview {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: all 0.4s ease;
        }}

        .media-card:hover .media-preview {{
            transform: scale(1.08);
        }}

        .media-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(13, 27, 42, 0.9), rgba(27, 38, 59, 0.8));
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: all 0.3s ease;
            backdrop-filter: blur(4px);
        }}

        .media-card:hover .media-overlay {{
            opacity: 1;
        }}

        .media-action-btn {{
            background: linear-gradient(135deg, var(--enzyme-green), var(--dna-blue));
            color: var(--bg-white);
            border: none;
            padding: var(--space-md) var(--space-xl);
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            transition: all 0.3s ease;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: var(--shadow-md);
        }}

        .media-action-btn:hover {{
            transform: translateY(-2px) scale(1.05);
            box-shadow: var(--shadow-lg);
        }}

        .action-icon {{
            font-size: 1.2rem;
        }}

        .media-badge {{
            position: absolute;
            top: var(--space-lg);
            right: var(--space-lg);
            padding: var(--space-sm) var(--space-md);
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            background: linear-gradient(135deg, var(--dna-blue), var(--protein-purple));
            color: var(--bg-white);
            box-shadow: var(--shadow-sm);
        }}

        .media-duration {{
            position: absolute;
            bottom: var(--space-lg);
            right: var(--space-lg);
            background: rgba(13, 27, 42, 0.9);
            color: var(--bg-white);
            padding: var(--space-xs) var(--space-sm);
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }}

        .media-info {{
            padding: var(--space-xl);
            background: var(--bg-white);
        }}

        .media-title {{
            font-size: 1.3rem;
            margin-bottom: var(--space-md);
            color: var(--nature-dark);
            line-height: 1.4;
            font-weight: 700;
        }}

        .media-meta {{
            display: flex;
            align-items: center;
            gap: var(--space-md);
            margin-bottom: var(--space-lg);
            font-size: 0.9rem;
            color: var(--nature-secondary);
        }}

        .media-type {{
            font-weight: 600;
            color: var(--enzyme-green);
            display: flex;
            align-items: center;
            gap: var(--space-xs);
        }}

        .media-date {{
            color: var(--nature-accent);
        }}

        .media-description {{
            font-size: 0.95rem;
            color: var(--nature-secondary);
            line-height: 1.6;
        }}

        .media-description i {{
            color: var(--enzyme-green);
            margin-right: var(--space-xs);
        }}

        /* ====== ENHANCED STATISTICS ====== */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: var(--space-xl);
            margin: var(--space-xxl) 0;
        }}

        .stat-card {{
            background: linear-gradient(135deg, var(--bg-white), var(--bg-lighter));
            border: 2px solid var(--border-light);
            border-radius: 12px;
            padding: var(--space-xl);
            text-align: center;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--dna-blue), var(--enzyme-green));
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }}

        .stat-icon {{
            font-size: 3rem;
            margin-bottom: var(--space-lg);
            color: var(--enzyme-green);
            opacity: 0.8;
        }}

        .stat-number {{
            font-size: 3.5rem;
            font-weight: 800;
            color: var(--nature-dark);
            margin-bottom: var(--space-sm);
            background: linear-gradient(135deg, var(--nature-dark), var(--protein-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-label {{
            font-size: 1rem;
            color: var(--nature-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}

        /* ====== ENHANCED EMPTY STATE ====== */
        .empty-state {{
            text-align: center;
            padding: var(--space-xxxl);
            background: linear-gradient(135deg, var(--bg-lighter), var(--bg-light));
            border: 3px dashed var(--border-color);
            border-radius: 16px;
            grid-column: 1 / -1;
        }}

        .empty-icon {{
            font-size: 4rem;
            margin-bottom: var(--space-xl);
            opacity: 0.5;
        }}

        /* ====== ENHANCED MODAL STYLES ====== */
        .modal {{
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(13, 27, 42, 0.98);
            backdrop-filter: blur(12px);
            opacity: 0;
            transition: opacity 0.4s ease;
        }}

        .modal.show {{
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 1;
        }}

        .modal-content {{
            max-width: 95vw;
            max-height: 95vh;
            object-fit: contain;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            transform: scale(0.8);
            transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 2px solid var(--enzyme-green);
        }}

        .modal.show .modal-content {{
            transform: scale(1);
        }}

        .modal-close {{
            position: fixed;
            top: var(--space-xxl);
            right: var(--space-xxl);
            background: linear-gradient(135deg, var(--reaction-red), var(--substrate-orange));
            color: var(--bg-white);
            border: 2px solid rgba(255, 255, 255, 0.3);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 1.8rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow-md);
        }}

        .modal-close:hover {{
            transform: rotate(90deg) scale(1.1);
            box-shadow: var(--shadow-lg);
        }}

        .modal-nav {{
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            background: linear-gradient(135deg, var(--dna-blue), var(--protein-purple));
            color: var(--bg-white);
            border: 2px solid rgba(255, 255, 255, 0.3);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow-md);
        }}

        .modal-nav:hover {{
            transform: translateY(-50%) scale(1.1);
            box-shadow: var(--shadow-lg);
        }}

        .modal-prev {{ left: var(--space-xxl); }}
        .modal-next {{ right: var(--space-xxl); }}

        .modal-caption {{
            position: fixed;
            bottom: var(--space-xxl);
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, var(--enzyme-green), var(--dna-blue));
            color: var(--bg-white);
            padding: var(--space-lg) var(--space-xl);
            border-radius: 12px;
            max-width: 80%;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            box-shadow: var(--shadow-md);
            font-size: 1.1rem;
            font-weight: 600;
        }}

        /* ====== ENHANCED VIDEO MODAL ====== */
        .video-modal {{
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(13, 27, 42, 0.98);
            backdrop-filter: blur(12px);
            opacity: 0;
            transition: opacity 0.4s ease;
        }}

        .video-modal.show {{
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 1;
        }}

        .video-modal-content {{
            max-width: 95vw;
            max-height: 95vh;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            transform: scale(0.8);
            transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            background: #000;
            border: 2px solid var(--dna-blue);
        }}

        .video-modal.show .video-modal-content {{
            transform: scale(1);
        }}

        .video-modal video {{
            width: 100%;
            height: auto;
            max-height: 95vh;
            border-radius: 14px;
        }}

        .video-close-btn {{
            position: fixed;
            top: var(--space-xxl);
            right: var(--space-xxl);
            background: linear-gradient(135deg, var(--reaction-red), var(--substrate-orange));
            color: var(--bg-white);
            border: 2px solid rgba(255, 255, 255, 0.3);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 1.8rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow-md);
            z-index: 10001;
        }}

        .video-close-btn:hover {{
            transform: rotate(90deg) scale(1.1);
            box-shadow: var(--shadow-lg);
        }}

        .video-modal-caption {{
            position: fixed;
            bottom: var(--space-xxl);
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, var(--dna-blue), var(--protein-purple));
            color: var(--bg-white);
            padding: var(--space-lg) var(--space-xl);
            border-radius: 12px;
            max-width: 80%;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            box-shadow: var(--shadow-md);
            font-size: 1.1rem;
            font-weight: 600;
        }}

        /* ====== ENHANCED FOOTER ====== */
        .page-footer {{
            background: linear-gradient(135deg, var(--nature-primary), var(--nature-dark));
            border-top: 3px solid var(--enzyme-green);
            padding: var(--space-xxl) 0;
            margin-top: var(--space-xxxl);
            text-align: center;
            color: var(--bg-white);
            position: relative;
        }}

        .page-footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--dna-blue), var(--enzyme-green), var(--protein-purple));
        }}

        .footer-text {{
            color: var(--nature-light);
            font-size: 1rem;
            opacity: 0.9;
        }}

        /* ====== RESPONSIVE DESIGN ENHANCEMENTS ====== */
        @media (max-width: 1200px) {{
            .container {{
                max-width: 100%;
                padding: 0 var(--space-lg);
            }}

            .media-grid {{
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: var(--space-xl);
            }}
        }}

        @media (max-width: 768px) {{
            .media-grid {{
                grid-template-columns: 1fr;
                gap: var(--space-lg);
            }}

            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            h1 {{
                font-size: 2.5rem;
            }}

            h2 {{
                font-size: 2rem;
            }}

            .container {{
                padding: 0 var(--space-md);
            }}

            .modal-close, .video-close-btn {{
                top: var(--space-lg);
                right: var(--space-lg);
                width: 50px;
                height: 50px;
            }}

            .modal-nav {{
                width: 50px;
                height: 50px;
            }}

            .modal-prev {{ left: var(--space-lg); }}
            .modal-next {{ right: var(--space-lg); }}

            /* Reduce scientific decorations on mobile */
            .science-element {{
                opacity: 0.15;
            }}
        }}

        @media (max-width: 480px) {{
            .page-header {{
                padding: var(--space-xxl) 0;
            }}

            .section {{
                padding: var(--space-xl) 0;
            }}

            .media-thumbnail {{
                height: 220px;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 2rem;
            }}

            h2 {{
                font-size: 1.75rem;
            }}

            .page-title::before {{
                display: none;
            }}
        }}

        /* ====== ACCESSIBILITY ENHANCEMENTS ====== */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}

            .science-element {{
                display: none;
            }}
        }}

        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}

        /* ====== LOADING ANIMATIONS ====== */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .media-card {{
            animation: fadeInUp 0.6s ease-out;
        }}

        .media-card:nth-child(odd) {{
            animation-delay: 0.1s;
        }}

        .media-card:nth-child(even) {{
            animation-delay: 0.2s;
        }}

        /* ====== INTERACTIVE ELEMENTS ====== */
        .floating-cta {{
            position: fixed;
            bottom: var(--space-xl);
            right: var(--space-xl);
            background: linear-gradient(135deg, var(--enzyme-green), var(--dna-blue));
            color: var(--bg-white);
            padding: var(--space-md) var(--space-lg);
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            animation: float-cta 3s ease-in-out infinite;
        }}

        .floating-cta:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: var(--shadow-lg), 0 0 20px var(--enzyme-green);
        }}

        @keyframes float-cta {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
    </style>
</head>
<body>
    <!-- Enhanced Scientific Background -->
    <div class="scientific-background"></div>

    <!-- Enhanced Scientific Elements -->
    <div class="science-element dna-helix">
        <div class="dna-strand"></div>
        <div class="dna-base blue" style="top: 15%"></div>
        <div class="dna-base green" style="top: 30%"></div>
        <div class="dna-base purple" style="top: 45%"></div>
        <div class="dna-base blue" style="top: 60%"></div>
        <div class="dna-base green" style="top: 75%"></div>
        <div class="dna-base purple" style="top: 90%"></div>
    </div>

    <div class="science-element cell-structure">
        <div class="cell-membrane"></div>
        <div class="nucleus"></div>
        <div class="organelle mitochondria" style="top: 20%; left: 20%;"></div>
        <div class="organelle ribosome" style="bottom: 30%; right: 25%;"></div>
        <div class="organelle golgi" style="top: 60%; left: 15%;"></div>
    </div>

    <div class="science-element molecule-cluster">
        <div class="molecule atom-large" style="top: 40%; left: 40%;"></div>
        <div class="molecule atom-medium" style="top: 20%; left: 60%;"></div>
        <div class="molecule atom-small" style="bottom: 30%; right: 40%;"></div>
        <div class="molecule atom-medium" style="bottom: 20%; left: 30%;"></div>
        <div class="chemical-bond" style="top: 45%; left: 42%; width: 50px; transform: rotate(45deg);"></div>
        <div class="chemical-bond" style="top: 25%; left: 55%; width: 40px; transform: rotate(120deg);"></div>
    </div>

    <div class="science-element protein-folding">
        <div class="protein-chain"></div>
        <div class="amino-acid" style="top: 30%; left: 25%;"></div>
        <div class="amino-acid" style="top: 60%; left: 45%;"></div>
        <div class="amino-acid" style="top: 40%; right: 30%;"></div>
        <div class="amino-acid" style="bottom: 25%; left: 35%;"></div>
    </div>

    <!-- Enhanced Page Header -->
    <header class="page-header">
        <div class="container">
            <h1 class="page-title">Advanced Research Media Archive</h1>
            <p class="page-subtitle">
                Comprehensive scientific documentation of experimental procedures, 
                research activities, and analytical results in synthetic biology
            </p>

            <!-- Enhanced Statistics -->
            <div class="stats-grid" id="mediaStats">
                <!-- Statistics will be populated by JavaScript -->
            </div>
        </div>
    </header>

    <main class="container">
        <!-- Enhanced Human Practices Section -->
        <section class="section" id="human-practices">
            <div class="section-header">
                <h2 class="section-title">
                    <i class="fas fa-users"></i> Human Practices & Outreach
                </h2>
                <p class="section-description lead">
                    Documentation of <span class="scientific-term">community engagement</span>, 
                    <span class="scientific-term">stakeholder interactions</span>, and 
                    <span class="scientific-term">public outreach activities</span> that 
                    inform and shape our research direction through ethical consideration 
                    and societal impact analysis.
                </p>
            </div>

            <div class="media-grid" id="hp-gallery">
                {hp_media_html}
            </div>
        </section>

        <!-- Enhanced Art & Design Section -->
        <section class="section" id="art-design">
            <div class="section-header">
                <h2 class="section-title">
                    <i class="fas fa-palette"></i> Scientific Communication & Visualization
                </h2>
                <p class="section-description lead">
                    Advanced <span class="scientific-term">scientific visualizations</span> and 
                    <span class="scientific-term">design elements</span> that communicate 
                    complex biological concepts and enhance public understanding of 
                    <span class="scientific-term">synthetic biology</span> through 
                    innovative graphical representation.
                </p>
            </div>

            <div class="media-grid" id="art-gallery">
                {art_media_html}
            </div>
        </section>
    </main>

    <!-- Enhanced Page Footer -->
    <footer class="page-footer">
        <div class="container">
            <p class="footer-text">
                Scientific Media Archive • Automatically Updated: {timestamp} • 
                iGEM Team Advanced Research Documentation System
            </p>
        </div>
    </footer>

    <!-- Enhanced Image Modal -->
    <div id="imageModal" class="modal" role="dialog" aria-labelledby="modalCaption" aria-hidden="true">
        <button class="modal-close" onclick="closeModal()" aria-label="Close scientific analysis">
            <i class="fas fa-times"></i>
        </button>
        <button class="modal-nav modal-prev" onclick="navigateMedia(-1)" aria-label="Previous analysis">
            <i class="fas fa-chevron-left"></i>
        </button>
        <button class="modal-nav modal-next" onclick="navigateMedia(1)" aria-label="Next analysis">
            <i class="fas fa-chevron-right"></i>
        </button>
        <img class="modal-content" id="modalImage" alt="" onload="mediaLoaded()">
        <div id="modalCaption" class="modal-caption"></div>
    </div>

    <!-- Enhanced Video Modal -->
    <div id="videoModal" class="video-modal" role="dialog" aria-labelledby="videoModalCaption" aria-hidden="true">
        <button class="video-close-btn" onclick="closeVideoModal()" aria-label="Close experimental video">
            <i class="fas fa-times"></i>
        </button>
        <div class="video-modal-content">
            <video id="modalVideo" controls>
                Your browser does not support the video tag.
            </video>
        </div>
        <div id="videoModalCaption" class="video-modal-caption"></div>
    </div>

    <!-- Floating CTA -->
    <a href="#human-practices" class="floating-cta">
        <i class="fas fa-microscope"></i>
        View Research Data
    </a>

    <script>
        // ====== ENHANCED INITIALIZATION ======
        function initMediaData() {{
            const hpMedia = Array.from(document.querySelectorAll('#hp-gallery .media-card'));
            const artMedia = Array.from(document.querySelectorAll('#art-gallery .media-card'));

            allMedia = [
                ...hpMedia.map((card, index) => ({{
                    element: card,
                    type: card.classList.contains('video-card') ? 'video' : 'image',
                    src: card.querySelector('.media-preview').src || card.querySelector('video source').src,
                    title: card.querySelector('.media-title').textContent,
                    description: card.querySelector('.media-description p').textContent,
                    date: card.querySelector('.media-date').textContent.replace('• ', ''),
                    gallery: 'human-practices',
                    index: index
                }})),
                ...artMedia.map((card, index) => ({{
                    element: card,
                    type: card.classList.contains('video-card') ? 'video' : 'image',
                    src: card.querySelector('.media-preview').src || card.querySelector('video source').src,
                    title: card.querySelector('.media-title').textContent,
                    description: card.querySelector('.media-description p').textContent,
                    date: card.querySelector('.media-date').textContent.replace('• ', ''),
                    gallery: 'art-design',
                    index: index + hpMedia.length
                }}))
            ];

            updateEnhancedStats();
            initVideoDurations();
            initScientificInteractions();
        }}

        // ====== ENHANCED STATISTICS ======
        function updateEnhancedStats() {{
            const hpMedia = allMedia.filter(m => m.gallery === 'human-practices');
            const artMedia = allMedia.filter(m => m.gallery === 'art-design');

            const hpPhotos = hpMedia.filter(m => m.type === 'image').length;
            const hpVideos = hpMedia.filter(m => m.type === 'video').length;
            const artPhotos = artMedia.filter(m => m.type === 'image').length;
            const totalPhotos = hpPhotos + artPhotos;
            const totalVideos = hpVideos;
            const totalMedia = allMedia.length;
            const currentYear = new Date().getFullYear();

            const statsHTML = 
                '<div class="stat-card">' +
                    '<div class="stat-icon">🧬</div>' +
                    '<div class="stat-number">' + totalMedia + '</div>' +
                    '<div class="stat-label">Research Datasets</div>' +
                '</div>' +
                '<div class="stat-card">' +
                    '<div class="stat-icon">🔬</div>' +
                    '<div class="stat-number">' + totalPhotos + '</div>' +
                    '<div class="stat-label">Experimental Images</div>' +
                '</div>' +
                '<div class="stat-card">' +
                    '<div class="stat-icon">🎥</div>' +
                    '<div class="stat-number">' + totalVideos + '</div>' +
                    '<div class="stat-label">Protocol Videos</div>' +
                '</div>' +
                '<div class="stat-card">' +
                    '<div class="stat-icon">📈</div>' +
                    '<div class="stat-number">' + currentYear + '</div>' +
                    '<div class="stat-label">Research Year</div>' +
                '</div>';

            document.getElementById('mediaStats').innerHTML = statsHTML;
        }}

        // ====== ENHANCED MEDIA VIEWER ======
        function enlargeImage(btn) {{
            if (isModalOpen) return;
            const card = btn.closest('.media-card');
            openMediaModal(card, 'image');
        }}

        function playVideo(btn) {{
            if (isModalOpen) return;
            const card = btn.closest('.media-card');
            openMediaModal(card, 'video');
        }}

        function openMediaModal(card, mediaType) {{
            currentGallery = card.closest('#hp-gallery') ? 'human-practices' : 'art-design';
            currentMediaIndex = allMedia.findIndex(m => m.element === card);

            if (currentMediaIndex === -1) {{
                console.error('Research data not found');
                return;
            }}

            if (mediaType === 'image') {{
                const modal = document.getElementById('imageModal');
                const modalImg = document.getElementById('modalImage');
                const caption = document.getElementById('modalCaption');

                modal.style.display = 'flex';
                modalImg.style.display = 'none';
                modalImg.src = '';
                modalImg.alt = allMedia[currentMediaIndex].title;

                modalImg.src = allMedia[currentMediaIndex].src;
                caption.textContent = allMedia[currentMediaIndex].title + ' • ' + allMedia[currentMediaIndex].date;

                setTimeout(() => {{
                    modal.classList.add('show');
                    isModalOpen = true;
                }}, 10);
            }} else if (mediaType === 'video') {{
                const modal = document.getElementById('videoModal');
                const modalVideo = document.getElementById('modalVideo');
                const caption = document.getElementById('videoModalCaption');

                modal.style.display = 'flex';
                modalVideo.src = '';
                modalVideo.load();

                modalVideo.src = allMedia[currentMediaIndex].src;
                caption.textContent = allMedia[currentMediaIndex].title + ' • ' + allMedia[currentMediaIndex].date;

                setTimeout(() => {{
                    modal.classList.add('show');
                    isModalOpen = true;

                    // Enhanced video playback
                    modalVideo.play().then(() => {{
                        console.log('Experimental video analysis started');
                    }}).catch(e => {{
                        console.log('Video analysis requires user interaction:', e);
                    }});
                }}, 10);
            }}
        }}

        function mediaLoaded() {{
            const modalImg = document.getElementById('modalImage');
            modalImg.style.display = 'block';
        }}

        function closeModal() {{
            const modal = document.getElementById('imageModal');
            modal.classList.remove('show');
            isModalOpen = false;

            setTimeout(() => {{
                modal.style.display = 'none';
            }}, 400);
        }}

        function closeVideoModal() {{
            const modal = document.getElementById('videoModal');
            const video = document.getElementById('modalVideo');

            video.pause();
            modal.classList.remove('show');
            isModalOpen = false;

            setTimeout(() => {{
                modal.style.display = 'none';
                video.src = '';
            }}, 400);
        }}

        function navigateMedia(direction) {{
            if (allMedia.length === 0) return;

            currentMediaIndex += direction;
            if (currentMediaIndex >= allMedia.length) currentMediaIndex = 0;
            if (currentMediaIndex < 0) currentMediaIndex = allMedia.length - 1;

            const mediaData = allMedia[currentMediaIndex];

            if (mediaData.type === 'image') {{
                closeVideoModal();
                const modalImg = document.getElementById('modalImage');
                const caption = document.getElementById('modalCaption');

                modalImg.style.display = 'none';
                modalImg.src = mediaData.src;
                modalImg.alt = mediaData.title;
                caption.textContent = mediaData.title + ' • ' + mediaData.date;
            }} else {{
                closeModal();
                const modalVideo = document.getElementById('modalVideo');
                const caption = document.getElementById('videoModalCaption');

                modalVideo.src = mediaData.src;
                modalVideo.load();
                caption.textContent = mediaData.title + ' • ' + mediaData.date;

                modalVideo.play().then(() => {{
                    console.log('Experimental video analysis continued');
                }}).catch(e => {{
                    console.log('Video analysis requires user interaction:', e);
                }});
            }}

            currentGallery = mediaData.gallery;
        }}

        // ====== ENHANCED VIDEO DURATION ======
        function initVideoDurations() {{
            document.querySelectorAll('video.media-preview').forEach(video => {{
                video.addEventListener('loadedmetadata', function() {{
                    const duration = Math.floor(video.duration);
                    const minutes = Math.floor(duration / 60);
                    const seconds = duration % 60;
                    const durationElement = video.parentElement.querySelector('.media-duration');
                    if (durationElement) {{
                        durationElement.textContent = minutes + ':' + seconds.toString().padStart(2, '0');
                    }}
                }});
            }});
        }}

        // ====== SCIENTIFIC INTERACTIONS ======
        function initScientificInteractions() {{
            // Add hover effects to scientific elements
            document.querySelectorAll('.media-card').forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.zIndex = '10';
                }});

                card.addEventListener('mouseleave', function() {{
                    this.style.zIndex = '1';
                }});
            }});

            // Add loading animation to images
            document.querySelectorAll('.media-preview').forEach(img => {{
                img.addEventListener('load', function() {{
                    this.style.opacity = '1';
                    this.style.transform = 'scale(1)';
                }});

                img.style.opacity = '0';
                img.style.transform = 'scale(0.95)';
                img.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            }});
        }}

        // ====== ENHANCED KEYBOARD NAVIGATION ======
        document.addEventListener('keydown', function(event) {{
            if (!isModalOpen) return;

            if (event.key === 'Escape') {{
                const imageModal = document.getElementById('imageModal');
                const videoModal = document.getElementById('videoModal');

                if (imageModal.classList.contains('show')) {{
                    closeModal();
                }} else if (videoModal.classList.contains('show')) {{
                    closeVideoModal();
                }}
            }} else if (event.key === 'ArrowRight') {{
                navigateMedia(1);
            }} else if (event.key === 'ArrowLeft') {{
                navigateMedia(-1);
            }} else if (event.key === ' ') {{
                event.preventDefault();
                const videoModal = document.getElementById('videoModal');
                const video = document.getElementById('modalVideo');
                if (videoModal.classList.contains('show')) {{
                    if (video.paused) {{
                        video.play();
                    }} else {{
                        video.pause();
                    }}
                }}
            }}
        }});

        // ====== ENHANCED INITIALIZATION ======
        document.addEventListener('DOMContentLoaded', function() {{
            initMediaData();

            // Enhanced background click to close modals
            document.getElementById('imageModal').addEventListener('click', function(event) {{
                if (event.target === this) {{
                    closeModal();
                }}
            }});

            document.getElementById('videoModal').addEventListener('click', function(event) {{
                if (event.target === this) {{
                    closeVideoModal();
                }}
            }});

            // Add scroll animations
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};

            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);

            document.querySelectorAll('.section, .stat-card').forEach(el => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            }});
        }});

        // Global variables
        let allMedia = [];
        let currentMediaIndex = 0;
        let currentGallery = '';
        let isModalOpen = false;
    </script>
</body>
</html>'''


def main():
    """主函数：构建增强版科学风格网站"""
    print("🧬 Building Advanced Nature-Style Research Media Archive...")

    # 定义媒体类型
    image_types = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.tiff', '*.bmp']
    video_types = ['*.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
    all_media_types = image_types + video_types

    # 扫描媒体目录
    print("🔍 Scanning for scientific research media files...")
    art_media = get_media_files('ART', all_media_types)
    hp_media = get_media_files('HP', all_media_types)

    # 统计信息
    art_images = len([m for m in art_media if is_image_file(m)])
    hp_images = len([m for m in hp_media if is_image_file(m)])
    hp_videos = len([m for m in hp_media if is_video_file(m)])

    print(f"🎨 Found {art_images} scientific visualization assets")
    print(f"📸 Found {hp_images} experimental documentation images")
    print(f"🎥 Found {hp_videos} protocol video records")
    print(f"📊 Total: {len(art_media) + len(hp_media)} research datasets")

    # 生成媒体HTML
    art_html = generate_media_html(art_media, 'art-design')
    hp_html = generate_media_html(hp_media, 'human-practices')

    # 创建时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 生成集成版本HTML
    integrated_html = create_hp_integrated_html(hp_html, art_html, timestamp)

    # 写入文件
    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(integrated_html)

    print("✅ Advanced Nature-Style Research Media Archive built successfully!")
    print("📄 Generated: gallery.html")
    print("🎯 Enhanced Scientific Features:")
    print("   - 🧬 Enhanced DNA helix with multiple colors and animations")
    print("   - 🔬 Advanced cell structure with organelles")
    print("   - ⚛️  Molecular clusters with chemical bonds")
    print("   - 🌀 Protein folding animations")
    print("   - 🎨 Enhanced Nature journal color palette")
    print("   - 📐 Improved layout and typography")
    print("   - ✨ Enhanced hover effects and transitions")
    print("   - 📱 Better responsive design")
    print("   - 🔍 Improved scientific terminology")
    print("   - 🎯 Floating CTA for better navigation")


if __name__ == "__main__":
    main()
