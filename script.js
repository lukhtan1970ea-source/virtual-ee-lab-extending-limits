const canvas = document.getElementById('benchCanvas'); 
const ctx = canvas.getContext('2d'); 
const clearBtn = document.getElementById('clearBtn');

// Определение этапа лабораторной работы
let currentStage = window.name.includes("bench_s2") ? "stage2" : (window.name.includes("bench_s3") ? "stage3" : "stage1");

let wires = []; 
let activeTerminal = null; 
let mouseX = 0; 
let mouseY = 0; 
let isDrawing = false;

// Потенциометр со стопором (значение от 0.0 до 1.0)
let knob = { x: 150, y: 320, r: 25, value: 0.0, angle: -Math.PI * 0.75, isDragging: false };

// ОБНОВЛЕННАЯ СЕТКА КЛЕММ: Раздельный вход для Тока (I) и Напряжения (U)
// Нова розведена по вертикалі сітка клем (нічого не наповзає)
// Нова сітка клем: винесені за межі тіла деталей, без зайвих слів "вхід/вихід/плюс/мінус"
// Нова простора сітка клем: R2 зміщено вправо і вниз (під мультиметр)
const terminals = [
    { id: "source_plus", name: "Джерело +", x: 45, y: 75, r: 8, color: "#FF4B4B" },
    { id: "source_minus", name: "Джерело -", x: 115, y: 75, r: 8, color: "#1E1E1E" },
    
    { id: "ua_plus", name: "μA +", x: 310, y: 135, r: 8, color: "#FF4B4B" },
    { id: "ua_minus", name: "μA -", x: 380, y: 135, r: 8, color: "#1E1E1E" },
    
    { id: "ep_in_u", name: "ЕП Вхід U", x: 540, y: 135, r: 8, color: "#FF8C00" },
    { id: "ep_in_i", name: "ЕП Вхід I", x: 600, y: 135, r: 8, color: "#FF4B4B" },
    { id: "ep_com", name: "ЕП Спільний (0)", x: 660, y: 135, r: 8, color: "#1E1E1E" },
    
    // R2 зміщено вправо під мультиметр і вниз на y: 245
    { id: "r2_1", name: "R2", x: 515, y: 245, r: 8, color: "#666" },
    { id: "r2_2", name: "R2", x: 685, y: 245, r: 8, color: "#666" },
    
    { id: "r1_top", name: "R1", x: 30, y: 245, r: 6, color: "#666" },
    { id: "r1_bot", name: "R1", x: 270, y: 245, r: 6, color: "#666" },
    { id: "r1_wiper", name: "R1 Повзунок", x: 150, y: 175, r: 6, color: "#32CD32" }
];

// Клеми шунта винесені на x: 275 та x: 485 (корпус буде між ними від 300 до 460)
if (currentStage === "stage2") {
    terminals.push({ id: "rsh_1", name: "Rш", x: 275, y: 185, r: 8, color: "#8B008B" });
    terminals.push({ id: "rsh_2", name: "Rш", x: 485, y: 185, r: 8, color: "#8B008B" });
}

function hasWire(t1, t2) {
    return wires.some(w => (w.from.id === t1 && w.to.id === t2) || (w.from.id === t2 && w.to.id === t1));
}

function sendDataToStreamlit(vals) {
    window.parent.postMessage({
        type: "LAB_UPDATE", stage: currentStage, n: vals.n, val: vals.I_ep
    }, "*");
}

function isConnectedInside(t1, t2) {
    if ((t1 === "r1_top" || t1 === "r1_bot") && t2 === "r1_wiper") return true;
    if ((t2 === "r1_top" || t2 === "r1_bot") && t1 === "r1_wiper") return true;
    if (t1 === "ua_plus" && t2 === "ua_minus") return true;
    if (t2 === "ua_plus" && t1 === "ua_minus") return true;
    
    // Внутренние связи мультиметра зависят от гнезда подключения
    if (t1 === "ep_in_i" && t2 === "ep_com") return true;
    if (t2 === "ep_in_i" && t1 === "ep_com") return true;
    if (t1 === "ep_in_u" && t2 === "ep_com") return true;
    if (t2 === "ep_in_u" && t1 === "ep_com") return true;
    
    if (t1 === "r2_1" && t2 === "r2_2") return true;
    if (t2 === "r2_1" && t1 === "r2_2") return true;
    if (t1 === "rsh_1" && t2 === "rsh_2") return true;
    if (t2 === "rsh_1" && t1 === "rsh_2") return true;
    return false;
}
function checkCircuitConnected() {
    let visited = new Set();
    let queue = ["source_plus"];
    while (queue.length > 0) {
        let current = queue.shift();
        if (current === "source_minus") return true;
        if (!visited.has(current)) {
            visited.add(current);
            wires.forEach(w => {
                if (w.from.id === current && !visited.has(w.to.id)) queue.push(w.to.id);
                if (w.to.id === current && !visited.has(w.from.id)) queue.push(w.from.id);
            });
            terminals.forEach(t => {
                if (t.id !== current && !visited.has(t.id)) {
                    if (isConnectedInside(current, t.id)) queue.push(t.id);
                }
            });
        }
    }
    return false;
}

