'''
1)  A report describes your compiler.  It consists of two parts
	1.1   a scanner, how you scan the source and separate characters into token
		I separate characters by tokenizing from space and newline character, newline character represent new line rules in the grammar. While space used to separate each atomic value in the code.
	1.2   a parser, how you check the sequence of token that it is correct according to the grammar.  
		I used DFS algorithm to find the correct grammar, if any grammar matches the line, it'll add the answer to trans list. But if there is no matching rules, it will return empty list and catch as invalid line. The program will print out the incorrect line.
2)  Your pseudo code of the compiler
	No, it's a actual code in python 3.6. I wish I could get my extra point on this work.
'''

import sys
import traceback
word_dict = {
	'line': 10, \
	'id': 11, \
	'const': 12, \
	'IF': 13,\
	'GOTO': 14, \
	'PRINT': 15, \
	'STOP': 16, \
	'+': 1, \
	'-': 2, \
	'<': 3, \
	'=': 4 
}

G = {
	'stmt': ['asgmt', 'if', 'print', 'goto', 'stop'], \
	'asgmt': ['id = exp'], \
	'exp': ['term + term', 'term - term', 'term'], \
	'term' : ['id', 'const'], \
	'if': ['IF cond line_num'], \
	'cond': ['term < term', 'term = term'], \
	'print': ['PRINT id'], \
	'goto': ['GOTO line_num'], \
	'stop': ['STOP']
}

TERM_WORD = ['IF', 'PRINT', 'STOP']

fin = True

def dfs(now, line, wtype):
	#print(now, line, wtype)
	ret = []
	for k in range(len(G[wtype])):
		pos = G[wtype][k]
		spl = pos.split()
		i = 0
		while i < len(spl) and now + i < len(line):
					
			# If terminal with WORD
			if spl[i] in TERM_WORD and line[now+i] in TERM_WORD:
				ret.append((word_dict[line[now+i]], 0))
			elif spl[i] == 'GOTO' and line[now+i] == 'GOTO' and now+i+1 < len(line) and getType(line[now+i+1]) in ['const', 'line_num']:
				ret.append((word_dict[spl[i]], int(line[now+i+1])))
				i += 1
			elif spl[i] == 'line_num' and now+i+1 < len(line) and getType(line[now+i+1]) in ['const', 'line_num']:
				ret.append((word_dict['GOTO'], int(line[now+i+1])))	
			elif getType(line[now+i]) == spl[i]:
				if spl[i] == 'id':
					ret.append((word_dict[spl[i]], ord(line[now+i][0]) - ord('A') + 1))
				elif spl[i] == 'const':
					ret.append((word_dict[spl[i]], int(line[now+i])))
			elif getType(line[now+i]) == 'op':
				ret.append((17, word_dict[line[now+i]]))
				#now += 1			
			
			# If not terminal:
			elif spl[i] in G.keys():
				#print("Going to", spl[i])
				tmp = ret
				sth = dfs(now+i, line, spl[i])
				if (sth != []):
					ret = ret + sth
					#print("from", spl[i], ":", ret)
					now = now+i
				else:
					#print(line, spl[i], G[spl[i]], ret)
					ret = []

			else:
				#print("Not match", spl[i], "from", spl)
				ret = []
				break

			i += 1

		# print("ret size", i, "spl", spl)
		# print(k, "th rules on", wtype)
		# if(k+1 < len(G[wtype])):
		# 	print(G[wtype])

		# print(ret, len(ret), i, len(spl), spl)

		# If found matched rule
		if i == len(spl) and ret != []:
			# print ("matched", spl)
			# if spl == ['if']:
			# 	ret[-1] = ()
			return ret
		else:
			ret = []		

	#if(len(ret) == 0):
		#print("Parsing error on", line)
	return ret

def parse(line):
	ans = dfs(1, line, 'stmt')
	if(len(ans) == 0 or (len(ans) != len(line) - 1) and line[1] != 'GOTO') or (len(ans) != 1 and line[1] == 'GOTO'):
		fin = False
		return None
	return ans

def getType(word):
	#print(word)
	if(type(word) != str):
		return None
	if(word.isdigit() and 0 <= int(word) <= 100):
		return 'const'
	elif(word.isdigit() and 1 <= int(word) <= 1000):
		return 'line_num'
	elif(len(word) == 1 and ord('A') <= ord(word[0]) <= ord('Z')):
		return 'id'
	elif(word == "+" or word == "-" or word == "<" or word == "="):
		return 'op'
	return None

trans = []

def scanner(lines):
	ct = 0
	for line in lines:
		ct += 1
		line_arr = line.strip().split()
		if(line_arr[0].isdigit() and (1 <= int(line_arr[0]) <= 1000) and len(line_arr) > 1):
			ans = parse(line_arr)
			if ans != None:
				trans.append([(10, int(line_arr[0]))] + ans)
				#print("Line", ct , ":", [(10, int(line_arr[0]))] + ans)
			else:
				print("Parsing Error: not match any rules on line", ct)
				break
		elif len(line_arr) <=1:
			print("Parsing Error: line should contain more than 1 expression at line", ct)
			break
		else:
			print("Parsing Error: line should start with line_num. At line", ct)
			break


def main():
	if(len(sys.argv) != 2):
		print("USAGE: python bint.py FILENAME")
		return
	try:
		file = open("./" + sys.argv[1], 'r')
		scanner(file.readlines())
		if(not fin):
			return
		for line in trans:
			for pair in line:
				if(len(pair) == 2):
					print(pair[0], pair[1], end=" ")
			print("")
	except Exception:
		traceback.print_exc()

main()