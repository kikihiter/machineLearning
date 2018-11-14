#! user/bin/env python
# kiki 2018/10/11 python2.7
# python 04_saveload.py

'''
someting about 'save' and 'load' of nn
only 'save'
'''

import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch.autograd import Variable

class Net(torch.nn.Module):
	def __init__(self,n_input,n_hidden,n_output):
		super(Net,self).__init__()
		self.hidden = torch.nn.Linear(n_input,n_hidden)
		self.predict = torch.nn.Linear(n_hidden,n_output)

	def forward(self,x):
		x = F.relu(self.hidden(x))
		x = self.predict(x)
		return x


if __name__ == "__main__":
	x = torch.unsqueeze(torch.linspace(-1,1,100),1)
	y = x*x + 0.2*torch.rand(x.size())

	#print x,y
	x,y = Variable(x),Variable(y)

	net1 = Net(1,10,1)
	optimzer = torch.optim.SGD(net1.parameters(),0.5)
	loss_func = torch.nn.MSELoss()

	for t in range(100):
		prediction = net1(x)
		loss = loss_func(prediction,y)
		optimzer.zero_grad()
		loss.backward()
		optimzer.step()

	torch.save(net1,'huigui.pkl')


	#plt.cla()
	plt.scatter(x.data.numpy(),y.data.numpy())
	plt.plot(x.data.numpy(),prediction.data.numpy(),'r-',lw=5)
	plt.text(0.5,0,'Loss=%.4f' % loss.data[0],fontdict={'size':20,'color':'red'})
	#plt.pause(0.1)
	#plt.ioff()
	plt.show()