function getCircuitValues() {
    const has_power = hasWire("source_plus", "r1_top") && hasWire("source_minus", "r1_bot");
    const is_closed = checkCircuitConnected();
    
    // Проверяем, в какое именно гнездо мультиметра включен провод
    const connected_to_i = hasWire("ep_in_i", "ua_minus") || hasWire("ep_in_i", "r2_2") || hasWire("ep_in_i", "r2_1") || wires.some(w => w.from.id === "ep_in_i" || w.to.id === "ep_in_i");
    const connected_to_u = hasWire("ep_in_u", "ua_plus") || hasWire("ep_in_u", "ua_minus") || wires.some(w => w.from.id === "ep_in_u" || w.to.id === "ep_in_u");

    if (!has_power || !is_closed) return { I_ep: 0, n: 0, mode: currentStage === "stage3" ? "mV" : "μA" };

    let factor = knob.value; 

    if (currentStage === "stage1") {
        // Если на этапе амперметра подключились к гнезду вольтметра U — тока не будет (большое внутреннее сопротивление)
        if (!connected_to_i) return { I_ep: 0, n: 0, mode: "μA" };
        let I = factor * 250.0; 
        return { I_ep: I, n: I, mode: "μA" };
    } 
    else if (currentStage === "stage2") {
        if (!connected_to_i) return { I_ep: 0, n: 0, mode: "μA" };
        const has_shunt = hasWire("ua_plus", "rsh_1") && hasWire("ua_minus", "rsh_2");
        if (!has_shunt) {
            let I = factor * 250.0;
            return { I_ep: I, n: I, mode: "μA" };
        }
        let total_I = factor * 500.0;
        let I_micro = total_I / 10.0; 
        return { I_ep: total_I, n: I_micro, mode: "μA" };
    } 
    else { // stage3 (режим вольтметра)
        // Если на этапе вольтметра подключились к токовому гнезду I — будет КЗ или прибор выдаст 0
        if (!connected_to_u) return { I_ep: 0, n: 0, mode: "mV" };
        let U_mv = factor * 250.0;
        let n_div = U_mv / 5.0; 
        return { I_ep: U_mv, n: n_div, mode: "mV" };
    }
}
function drawMicroampermeter(n_val) {
    ctx.fillStyle = "#2B2B2B"; ctx.fillRect(260, 15, 170, 110); ctx.strokeRect(260, 15, 170, 110);
    ctx.fillStyle = "#FFFDD0"; ctx.fillRect(270, 20, 150, 80); 
    
    ctx.beginPath(); ctx.arc(345, 115, 80, -Math.PI * 0.78, -Math.PI * 0.22);
    ctx.strokeStyle = "#000"; ctx.lineWidth = 1.5; ctx.stroke();

    ctx.fillStyle = "#000"; ctx.font = "9px 'Courier New'"; ctx.textAlign = "center";
    for (let i = 0; i <= 50; i += 5) {
        let angle = -Math.PI * 0.75 + (i / 50.0) * (Math.PI * 0.5);
        let isMajor = (i % 10 === 0);
        let len = isMajor ? 6 : 3;
        let x1 = 345 + 80 * Math.cos(angle); let y1 = 115 + 80 * Math.sin(angle);
        let x2 = 345 + (80 - len) * Math.cos(angle); let y2 = 115 + (80 - len) * Math.sin(angle);
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
        if (isMajor) {
            let tx = 345 + 68 * Math.cos(angle); let ty = 115 + 68 * Math.sin(angle);
            ctx.fillText(i, tx, ty);
        }
    }
    ctx.font = "bold 12px Arial"; ctx.fillText("μА", 345, 85);

    let targetAngle = -Math.PI * 0.75 + (n_val / 50.0) * (Math.PI * 0.5);
    if (targetAngle < -Math.PI * 0.78) targetAngle = -Math.PI * 0.78; 
    if (targetAngle > -Math.PI * 0.20) targetAngle = -Math.PI * 0.20; 

    let sx = 345 + 78 * Math.cos(targetAngle); let sy = 115 + 78 * Math.sin(targetAngle);
    ctx.beginPath(); ctx.moveTo(345, 105); ctx.lineTo(sx, sy);
    ctx.strokeStyle = "#FF0000"; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.beginPath(); ctx.arc(345, 105, 3, 0, 2 * Math.PI); ctx.fillStyle = "#000"; ctx.fill();
}

