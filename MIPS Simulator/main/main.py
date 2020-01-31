import parser
import register
import instructionCache
import dataCache
import configuration
import sys

IF = 0
ID = 0
EX = 0
WB = 0
RAW = 'N'
WAR = 'N'
WAW = 'N'
Struct = 'N'
index = 0
instructCacheHits = 0
dataCacheHits = 0
instructCacheRequests = 0
dataCacheRequests = 0
hasBranchInstruction = False
length = len(parser.instructions)
fromWriteBack = False
fromExecute = False
instructCachePenalty = 2 * (configuration.memory + configuration.iCache)
dataCachePenalty = 2 * (configuration.memory + configuration.dCache)
loop_number = 1
final_instructions = []
Load_StructureHazard = ['LW','SW','SD','S.D','L.D','LD','DADDI','DSUBI','ANDI','ORI']
Double_Add_Sub_StructureHazard = ['ADD.D','ADDD','SUB.D','SUBD']
Integer_Add_Sub_StructureHazard = ['DADD','DSUB']
IsCompleted = False

write_file = open(sys.argv[5],'w+')

class final_instruction:
    def __init__(self, fetch, decode, execute, write_back,raw,war,waw,struct_hazard):
        self.fetch = fetch
        self.decode = decode
        self.execute = execute
        self.write_back = write_back
        self.raw = raw
        self.war = war
        self.waw = waw
        self.struct_hazard = struct_hazard




def fetch(index):
    first_IF = 0
    second_IF = 0
    global IF, instructCacheHits, instructCacheRequests
    cache_index = (index % length)
    #print(index==0)
    #print("FETCHHHHHHHHHHHHHHHHHHHHHHHH")

    if (index == 0 and loop_number == 1):
        IF = instructCachePenalty
        instructionCache.isInstructionCacheMiss(inst.instructions[0], 0)
        #final_instructions[index].fetch = IF
        return
    else:
        #print("index",index)

        #print("Yes",instructionCache.isInstructionCacheMiss(inst.instructions[0], 0))
        #print("No",instructionCache.isInstructionCacheMiss(inst.instructions[1], 1))

        instructCacheRequests += 1
        if(instructionCache.isInstructionCacheMiss(inst.instructions[cache_index],cache_index)):

            #print("Is a miss")
            first_IF = final_instructions[index-1].fetch+instructCachePenalty
        else:
            instructCacheHits += 1
            first_IF = final_instructions[index-1].fetch+configuration.iCache
            #print("Is not a miss")



        second_IF = final_instructions[index-1].decode
        IF = max(first_IF,second_IF)





