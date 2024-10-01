from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

TAMANO_CUADRICULA = 4
FIGURAS = ['circulo', 'cuadrado', 'rectangulo', 'cono']
HUMANO = 1
IA = 2

tablero = [[None for _ in range(TAMANO_CUADRICULA)] for _ in range(TAMANO_CUADRICULA)]
piezas = {
    HUMANO: {'circulo': 2, 'cuadrado': 2, 'rectangulo': 2, 'cono': 2},
    IA: {'circulo': 2, 'cuadrado': 2, 'rectangulo': 2, 'cono': 2}
}

def es_movimiento_valido(fila, columna, figura, jugador):
    oponente = IA if jugador == HUMANO else HUMANO
    
    for i in range(TAMANO_CUADRICULA):
        if tablero[fila][i] and tablero[fila][i][0] == oponente and tablero[fila][i][1] == figura:
            return False
        if tablero[i][columna] and tablero[i][columna][0] == oponente and tablero[i][columna][1] == figura:
            return False

    region_fila, region_columna = fila // 2 * 2, columna // 2 * 2
    for i in range(region_fila, region_fila + 2):
        for j in range(region_columna, region_columna + 2):
            if tablero[i][j] and tablero[i][j][0] == oponente and tablero[i][j][1] == figura:
                return False

    return True

def colocar_pieza(fila, columna, figura, jugador):
    tablero[fila][columna] = (jugador, figura)
    piezas[jugador][figura] -= 1

def comprobar_ganador():
    for fila in range(TAMANO_CUADRICULA):
        if len(set(tablero[fila][col][1] for col in range(TAMANO_CUADRICULA) if tablero[fila][col])) == 4:
            return True

    for columna in range(TAMANO_CUADRICULA):
        if len(set(tablero[fila][columna][1] for fila in range(TAMANO_CUADRICULA) if tablero[fila][columna])) == 4:
            return True

    for fila_region in range(0, TAMANO_CUADRICULA, 2):
        for columna_region in range(0, TAMANO_CUADRICULA, 2):
            region = [tablero[fila_region + i][columna_region + j] for i in range(2) for j in range(2) if tablero[fila_region + i][columna_region + j]]
            if len(set(pieza[1] for pieza in region)) == 4:
                return True

    return False

def movimiento_ia():
    movimientos_validos = []
    for row in range(TAMANO_CUADRICULA):
        for col in range(TAMANO_CUADRICULA):
            if not tablero[row][col]:
                for shape in FIGURAS:
                    if piezas[IA][shape] > 0 and es_movimiento_valido(row, col, shape, IA):
                        movimientos_validos.append((row, col, shape))
    if movimientos_validos:
        return random.choice(movimientos_validos)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    fila, columna, figura = data['fila'], data['columna'], data['figura']
    
    if es_movimiento_valido(fila, columna, figura, HUMANO):
        colocar_pieza(fila, columna, figura, HUMANO)
        if comprobar_ganador():
            return jsonify({'status': 'win', 'winner': 'human', 'board': tablero})
        
        ia_move = movimiento_ia()
        if ia_move:
            colocar_pieza(*ia_move, IA)
            if comprobar_ganador():
                return jsonify({'status': 'win', 'winner': 'ia', 'board': tablero})
        
        return jsonify({'status': 'ok', 'board': tablero})
    else:
        return jsonify({'status': 'invalid'})

if __name__ == '__main__':
    app.run(debug=True)