#!user/bin/env  python
# kiki 2018/10/10
# python littleTest.py
import torch
import torch.nn.functional as F

if __name__ == "__main__":
	x = torch.zeros(2,1,2)
	print x
	y = torch.squeeze(x)
	print y
	print x
	x0 = torch.zeros(5)
	#y0 = torch.squeeze(x0,1)
	print x0
	#print y0

	x1 = torch.linspace(-2,2,5)
	print x1
	y1 = torch.unsqueeze(x1,-2)
	print "-2:",y1
	print "-1:",torch.unsqueeze(x1,-1)
	print "0:",torch.unsqueeze(x1,0)
	print "1:",torch.unsqueeze(x1,1)