function drawBench() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const vals = getCircuitValues();

    knob.angle = -Math.PI * 0.75 + knob.value * (Math.PI * 1.5);

    // 1. Джерело живлення
    ctx.fillStyle = "#EAEAEA"; ctx.fillRect(20, 15, 120, 110); ctx.strokeStyle = "#333"; ctx.strokeRect(20, 15, 120, 110);
    ctx.fillStyle = "#333"; ctx.font = "bold 11px Arial"; ctx.textAlign = "left"; ctx.fillText("Джерело =5V", 35, 40);

    // 2. Мікроамперметр
    drawMicroampermeter(vals.n);

    // 3. Вольтметр В7-21А
    ctx.fillStyle = "#222222"; ctx.fillRect(520, 15, 160, 110); ctx.strokeStyle = "#333"; ctx.strokeRect(520, 15, 160, 110);
    ctx.fillStyle = "#0A0A0A"; ctx.fillRect(530, 25, 140, 45);
    ctx.fillStyle = "#888"; ctx.font = "bold 9px Arial"; ctx.fillText("В7-21А МУЛЬТИМЕТР", 535, 20);
    
    ctx.fillStyle = "#FF1111"; ctx.font = "bold 22px 'Courier New'"; ctx.textAlign = "right";
    ctx.fillText(vals.I_ep.toFixed(vals.mode === "μA" ? 2 : 1), 640, 55);
    ctx.font = "10px Arial"; ctx.fillText(vals.mode, 665, 52);

    // 4. Резистор R2 (Переміщено вправо під мультиметр і вниз на y: 225)
    ctx.fillStyle = "#DEB887"; ctx.fillRect(430, 225, 140, 40); ctx.strokeStyle = "#333"; ctx.strokeRect(530, 225, 140, 40);
    ctx.fillStyle = "#333"; ctx.font = "12px Arial"; ctx.textAlign = "center"; ctx.fillText("R2 = 4 кОм", 600, 249);

    // 5. Потенціометр R1
    ctx.fillStyle = "#D3D3D3"; ctx.fillRect(50, 195, 200, 170); ctx.strokeStyle = "#333"; ctx.strokeRect(50, 195, 200, 170);
    ctx.fillStyle = "#333"; ctx.textAlign = "center"; ctx.fillText("R1", 150, 212);

    // Ручка потенціометра
    ctx.beginPath(); ctx.arc(knob.x, knob.y, knob.r, 0, 2 * Math.PI);
    ctx.fillStyle = "#555"; ctx.fill(); ctx.strokeStyle = "#222"; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(knob.x, knob.y);
    ctx.lineTo(knob.x + knob.r * Math.cos(knob.angle), knob.y + knob.r * Math.sin(knob.angle));
    ctx.strokeStyle = "#FFF"; ctx.lineWidth = 3; ctx.stroke();

    // 6. Опір Шунта (на Етапі 2 залишається по центру під мікроамперметром)
    if (currentStage === "stage2") {
        ctx.fillStyle = "#9370DB"; ctx.fillRect(300, 170, 160, 30); ctx.strokeStyle = "#333"; ctx.strokeRect(300, 170, 160, 30);
        ctx.fillStyle = "#FFF"; ctx.font = "10px Arial"; ctx.textAlign = "center"; ctx.fillText("Rш = 111.11 Ом", 380, 188);
    }

    // ВІЗУАЛІЗАЦІЯ КЛЕМ ТА ЇХ ЧИСТИХ ПІДПИСІВ З ЗОВНІШНІХ БОКІВ
    terminals.forEach(t => {
        ctx.beginPath(); ctx.arc(t.x, t.y, t.r, 0, 2 * Math.PI);
        ctx.fillStyle = t.color; ctx.fill(); ctx.strokeStyle = "#000"; ctx.stroke();
        
        ctx.fillStyle = "#1E1E1E"; ctx.font = "bold 9px monospace";
        
        // Правила автоматичного зсуву тексту для винесених бокових клем
        if (t.id === "rsh_1" || t.id === "r2_1" || t.id === "r1_top") {
            ctx.textAlign = "right";
            ctx.fillText(t.name, t.x - t.r - 4, t.y + 3);
        } else if (t.id === "rsh_2" || t.id === "r2_2" || t.id === "r1_bot") {
            ctx.textAlign = "left";
            ctx.fillText(t.name, t.x + t.r + 4, t.y + 3);
        } else if (t.y < 150) {
            ctx.textAlign = "center";
            ctx.fillText(t.name, t.x, t.y + t.r + 11);
        } else {
            ctx.textAlign = "center";
            ctx.fillText(t.name, t.x, t.y - t.r - 4);
        }
    });

    // Дроти
    wires.forEach(w => {
        ctx.beginPath(); ctx.moveTo(w.from.x, w.from.y);
        ctx.bezierCurveTo(w.from.x, w.from.y + 40, w.to.x, w.to.y + 40, w.to.x, w.to.y);
        ctx.strokeStyle = "#0055ff"; ctx.lineWidth = 3; ctx.stroke();
    });

    if (isDrawing && activeTerminal) {
        ctx.beginPath(); ctx.moveTo(activeTerminal.x, activeTerminal.y);
        ctx.lineTo(mouseX, mouseY); ctx.strokeStyle = "rgba(0, 85, 255, 0.5)"; ctx.lineWidth = 2; ctx.stroke();
    }
}