def decode(index):
    global ID
    global WAW,RAW,WAR
    cache_index = (index % length)
    first_ID = 0
    second_ID = 0
    third_ID = 0
    fourth_ID = 0

    if(inst.instructions[cache_index].operation == 'HLT'):
        ID = 0
        return

    first_ID = IF + 1

    current_operation = inst.instructions[cache_index].operation
    current_operand1 = inst.instructions[cache_index].operand1
    current_operand2 = inst.instructions[cache_index].operand2
    current_operand3 = inst.instructions[cache_index].operand3


    sec_op = 0
    third_op = 0

    if (index != 0):


        if (current_operation in ('LW','LD','L.D')):
            sec_op = 0
            third_op = 0

            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and prev_operand1 == current_operand2 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
            second_ID = sec_op


        if (current_operation in ('SW','SD','S.D')):

            for i in range(index - 1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1


                if (prev_operand1 == current_operand1 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
            second_ID = sec_op


        if (current_operation in ('DADD','DSUB','ADD.D','ADDD','SUB.D','SUBD','MULD','MUL.D','DIV.D','DIVD','AND','OR')):

            sec_op = 0
            third_op = 0
            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and current_operand2 == prev_operand1 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
                if ((prev_operation not in ('SW','SD','S.D')) and current_operand3 == prev_operand1 and final_instructions[i].write_back > first_ID):
                    third_op = final_instructions[i].write_back
                    RAW = 'Y'
            second_ID = max(sec_op,third_op)

        if (current_operation in ('DADDI','DSUBI','ANDI','ORI')):
            sec_op = 0
            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and prev_operand1 == current_operand2 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'

            second_ID = sec_op

        if(current_operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):
            for i in range(index - 1, 0, -1):
                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                if(prev_operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):
                    if (((final_instructions[i].execute - 1) - (final_instructions[i].decode + 1)) > 1):
                        second_ID = final_instructions[i].execute - 1


        if (current_operation in ('BNE','BEQ')):
            sec_op = 0
            for i in range(index-1, 0, -1):

                cache_index_loop = i % length

                prev_operation = inst.instructions[cache_index_loop].operation
                prev_operand1 = inst.instructions[cache_index_loop].operand1
                prev_operand2 = inst.instructions[cache_index_loop].operand2
                prev_operand3 = inst.instructions[cache_index_loop].operand3

                if ((prev_operation not in ('SW','SD','S.D')) and prev_operand2 == current_operand1 and final_instructions[i].write_back > first_ID):
                    sec_op = final_instructions[i].write_back
                    RAW = 'Y'
                    break

            second_ID = sec_op

        for i in range(index-1, 0, -1):

            cache_index_loop = i % length

            prev_operation = inst.instructions[cache_index_loop].operation
            prev_op1 = inst.instructions[cache_index_loop].operand1
            if (((current_operation not in ('BNE','BEQ')) or (prev_operation not in ('BNE','BEQ'))) and (prev_op1 == current_operand1) and (final_instructions[i].write_back > first_ID)):
                third_ID = final_instructions[i].write_back
                WAW = 'Y'

        first_max = max(first_ID, second_ID)
        ID = max(first_max,third_ID)


    else:
        ID = first_ID




def execute(index):

    global EX, Struct, IsCompleted, hasBranchInstruction, dataCacheHits, dataCacheRequests,ID, fromExecute
    first_EX = 0
    second_EX = 0
    dCache_Index = (index % length)
    current_op = inst.instructions[dCache_Index].operation
    isFirst = True
    isDouble = False
    isCacheMiss = False
    isStrucHaz = False

    if (inst.instructions[dCache_Index].operation == 'HLT'):
        EX = 0
        return


        EX = 0
        return

    if(current_op in ('LW','LD','L.D','S.D','SW','SD')):
        if(current_op in ('LW','SW')):
            isDouble = False
            first_EX = 0
            dataCacheRequests += 1

        elif(current_op in ('LD','L.D','SD','S.D')):
            #print("Inside 1")
            isDouble = True
            first_EX = 1
            dataCacheRequests += 2


        if(index == 0):
            isFirst = 0

            #print("Inside 2")
        else:
            isFirst = 1


        if(dataCache.isDataCacheMiss(inst.instructions[dCache_Index].operand2,inst.instructions[dCache_Index].displacement,isFirst,isDouble)):
            print("Inside 3")
            isCacheMiss = True
            second_EX = dataCachePenalty   
            if(current_op in ('SW','SD','S.D')):
                second_EX += 1
        else:
            print("Inside 4")
            if(current_op in ('LW','SW')):
                dataCacheHits += 1
            else:
                dataCacheHits += 2
            second_EX = configuration.dCache

        if(isStructuralHazard(index)):
           #print("Inside 5")
            EX = first_EX + second_EX + final_instructions[index-1].execute + 1 - 1
        else:
           #print("Inside 6")
            EX = first_EX + second_EX + ID + 1




    if (inst.instructions[dCache_Index].operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI','ADD.D','ADDD','SUBD','SUB.D','MUL.D','MULD','DIV.D','DIVD')):

        if (inst.instructions[dCache_Index].operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):

            op1 = int((inst.instructions[dCache_Index].operand1)[1:])
            op2 = int((inst.instructions[dCache_Index].operand2)[1:])

            if(inst.instructions[dCache_Index].operation == 'DADD'):
                op3 = int((inst.instructions[dCache_Index].operand3)[1:])
                reg.R[op1] = reg.R[op2] + reg.R[op3]
            elif(inst.instructions[dCache_Index].operation == 'DSUB'):
                op3 = int((inst.instructions[dCache_Index].operand3)[1:])
                reg.R[op1] = reg.R[op2] - reg.R[op3]
            elif (inst.instructions[dCache_Index].operation == 'AND'):
                op3 = int((inst.instructions[index].operand3)[1:])
                reg.R[op1] = reg.R[op2] & reg.R[op3]
            elif (inst.instructions[dCache_Index].operation == 'OR'):
                op3 = int((inst.instructions[index].operand3)[1:])
                reg.R[op1] = reg.R[op2] | reg.R[op3]
            elif (inst.instructions[dCache_Index].operation == 'DADDI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] + op3
            elif (inst.instructions[dCache_Index].operation == 'DSUBI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] - op3
            elif (inst.instructions[dCache_Index].operation == 'ANDI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] & op3
            elif (inst.instructions[dCache_Index].operation == 'ORI'):
                op3 = int(inst.instructions[dCache_Index].operand3)
                reg.R[op1] = reg.R[op2] | op3


            if(inst.instructions[dCache_Index].operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI')):
                for i in range(index - 1, 0, -1):
                    cache_index_loop = i % length
                    prev_operation = inst.instructions[cache_index_loop].operation
                    prev_operation2 = inst.instructions[cache_index_loop-1].operation
                    if ((prev_operation in ('DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI','LD','LW','L.D','SD','S.D')) and ((final_instructions[i].execute>=(ID+2)) and ((ID+2)>=(final_instructions[i].decode+1)))):

                        Struct = 'Y'
                        EX = final_instructions[i].execute + 1
                        break
                    else:
                        EX = ID + 2





        elif(inst.instructions[dCache_Index].operation in ('ADD.D','ADDD','SUBD','SUB.D')):
            print("1")
            for i in range(index-1, 0, -1):
                cache_index_loop = i % length
                prev_operation = inst.instructions[cache_index_loop].operation


                if ((prev_operation in Double_Add_Sub_StructureHazard) and final_instructions[i].execute > (ID+1) and configuration.isAdderPipelined == False):

                    EX = final_instructions[i].execute + configuration.adder
                    break
                else:

                    EX = ID + configuration.adder
        elif(inst.instructions[dCache_Index].operation in ('MUL.D','MULD')):

            for i in range(index-1, 0, -1):
                cache_index_loop = i % length
                prev_operation = inst.instructions[cache_index_loop].operation
                if (prev_operation in ('MULD','MUL.D') and final_instructions[i].execute > (ID+1) and configuration.isMultiplierPipelined == False):
                    EX = final_instructions[i].execute + configuration.multiplier
                    break
                else:
                    EX = ID + configuration.multiplier

        elif(inst.instructions[dCache_Index].operation in ('DIV.D','DIVD')):
            for i in range(index-1, 0, -1):
                cache_index_loop = i % length
                prev_operation = inst.instructions[cache_index_loop].operation
                if (prev_operation in ('DIVD','DIV.D') and final_instructions[i].execute > (ID+1) and configuration.isDividerPipelined == False):
                    EX = final_instructions[i].execute + configuration.divider
                    break
                else:
                    EX = ID + configuration.divider

    if (current_op in ('BNE', 'BEQ')):
        hasBranchInstruction = True
        EX = 0
        if (current_op == 'BNE'):
            oper1_index = int((inst.instructions[dCache_Index].operand1)[1:])
            oper2_index = int((inst.instructions[dCache_Index].operand2)[1:])

            if (reg.R[oper1_index] != reg.R[oper2_index]):
                IsCompleted = False
            else:
                IsCompleted = True

        elif (current_op == 'BEQ'):
            oper1_index = int((inst.instructions[dCache_Index].operand1)[1:])
            oper2_index = int((inst.instructions[dCache_Index].operand2)[1:])

            if (reg.R[oper1_index] == reg.R[oper2_index]):
                IsCompleted = False
            else:
                IsCompleted = True


def write_back(index):
    global WB
    global EX,Struct, fromWriteBack
    cache_index = (index % length)
    current_op = inst.instructions[cache_index].operation

    if (inst.instructions[cache_index].operation == 'HLT'):
        WB = 0
        return

    if (current_op in ('BNE','BEQ')):
        WB = 0
        return

    WB = EX + 1

    for i in range(index-1,0,-1):
        if((WB == final_instructions[i].write_back)):
            EX = EX + 1
            WB = WB + 1
            Struct = 'Y'
            fromWriteBack = True








def isStructuralHazard(index):
    global Struct
    cache_index = (index % length) - 1
    current_operation = inst.instructions[cache_index].operation
    Struct = 'N'


    if ((index != 0) and (((ID + 2) >= (final_instructions[index - 1].decode + 2)) and ((ID + 2) <= (final_instructions[index - 1].execute)))):
        Struct = 'Y'
        return True



    '''if(current_operation in Load_StrutcureHazard):
        for i in range(index-1,0,-1):
            prev_operation = inst.instructions[i].operation
            if (prev_operation in Load_StructureHazard and final_instructions[i].write_back > first_IF):
                return True
        return False'''





def run_Instructions():
    global Struct, WAW, RAW, WAR, index
    total_halts = 0

    for instr in inst.instructions_string:


        index_of_current_instruction = index

        fetch(index_of_current_instruction)
        #print(final_instructions[index_of_current_instruction].IF)
        decode(index_of_current_instruction)
        execute(index_of_current_instruction)
        write_back(index_of_current_instruction)

        #print(index_of_current_instruction)
        final_instructions.append(final_instruction(IF, ID, EX, WB, RAW, WAR, WAW, Struct))
        Struct = 'N'
        WAW = 'N'
        WAR = 'N'
        RAW = 'N'
        print(instr.rstrip('\n'),"\t",final_instructions[index_of_current_instruction].fetch,"\t",final_instructions[index_of_current_instruction].decode,"\t",final_instructions[index_of_current_instruction].execute,"\t",final_instructions[index_of_current_instruction].write_back,"\t",final_instructions[index_of_current_instruction].raw,"\t",final_instructions[index_of_current_instruction].war,"\t",final_instructions[index_of_current_instruction].waw,"\t",final_instructions[index_of_current_instruction].struct_hazard)

        write_file.write(instr.rstrip('\n') + "\t" + str(final_instructions[index_of_current_instruction].fetch)  + "\t" + str(final_instructions[index_of_current_instruction].decode) + "\t" + str(final_instructions[index_of_current_instruction].execute) + "\t" + str(final_instructions[index_of_current_instruction].write_back) + "\t" + final_instructions[index_of_current_instruction].raw + "\t" + final_instructions[index_of_current_instruction].war + "\t" + final_instructions[index_of_current_instruction].waw + "\t" + final_instructions[index_of_current_instruction].struct_hazard + "\n")

        index = index + 1



while True:
    if (IsCompleted):
        break
    else:
        run_Instructions()
        if(not hasBranchInstruction):
            break
        loop_number = loop_number + 1

print("Total number of access requests for instruction cache: "+str(instructCacheRequests)+'\n')
print("Number of instruction cache hits: "+str(instructCacheHits)+'\n')
print("Total number of access requests for data cache: "+str(dataCacheRequests)+'\n')
print("Number of data cache hits: "+str(dataCache.dcache_hits)+'\n')


write_file.write("Total number of access requests for instruction cache: "+str(instructCacheRequests)+'\n')
write_file.write("Number of instruction cache hits: "+str(instructCacheHits)+'\n')
write_file.write("Total number of access requests for data cache: "+str(dataCacheRequests)+'\n')
write_file.write("Number of data cache hits: "+str(dataCache.dcache_hits)+'\n')

write_file.close()