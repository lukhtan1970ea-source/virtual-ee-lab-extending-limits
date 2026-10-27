import streamlit as st
import streamlit.components.v1 as components

def interactive_bench(stage_name, key=None):
    """
    Абсолютно стабільний кастомний компонент для інтерактивного стенду.
    Увесь код зібрано в один файл для уникнення проблем із правами доступу на Streamlit Cloud.
    """
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            #canvas-container {{
                text-align: center;
                font-family: 'Courier New', monospace;
            }}
            canvas {{
                border: 3px solid #4A4A4A;
                background-color: #F5F5F5;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
                border-radius: 8px;
                cursor: default;
            }}
            .controls {{
                margin-top: 10px;
            }}
            button {{
                background-color: #FF4B4B;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
            }}
            button:hover {{
                background-color: #E03E3E;
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container">
            <canvas id="benchCanvas" width="700" height="400"></canvas>
            <div class="controls">
                <button id="clearBtn">🧹 Очистити всі дроти</button>
            </div>
        </div>

        <script>
            function sendDataToPython(wires, knobAngle) {{
                const data = {{ wires: wires, knobAngle: knobAngle }};
                window.parent.postMessage({{
                    isStreamlitMessage: true,
                    type: "streamlit:setComponentValue",
                    value: data
                }}, "*");
            }}

            const canvas = document.getElementById('benchCanvas');
            const ctx = canvas.getContext('2d');
            const clearBtn = document.getElementById('clearBtn');

            let currentStage = "{stage_name}";
            let isInitialized = true; // У цьому режимі ініціалізація миттєва
            
            let wires = [];
            let activeTerminal = null;
            let mouseX = 0;
            let mouseY = 0;
            let isDrawing = false;
            
            let knob = {{ x: 150, y: 320, r: 25, angle: 0, isDragging: false }};

            const terminals = [
                {{ id: "source_plus", name: "Джерело +", x: 50, y: 60, r: 8, color: "#FF4B4B" }},
                {{ id: "source_minus", name: "Джерело -", x: 50, y: 120, r: 8, color: "#1E1E1E" }},
                {{ id: "ua_plus", name: "μA +", x: 320, y: 60, r: 8, color: "#FF4B4B" }},
                {{ id: "ua_minus", name: "μA -", x: 380, y: 60, r: 8, color: "#1E1E1E" }},
                {{ id: "ep_in", name: "ЕП Вхід", x: 560, y: 100, r: 8, color: "#FFA500" }},
                {{ id: "ep_com", name: "ЕП Спільний", x: 620, y: 100, r: 8, color: "#1E1E1E" }},
                {{ id: "r2_1", name: "R2 контакт 1", x: 340, y: 220, r: 8, color: "#666" }},
                {{ id: "r2_2", name: "R2 контакт 2", x: 420, y: 220, r: 8, color: "#666" }},
                {{ id: "r1_top", name: "R1 Верх", x: 110, y: 280, r: 6, color: "#666" }},
                {{ id: "r1_bot", name: "R1 Ниж", x: 190, y: 280, r: 6, color: "#666" }},
                {{ id: "r1_wiper", name: "R1 Повзунок", x: 150, y: 250, r: 6, color: "#32CD32" }}
            ];

            if (currentStage === "stage2") {{
                terminals.push({{ id: "rsh_1", name: "Rш контакт 1", x: 320, y: 140, r: 8, color: "#8B008B" }});
                terminals.push({{ id: "rsh_2", name: "Rш контакт 2", x: 380, y: 140, r: 8, color: "#8B008B" }});
            }}
            function drawBench() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // 1. Джерело живлення
                ctx.fillStyle = "#EAEAEA";
                ctx.fillRect(20, 20, 120, 130);
                ctx.strokeStyle = "#333";
                ctx.strokeRect(20, 20, 120, 130);
                ctx.fillStyle = "#333";
                ctx.font = "bold 12px Arial";
                ctx.fillText("Джерело =U", 35, 40);

                // 2. Мікроамперметр
                ctx.fillStyle = "#FFFDD0";
                ctx.fillRect(280, 20, 140, 100);
                ctx.strokeRect(280, 20, 140, 100);
                ctx.fillStyle = "#333";
                ctx.fillText("Мікроамперметр", 295, 40);

                // 3. Еталонний прилад В7-21А
                ctx.fillStyle = "#3A3A3A";
                ctx.fillRect(520, 20, 160, 110);
                ctx.strokeRect(520, 20, 160, 110);
                ctx.fillStyle = "#000";
                ctx.fillRect(535, 35, 130, 40);
                ctx.fillStyle = "#FF3333";
                ctx.font = "bold 20px 'Courier New'";
                ctx.fillText("В7-21А", 555, 30);

                // 4. Резистор R2
                ctx.fillStyle = "#DEB887";
                ctx.fillRect(330, 190, 100, 40);
                ctx.strokeRect(330, 190, 100, 40);
                ctx.fillStyle = "#333";
                ctx.font = "12px Arial";
                ctx.fillText("Резистор R2", 345, 212);

                // 5. Потенціометр R1
                ctx.fillStyle = "#D3D3D3";
                ctx.fillRect(80, 220, 140, 130);
                ctx.strokeRect(80, 220, 140, 130);
                ctx.fillStyle = "#333";
                ctx.fillText("Регулятор R1", 110, 240);
                
                ctx.beginPath();
                ctx.arc(knob.x, knob.y, knob.r, 0, 2 * Math.PI);
                ctx.fillStyle = "#666";
                ctx.fill();
                ctx.stroke();
                
                ctx.beginPath();
                ctx.moveTo(knob.x, knob.y);
                ctx.lineTo(knob.x + knob.r * Math.cos(knob.angle), knob.y + knob.r * Math.sin(knob.angle));
                ctx.strokeStyle = "#FFF";
                ctx.lineWidth = 3;
                ctx.stroke();
                ctx.lineWidth = 1;

                if (currentStage === "stage2") {
                    ctx.fillStyle = "#E6E6FA";
                    ctx.fillRect(310, 125, 80, 30);
                    ctx.strokeRect(310, 125, 80, 30);
                    ctx.fillStyle = "#333";
                    ctx.fillText("Шунт Rш", 325, 142);
                }

                terminals.forEach(t => {
                    ctx.beginPath();
                    ctx.arc(t.x, t.y, t.r, 0, 2 * Math.PI);
                    ctx.fillStyle = t.color;
                    ctx.fill();
                    ctx.strokeStyle = "#000";
                    ctx.stroke();
                });

                wires.forEach(w => {
                    ctx.beginPath();
                    ctx.moveTo(w.from.x, w.from.y);
                    ctx.lineTo(w.to.x, w.to.y);
                    ctx.strokeStyle = w.from.id.includes("plus") ? "#FF3333" : (w.from.id.includes("minus") ? "#111111" : "#4682B4");
                    ctx.lineWidth = 4;
                    ctx.lineCap = "round";
                    ctx.stroke();
                });

                if (isDrawing && activeTerminal) {
                    ctx.beginPath();
                    ctx.moveTo(activeTerminal.x, activeTerminal.y);
                    ctx.lineTo(mouseX, mouseY);
                    ctx.strokeStyle = activeTerminal.id.includes("plus") ? "#FF3333" : (activeTerminal.id.includes("minus") ? "#111111" : "#4682B4");
                    ctx.lineWidth = 3;
                    ctx.stroke();
                }
            }
            function getTerminalAt(x, y) {
                return terminals.find(t => Math.hypot(t.x - x, t.y - y) < t.r + 5);
            }

            function isOverKnob(x, y) {
                return Math.hypot(knob.x - x, knob.y - y) < knob.r;
            }

            canvas.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                mouseX = e.clientX - rect.left;
                mouseY = e.clientY - rect.top;

                const overTerminal = getTerminalAt(mouseX, mouseY);
                const overKnob = isOverKnob(mouseX, mouseY);
                
                if (overTerminal || overKnob || knob.isDragging) {
                    canvas.style.cursor = 'pointer';
                    canvas.title = overTerminal ? overTerminal.name : "";
                } else {
                    canvas.style.cursor = 'default';
                }

                if (knob.isDragging) {
                    knob.angle = Math.atan2(mouseY - knob.y, mouseX - knob.x);
                    drawBench();
                    if (isInitialized) sendDataToPython(wires, knob.angle);
                }

                if (isDrawing) {
                    drawBench();
                }
            });

            canvas.addEventListener('mousedown', (e) => {
                if (e.button !== 0) return;
                const t = getTerminalAt(mouseX, mouseY);
                if (t) {
                    isDrawing = true;
                    activeTerminal = t;
                } else if (isOverKnob(mouseX, mouseY)) {
                    knob.isDragging = true;
                }
            });

            canvas.addEventListener('mouseup', (e) => {
                if (knob.isDragging) {
                    knob.isDragging = false;
                    return;
                }

                if (isDrawing) {
                    const targetTerminal = getTerminalAt(mouseX, mouseY);
                    if (targetTerminal && targetTerminal.id !== activeTerminal.id) {
                        const alreadyExists = wires.some(w => 
                            (w.from.id === activeTerminal.id && w.to.id === targetTerminal.id) ||
                            (w.from.id === targetTerminal.id && w.to.id === activeTerminal.id)
                        );
                        if (!alreadyExists) {
                            wires.push({ from: activeTerminal, to: targetTerminal });
                            if (isInitialized) sendDataToPython(wires, knob.angle);
                        }
                    }
                    isDrawing = false;
                    activeTerminal = null;
                    drawBench();
                }
            });

            canvas.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                for (let i = wires.length - 1; i >= 0; i--) {
                    let w = wires[i];
                    let dist = Math.abs((w.to.y - w.from.y)*mouseX - (w.to.x - w.from.x)*mouseY + w.to.x*w.from.y - w.to.y*w.from.x) / Math.hypot(w.to.x - w.from.x, w.to.y - w.from.y);
                    if (dist < 8) {
                        wires.splice(i, 1);
                        if (isInitialized) sendDataToPython(wires, knob.angle);
                        drawBench();
                        break;
                    }
                }
            });

            clearBtn.addEventListener('click', () => {
                wires = [];
                if (isInitialized) sendDataToPython(wires, knob.angle);
                drawBench();
            });

            drawBench();
            // Первинне сповіщення Python, щоб ініціалізувати state
            setTimeout(() => { sendDataToPython(wires, knob.angle); }, 100);
        </script>
    </body>
    </html>
    """
    
    # Викликаємо чистий рендер без залучення файлової системи сервера
    return components.html(html_code, height=470, key=key)
