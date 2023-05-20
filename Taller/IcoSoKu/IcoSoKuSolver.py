# icosoku problem AI
from ortools.sat.python import cp_model as cp
import numpy as np

# Solver
def icosoku_solver(clavijas):
    model = cp.CpModel()

    # Los valores de la A hasta la L, tomaran los valores de las 12 clavijas.
    A, B, C, D, E, F, G, H, I, J, K, L = clavijas

    # caras establece la relación entre los valores de las esquinas de cada cara del icosoku.
    caras =  np.array([
                (B, A, C), (A, D, C), (A, E, D), (E, A, F), (B, F, A), 
                (F, B, K), (G, K, B), (G, B, C), (H, G, C), (D, H, C), 
                (I, D, E), (D, I, H), (I, E, J), (E, F, J), (F, K, J), 
                (K, G, L), (H, L, G), (L, H, I), (L, I, J), (K, L, J) 
             ])

    # pesos guarda todas las caras que tiene el icosoku, un total de 20.
    pesos = np.array([(0,0,0), (0,0,1), (0,0,2), (0,0,3), (0,1,1), 
                      (0,1,2), (0,1,2), (0,1,2), (0,2,1), (0,2,1), 
                      (0,2,1), (0,2,2), (0,3,3), (1,1,1), (1,2,3), 
                      (1,2,3), (1,3,2), (1,3,2), (2,2,2), (3,3,3)
                    ])

    # pesos_r = [PuntosEsquina1, PuntosEsquina2, PuntosEsquina3, Rotación, NFicha]
    # Rotación puede tomar 3 valores: 0=0°, 1=120° y 2=240°
    # NFicha es un contador de 0 a 19 que identifica cada cara del icosoku
    pesos_r = []

    for NFicha, esquina in enumerate(pesos):
        if (esquina[0] == esquina[1] == esquina[2]): # En este caso al ser las caras iguales, no se toma en cuenta su rotación
            pesos_r.append([esquina[0], esquina[1], esquina[2], 0, NFicha])
        else:        
            pesos_r.append([esquina[0], esquina[1], esquina[2], 0, NFicha])             
            pesos_r.append([esquina[1], esquina[2], esquina[0], 1, NFicha])
            pesos_r.append([esquina[2], esquina[0], esquina[1], 2, NFicha])            

    # # # # Declaracion de variables CSP # # # #

    # Cada ficha incluye los posibles valores que pueden tener cada esquina de una cara, su rotación y su identificador
    fichas = []             
    for i in range(20):
        fila = [model.NewIntVar(0, 3, 'Esquina{}'.format(e)) for e in range(3)]
        fila.append(model.NewIntVar(0, 2, 'Rotación{}'.format(i))) 
        fila.append(model.NewIntVar(0, 19, 'Ficha{}'.format(i))) 
        fichas.append(fila)

    # # # # Definición de restricciones CSP # # # # 

    # 1. Cada ficha debe ser diferente.
    def get_var_ficha(x):
        return x[4]

    model.AddAllDifferent(list(map(get_var_ficha, fichas)))

    # 2. Restringe cada ficha al conjunto de posibilidades que existen.
    for i in range(20):
        model.AddAllowedAssignments(fichas[i], pesos_r)

    # 3. La suma de las esquinas debe ser igual a la clavija
    for clavija in clavijas:
        CaraEsquina = []
        for j, cara in enumerate(caras):
            if   clavija == cara[0]:
                CaraEsquina.append([j,0])
            elif clavija == cara[1]:
                CaraEsquina.append([j,1])
            elif clavija == cara[2]:
                CaraEsquina.append([j,2])

        model.Add(sum((fichas[i][j] for i,j in CaraEsquina)) == clavija)
        
    ###################PRINTER#########################

    solver = cp.CpSolver()
    solution_printer = SolutionPrinter(fichas, limit=1)
     
    status = solver.SearchForAllSolutions(model, solution_printer)  

    if not (status == cp.FEASIBLE or status == cp.OPTIMAL):
        print("No solution found!")

    str_out = solver.ResponseStats() + '\n'
    str_out += solution_printer.getSolution() 
    return str_out


class SolutionPrinter(cp.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, fichas, limit=0):
        cp.CpSolverSolutionCallback.__init__(self)

        self.__fichas = fichas
        self.__limit = limit
        self.__sol_fichas = []
        self.__solution_count = 0
        self.__sol_str = ""

    def OnSolutionCallback(self):
        
        caras_str = [   'BAC', 'ADC', 'AED', 'EAF', 'BFA', 
                        'FBK', 'GKB', 'GBC', 'HGC', 'DHC', 
                        'IDE', 'DIH', 'IEJ', 'EFJ', 'FKJ', 
                        'KGL', 'HLG', 'LHI', 'LIJ', 'KLJ'
                    ]

        self.__solution_count += 1
        
        self.__sol_str += 'Solution #{} \n'.format(self.__solution_count)

        for i in range(20):
            self.__sol_str += caras_str[i] + ': '
            for j in range(3):
                self.__sol_str += '{:3d} '.format(self.Value(self.__fichas[i][j]))
            self.__sol_str += ' F: {:2d}'.format(self.Value(self.__fichas[i][4]+1))

            if   (self.Value(self.__fichas[i][3]) == 0):
                self.__sol_str += '  R: 0°'
            elif (self.Value(self.__fichas[i][3]) == 1):
                self.__sol_str += '  R: 120°'
            elif (self.Value(self.__fichas[i][3]) == 2):
                self.__sol_str += '  R: 240°'
            self.__sol_str += '\n'
            
            if(self.__solution_count == 1):
                self.__sol_fichas.append(
                        [   self.Value(self.__fichas[i][0]),
                            self.Value(self.__fichas[i][1]),
                            self.Value(self.__fichas[i][2]),
                            self.Value(self.__fichas[i][3]),
                            self.Value(self.__fichas[i][4]) 
                        ]                
                    )   
        self.__sol_str += '\n'

        if self.__limit > 0 and self.__solution_count >= self.__limit:
            self.StopSearch() 

    def getSolution(self):
        return self.__sol_str

def main(clavijas):
    ''' 
        Función para ejecutar el solver.
        @param clavijas -> Arreglo de las 12 diferentes clavijas
    '''
    elementos_posibles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if len(set(clavijas)) == 12 and set(clavijas).issubset(set(elementos_posibles)) :
        out = icosoku_solver(clavijas)
        print(out)

    else:
        print("No se han ingresado las 12 clavijas correctamente!")
    
main([11, 5, 7, 2, 10, 3, 4, 9, 1, 12, 6, 8])
