import parser


I_Cache = [[parser.instructions for x in range(4)] for y in range(4)]
total_instructions = len(parser.instructions_out)
# [[object1,object2,object3,object4],[object3,object4],[]]


def isInstructionCacheMiss(instruction, word_address):
    for row in I_Cache:
        for instruc in row:
            if instruction == instruc:
                #print("Instruction found!!!!!")
                return False
    implement_directMapCache(instruction, word_address)
    return True



def implement_directMapCache(instruction, word_address):
    global  I_Cache
    cache_block_address = (int(word_address / 4))%4
    wordAddress_In_blockAddress = 0
    current_index = word_address

    for i in range(0,4):

        if (current_index >= total_instructions):
            break


        current_instruction = inst.instructions[current_index]

        I_Cache[cache_block_address][wordAddress_In_blockAddress] = current_instruction
        current_index = current_index + 1
        wordAddress_In_blockAddress = wordAddress_In_blockAddress + 1



'''isInstructionCacheMiss(inst.instructions[0],0)
isInstructionCacheMiss(inst.instructions[1],1)
isInstructionCacheMiss(inst.instructions[2],2)
isInstructionCacheMiss(inst.instructions[3],3)
isInstructionCacheMiss(inst.instructions[4],4)
#isInstructionCacheMiss(inst.instructions[5],5)'''

'''print(inst.instructions[0].operation)
print(inst.instructions[1].operation)
print(inst.instructions[2].operation)
print(inst.instructions[3].operation)
print(inst.instructions[4].operation)
print(inst.instructions[5].operation)'''


'''
print(I_Cache[0][0].operation)
#print(I_Cache[0][0].operand1)
#print(I_Cache[0][0].operand2)

print(I_Cache[0][1].operation)
#print(I_Cache[0][1].operand1)
#print(I_Cache[0][1].operand2)

print(I_Cache[0][2].operation)
#print(I_Cache[0][2].operand1)
#print(I_Cache[0][2].operand2)

print(I_Cache[0][3].operation)
#print(I_Cache[0][3].operand1)
#print(I_Cache[0][3].operand2)

print(I_Cache[1][0].operation)
#print(I_Cache[1][0].operand1)
#print(I_Cache[1][0].operand2)

print(I_Cache[1][1].operation)
#print(I_Cache[1][1].operand1)
#print(I_Cache[1][1].operand2)

print(I_Cache[1][2].operation)
#print(I_Cache[1][2].operand1)
#print(I_Cache[1][2].operand2)

print(I_Cache[1][3].operation)
#print(I_Cache[1][3].operand1)
#print(I_Cache[1][3].operand2)
'''