function updateCursor(x, y) {
    let hover = false;
    if (Math.hypot(x - knob.x, y - knob.y) < knob.r) hover = true;
    terminals.forEach(t => { if (Math.hypot(x - t.x, y - t.y) < t.r + 4) hover = true; });
    canvas.style.cursor = hover ? "pointer" : "default";
}

window.addEventListener('keydown', (e) => {
    if (document.activeElement !== canvas) return; 
    if (e.key === "ArrowLeft") {
        knob.value = Math.max(knob.value - 0.01, 0.0);
        drawBench(); sendDataToStreamlit(getCircuitValues());
        e.preventDefault();
    } else if (e.key === "ArrowRight") {
        knob.value = Math.min(knob.value + 0.01, 1.0);
        drawBench(); sendDataToStreamlit(getCircuitValues());
        e.preventDefault();
    }
});

canvas.addEventListener('mousedown', (e) => {
    canvas.focus(); 
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left; const y = e.clientY - rect.top;
    if (Math.hypot(x - knob.x, y - knob.y) < knob.r) { knob.isDragging = true; return; }
    terminals.forEach(t => { if (Math.hypot(x - t.x, y - t.y) < t.r + 4) { activeTerminal = t; isDrawing = true; } });
});

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left; mouseY = e.clientY - rect.top;
    updateCursor(mouseX, mouseY);
    if (knob.isDragging) {
        let rawAngle = Math.atan2(mouseY - knob.y, mouseX - knob.x);
        let norm = (rawAngle + Math.PI * 0.75) / (Math.PI * 1.5);
        if (norm < 0 && norm > -0.2) norm = 0;
        if (norm > 1 || norm <= -0.2) norm = 1;
        knob.value = Math.min(Math.max(norm, 0), 1);
        drawBench(); sendDataToStreamlit(getCircuitValues());
    } else if (isDrawing) {
        drawBench();
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (knob.isDragging) { knob.isDragging = false; return; }
    if (!isDrawing) return;
    isDrawing = false;
    terminals.forEach(t => {
        if (t !== activeTerminal && Math.hypot(mouseX - t.x, mouseY - t.y) < t.r + 4) {
            if (!hasWire(activeTerminal.id, t.id)) { wires.push({ from: activeTerminal, to: t }); drawBench(); sendDataToStreamlit(getCircuitValues()); }
        }
    });
    activeTerminal = null; drawBench();
});

clearBtn.addEventListener('click', () => { wires = []; drawBench(); sendDataToStreamlit({I_ep: 0, n: 0, mode: "μA"}); });
setInterval(drawBench, 100);

