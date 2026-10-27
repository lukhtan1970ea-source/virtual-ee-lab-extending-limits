import numpy as np

# Фізичні константи лабораторного стенду (номінали приладів)
I_0 = 50.0      # Максимальний струм мікроамперметра (мкА)
R_0 = 1000.0    # Внутрішній опір мікроамперметра (Ом)
R_2 = 4000.0    # Добавочний опір / навантаження (Ом)
R_sh = 111.11   # Опір шунта для розширення межі в 10 разів (k=10)
U_source = 5.0  # Напруга джерела живлення (В)

def has_wire(wires, t1, t2):
    """Перевіряє, чи з'єднав студент клему t1 з клемою t2"""
    if not wires:
        return False
    for w in wires:
        fid = w["from"]["id"]
        tid = w["to"]["id"]
        if (fid == t1 and tid == t2) or (fid == t2 and tid == t1):
            return True
    return False

def calculate_stage1(wires, angle):
    """Розрахунок для Етапу 1: Градуювання мікроамперметра (Рис. 1.6)"""
    is_correct = (
        has_wire(wires, "source_plus", "r1_top") and
        has_wire(wires, "source_minus", "r1_bot") and
        has_wire(wires, "r1_wiper", "ua_plus") and
        has_wire(wires, "ua_minus", "r2_1") and
        has_wire(wires, "r2_2", "ep_in") and
        (has_wire(wires, "ep_com", "r1_bot") or has_wire(wires, "ep_com", "source_minus"))
    )
    if not is_correct:
        is_short = has_wire(wires, "source_plus", "source_minus")
        return {"status": "short" if is_short else "error", "I": 0.0, "n": 0.0}
    
    r1_factor = (np.sin(angle) + 1) / 2.0
    R_1_eff = r1_factor * 5000.0
    total_R = R_0 + R_2 + R_1_eff
    current_I = (U_source / total_R) * 1e6
    n_div = (current_I / I_0) * 50.0
    return {"status": "ok", "I": current_I, "n": n_div}

def calculate_stage2(wires, angle):
    """Розрахунок для Етапу 2: Розширення межі амперметра (Рис. 1.7)"""
    has_shunt = has_wire(wires, "ua_plus", "rsh_1") and has_wire(wires, "ua_minus", "rsh_2")
    is_correct = (
        has_wire(wires, "source_plus", "r1_top") and
        has_wire(wires, "source_minus", "r1_bot") and
        has_wire(wires, "r1_wiper", "ua_plus") and
        has_shunt and 
        has_wire(wires, "ua_minus", "r2_1") and
        has_wire(wires, "r2_2", "ep_in") and
        (has_wire(wires, "ep_com", "r1_bot") or has_wire(wires, "ep_com", "source_minus"))
    )
    if not is_correct:
        return {"status": "error", "I": 0.0, "n": 0.0}
    
    r1_factor = (np.sin(angle) + 1) / 2.0
    R_1_eff = r1_factor * 1000.0
    R_parallel = (R_0 * R_sh) / (R_0 + R_sh)
    total_R = R_parallel + R_2 + R_1_eff
    total_I = (U_source / total_R) * 1e6
    I_micro = total_I * (R_sh / (R_0 + R_sh))
    n_div = (I_micro / I_0) * 50.0
    
    if I_micro > I_0 + 5:
        return {"status": "overload", "I": total_I, "n": 50.0}
    return {"status": "ok", "I": total_I, "n": n_div}

def calculate_stage3(wires, angle):
    """Розрахунок для Етапу 3: Градуювання вольтметра (Рис. 1.8)"""
    is_series_voltmeter = has_wire(wires, "ua_minus", "r2_1")
    is_ep_parallel = has_wire(wires, "ua_plus", "ep_in") and has_wire(wires, "r2_2", "ep_com")
    is_connected = has_wire(wires, "source_plus", "r1_top") and has_wire(wires, "source_minus", "r1_bot") and has_wire(wires, "r1_wiper", "ua_plus") and has_wire(wires, "r2_2", "source_minus")
    
    if not (is_series_voltmeter and is_ep_parallel and is_connected):
        return {"status": "error", "U": 0.0, "n": 0.0}
    
    r1_factor = (np.sin(angle) + 1) / 2.0
    R_1_eff = r1_factor * 3000.0
    R_voltmeter = R_0 + R_2
    total_R = R_1_eff + R_voltmeter
    I_circuit = U_source / total_R
    U_mv = (I_circuit * R_voltmeter) * 1000.0
    n_div = ((I_circuit * 1e6) / I_0) * 50.0
    return {"status": "ok", "U": U_mv, "n": n_div}

