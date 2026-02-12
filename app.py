from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sindh: Craft + Computation</title>
    <style>
        /* --- 1. THE BACKGROUND (Using your bg.png) --- */
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            
            /* The Background Image */
            background-color: #1a100e; 
            background-image: url('/static/pngs/bg.png'); 
            background-size: cover;     /* Stretches image to fit screen */
            background-position: center;
            background-repeat: no-repeat;
            
            font-family: 'Courier New', monospace;
            overflow: hidden;
        }

        /* --- 2. THE MAP FRAME (The Box) --- */
        .map-frame {
            position: relative;
            width: 700px;
            height: 700px;
            
            /* Decorative Border */
            border: 20px solid #5d2823; 
            outline: 4px dashed #ffcc00; /* Gold stitching */
            
            /* Shadow to make it pop off the background */
            box-shadow: 0 0 80px rgba(0,0,0,0.9); 
            
            /* Dark semi-transparent background so map is readable */
            background: rgba(20, 10, 5, 0.85); 
            backdrop-filter: blur(2px); /* Blurs the bg.png slightly behind the map */
            
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 10px;
        }

        /* --- 3. MAP ELEMENTS --- */
        svg { width: 100%; height: 100%; overflow: visible; }

        .land-shape {
            fill: url(#rugPattern); 
            stroke: #ffbd4a; stroke-width: 2px;
            filter: drop-shadow(0 0 10px rgba(0,0,0,0.8));
        }

        .network-line {
            fill: none; stroke: #00e5ff; stroke-width: 2px;
            stroke-dasharray: 5, 5; opacity: 0.6;
            animation: flow 2s linear infinite;
        }

        @keyframes flow {
            from { stroke-dashoffset: 10; }
            to { stroke-dashoffset: 0; }
        }

        /* --- 4. INTERACTIVE ICONS --- */
        .city-group {
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .city-group:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 15px #ffcc00);
            z-index: 50;
        }
        .city-label {
            fill: white; font-size: 14px; font-weight: bold;
            text-shadow: 0 0 4px black; text-anchor: middle;
            pointer-events: none;
        }

        /* --- 5. THE POP-UP MODAL (Hidden by default) --- */
        .modal-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(5px);
            display: none; /* Hidden initially */
            justify-content: center;
            align-items: center;
            z-index: 100;
        }

        .modal-box {
            width: 400px;
            background: #2d1c19; /* Dark brown card */
            border: 2px solid #ffcc00;
            padding: 25px;
            color: #fff;
            box-shadow: 0 0 30px #ffcc00;
            position: relative;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.3s ease;
            text-align: left;
        }

        /* Animation class */
        .modal-open .modal-box {
            transform: translateY(0);
            opacity: 1;
        }

        .modal-header {
            font-family: 'Brush Script MT', cursive;
            font-size: 2.5rem;
            color: #ffcc00;
            margin-bottom: 15px;
            border-bottom: 1px dashed #555;
            padding-bottom: 10px;
        }

        .modal-content p {
            line-height: 1.6;
            font-size: 1rem;
        }

        .close-btn {
            position: absolute;
            top: 10px; right: 15px;
            font-size: 24px;
            cursor: pointer;
            color: #ffcc00;
            transition: color 0.2s;
        }
        .close-btn:hover { color: white; }

        /* Title Overlay */
        .title-container {
            position: absolute; 
            top: 30px; left: 30px; 
            color: #eee; 
            z-index: 10;
            pointer-events: none;
        }
        h1 { margin: 0; font-family: 'Brush Script MT', cursive; font-size: 3rem; text-shadow: 3px 3px 0 #000; }
        h2 { margin: 0; font-size: 0.9rem; color: #ffcc00; text-transform: uppercase; letter-spacing: 2px; text-shadow: 2px 2px 0 #000; }

    </style>
</head>
<body>

    <div class="map-frame">
        <div class="title-container">
            <h1>Sindh</h1>
            <h2>Craft + Computation</h2>
        </div>

        <div id="infoModal" class="modal-overlay" onclick="closeModal()">
            <div class="modal-box" onclick="event.stopPropagation()">
                <span class="close-btn" onclick="closeModal()">&times;</span>
                <div id="modalTitle" class="modal-header">City Name</div>
                <div id="modalBody" class="modal-content">
                    <p>Details about the craft go here...</p>
                </div>
            </div>
        </div>

        <svg viewBox="0 0 500 600">
            <defs>
                <pattern id="rugPattern" patternUnits="userSpaceOnUse" width="40" height="40">
                    <rect width="40" height="40" fill="#601010"/> 
                    <circle cx="20" cy="20" r="5" fill="#300505"/> 
                </pattern>
            </defs>

            <path class="land-shape" d="M 150 60 L 300 30 L 380 120 L 420 180 L 320 500 L 220 550 L 80 480 L 40 350 L 100 150 Z" />

            <path class="network-line" d="M 120 450 L 220 350" />
            <path class="network-line" d="M 220 350 L 320 150" />
            <path class="network-line" d="M 200 180 L 320 150" />

            <g class="city-group" onclick="openCity('karachi')">
                <image href="/static/pngs/karachi.png" x="90" y="420" width="60" height="60" />
                <text class="city-label" x="120" y="500">KARACHI</text>
            </g>

            <g class="city-group" onclick="openCity('hyderabad')">
                <image href="/static/pngs/hyderabad.png" x="190" y="320" width="60" height="60" />
                <text class="city-label" x="220" y="400">HYDERABAD</text>
            </g>

            <g class="city-group" onclick="openCity('sukkur')">
                <image href="/static/pngs/sukkur.png" x="290" y="120" width="60" height="60" />
                <text class="city-label" x="320" y="115">SUKKUR</text>
            </g>

            <g class="city-group" onclick="openCity('larkana')">
                <image href="/static/pngs/larkana.png" x="170" y="150" width="60" height="60" />
                <text class="city-label" x="200" y="145">LARKANA</text>
            </g>

        </svg>
    </div>

    <script>
        const cityData = {
            'karachi': {
                title: "Karachi",
                desc: "<b>The Port & The Pattern.</b><br><br>While known as a modern metropolis, Karachi's craft history is rooted in the coastal shell-works and the vibrant diversity of its migrant artisans. <br><br><i>Key Craft:</i> Shell Carving, Modern Fusion Embroidery."
            },
            'hyderabad': {
                title: "Hyderabad",
                desc: "<b>The City of Glass & Geometry.</b><br><br>Famous for its delicate glass bangles (Chooriyan) and the geometric perfection of Ajrak block printing found in nearby Matiari.<br><br><i>Key Craft:</i> Ajrak Block Print, Glass Bangles, Kashi (Tile Work)."
            },
            'sukkur': {
                title: "Sukkur",
                desc: "<b>The River Gate.</b><br><br>Sukkur acts as the gateway to the date-palm forests. The women here stitch 'Ralli' quilts using vibrant scraps of fabric, creating abstract geometric art.<br><br><i>Key Craft:</i> Ralli (Patchwork Quilts), Date Leaf Weaving."
            },
            'larkana': {
                title: "Larkana",
                desc: "<b>The Ancient Thread.</b><br><br>Home to Mohenjo Daro, the designs found here date back 5000 years. The Sindhi Topi (Cap) with its mirror work reflects this ancient geometry.<br><br><i>Key Craft:</i> Sindhi Topi (Mirror Work), Ajrak."
            }
        };

        function openCity(cityName) {
            const modal = document.getElementById('infoModal');
            const title = document.getElementById('modalTitle');
            const body = document.getElementById('modalBody');

            const data = cityData[cityName];

            if(data) {
                title.innerText = data.title;
                body.innerHTML = data.desc;
                modal.style.display = 'flex';
                setTimeout(() => { modal.classList.add('modal-open'); }, 10);
            }
        }

        function closeModal() {
            const modal = document.getElementById('infoModal');
            modal.classList.remove('modal-open');
            setTimeout(() => { modal.style.display = 'none'; }, 300);
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)