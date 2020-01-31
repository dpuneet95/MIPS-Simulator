import re
import sys
import register

instructionsFile = open(sys.argv[1],'r')

instructions = []
instructions_out = []
isCompleted = False
LoadStoreDisp = 0
labels_list = []
validOperations = ['LW','SW','LD','L.D','S.D','SD','DADD','DADDI','DSUB','DSUBI','AND','ANDI','OR','ORI','ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD','J','BNE','BEQ','HLT']
validIntegerRegisters = ['R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R14','R15','R16','R17','R18','R19','R20','R21','R22','R23','R24','R25','R26','R27','R28','R29','R30','R31']
validFloatingPointRegisters = ['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24','F25','F26','F27','F28','F29','F30','F31']
loadOtherOperand = 0
instructCount = 1

class instruction:
    def __init__(self, operation, operand1,operand2,operand3,displacement):
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        self.displacement = displacement

def isaValidOperation(operation):
    if operation.strip(' ') not in validOperations:
        return False
    else:
        return True

def hasValidOperands(operation,operands,instructCount):
    global instructions, loadOtherOperand
    operandLength = len(operands)

    if (operandLength != 1 and operation == 'J'):
        print("Invalid number of operands for the operation J")
        return False
    elif ((operandLength == 3) and (operation not in ('BNE','BEQ','DADD','DADDI','DSUB','DSUBI','AND','ANDI','OR','ORI','ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD'))):
        print("Only Add, Sub, Mult, Div, Or, And, Bne, Beq can have 3 operands")
        return False
     elif (operandLength == 2 and (operation not in ('LW','SW','LD','L.D','S.D','SD'))):
        print("Only Load and Store instructions can have two operands")
        return False
    else:
        if (operation == 'LW'):
            loadOtherIntegerOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in validIntegerRegisters) or (loadOtherIntegerOperand not in validIntegerRegisters)):
                print("LW and SW can only have integer registers from R0 to R31")
                return False

        elif(operation in ('LD','L.D')):
            loadOtherOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in validFloatingPointRegisters) or (loadOtherOperand not in validIntegerRegisters)):
                print("LD can only have floating point registers from F0 to F31")
                return False
        
        elif (operation == 'SW'):
            loadOtherIntegerOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in validIntegerRegisters) or (loadOtherIntegerOperand not in validIntegerRegisters)):
                print("SW can only have integer registers from R0 to R31")
                return False

        elif(operation in ('SD','S.D')):
            loadOtherOperand = (re.search(r"\(([A-Za-z0-9_]+)\)", operands[1])).group(1)
            if ((operands[0].rstrip('\n') not in validFloatingPointRegisters) or (loadOtherOperand not in validIntegerRegisters)):
                print("S.D can only have floating point registers from F0 to F31")
                return False

        elif ((operation in ('DADDI','DSUBI','ANDI','ORI')) and ((operands[0].rstrip('\n') not in validIntegerRegisters) or (operands[1].rstrip('\n') not in validIntegerRegisters) or (not operands[2].rstrip('\n').isdigit()))):
            print("Integer immediate operations -  Add, Sub, And, Or can only have 2 integer registers and a numeric value")
            return False

        elif((operation in ('DADD','DSUB','AND','OR')) and ((operands[0].rstrip('\n') not in validIntegerRegisters) or (operands[1].rstrip('\n') not in validIntegerRegisters) or (operands[2].rstrip('\n') not in validIntegerRegisters))):
            print("Integer Add, Sub, And, Or can only have integer registers")
            return False

        elif((operation in ('ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD')) and ((operands[0].rstrip('\n') not in validFloatingPointRegisters) or (operands[1].rstrip('\n') not in validFloatingPointRegisters) or (operands[2].rstrip('\n') not in validFloatingPointRegisters))):
            print("FP Add, Sub, And, Or can only have floating point registers")
            return False

        elif((operation in ('BNE','BEQ')) and (operands[2].rstrip('\n') not in labels_list)):
            print("The given label not found")
            return False

        if len(operands)==0:
            instructions.append(instruction(operation,None,None,None,None))
        elif len(operands)==1:
            instructions.append(instruction(operation,operands[0].rstrip('\n'),None,None,None))
        elif len(operands)==2:
            global LoadStoreDisp
            disp = ''
            for i in operands[1]:
                if not i.isnumeric():
                    break
                else:
                    disp = disp + i
            LoadStoreDisp = int(disp)

            instructions.append(instruction(operation,operands[0].rstrip('\n'),loadOtherOperand,None,LoadStoreDisp))
        else:
            instructions.append(instruction(operation, operands[0].rstrip('\n'), operands[1].rstrip('\n'), operands[2].rstrip('\n'),None))
        return True

def instructionsAppend():
    global instructCount
    total_halts = 0

    for line in instructionsFile:
        values = []
        line_new = line.strip(' ').upper().rstrip('\n')

        if (line_new.__contains__('HLT')):
            total_halts = total_halts + 1
            if (total_halts == 2):
                continue

        instructions_out.append(line_new)

        if line_new.__contains__(':'):

            tempLabel = line_new.split(':')

            currLabel = (tempLabel[0]).strip()

            labels_list.append(currLabel)
            line_new = tempLabel[1].strip()

        line_new = line_new.rstrip('\n')
        splice = line_new.split()
        for val in splice:

            if(val == ','):
                continue
            else:
                values.append(val)

        operation = values[0]
        operands = values[1:]

        for i in range(0,len(operands)):
            operands[i] = operands[i].strip(',')

        isValidOp = isaValidOperation(operation)
        if (not isValidOp):
            print("Invalid operation type for instruction ",instructCount," !!!")
            break
        else:
            if(operation == 'HLT'):
                hasValidOpr = hasValidOperands(operation,[],instructCount)
            else:
                hasValidOpr = hasValidOperands(operation,operands,instructCount)
            if (not hasValidOpr):
                break
            else:
                instructCount += 1

instructionsAppend()
instructionsFile.close()
