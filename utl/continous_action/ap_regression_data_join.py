import sys
import getopt
import math

class PredictDataJoiner_ap:

  def __init__(self, data_file_name, predict_file_name, min_val, max_val, zero_one_width):
    self.data_file_name = data_file_name
    self.predict_file_name = predict_file_name
    self.min_val = min_val
    self.max_val = max_val
    self.zero_one_width = zero_one_width

  def join(self):

    data_file = open(self.data_file_name,"r")
    predict_file = open(self.predict_file_name,"r")

    range_val = self.max_val - self.min_val
    zero_one_h = abs(range_val) * self.zero_one_width
    N = 0
    abs_loss_acc = 0.
    sqr_loss_acc = 0.
    zero_one_loss_acc = 0.
    abs_loss_max = float("-inf")
    sqr_loss_max = float("-inf")
    max_found = float("-inf")
    min_found = float("inf")
    for (data_line, predict_line) in zip(data_file, predict_file):
      # Get data
      act = self.get_action(predict_line)
      reg = self.get_regression_val(data_line)
      # Compute losses
      abss = abs((reg-act)/range_val)
      if (abss > abs_loss_max):
        abs_loss_max = abss
      abs_loss_acc += abss
      sqrr = ((reg-act)/range_val)**2
      if (sqrr > sqr_loss_max):
        sqr_loss_max = sqrr
      sqr_loss_acc += sqrr
      if(not math.isclose(act,reg,abs_tol=zero_one_h)):
        zero_one_loss_acc += 1.0
      N += 1
      if(N%10000 == 0):
        print('.',end='',flush=True)
      if(reg > max_found):
        max_found = reg
      if(reg < min_found):
        min_found = reg

    abs_loss = abs_loss_acc / float(N)
    sqr_loss = sqr_loss_acc / float(N)
    zero_one_loss = zero_one_loss_acc / float(N)

    print('.')
    print("abs_loss=",abs_loss,", abs_loss_acc=",abs_loss_acc,", N=",N,)
    print("sqr_loss=",sqr_loss,", sqr_loss_acc=",sqr_loss_acc,", N=",N,)
    print("zero_one_loss=",zero_one_loss,", zero_one_loss_acc=",zero_one_loss_acc,", N=",N,)
    print("abs_loss_MAX=",abs_loss_max,", sqr_loss_MAX=",sqr_loss_max,", N=",N,)
    print("zero_one_width=",zero_one_width)
    print("max_param=",self.max_val,",min_param=",self.min_val,"max_found=",max_found,"min_found=",min_found)
    if(not math.isclose(self.max_val,max_found,rel_tol=.001)):
      print("ERR:Please check max param. ", self.max_val, "is not close to ", max_found)
    if(not math.isclose(self.min_val,min_found,rel_tol=.001)):
      print("ERR:Please check min param. ", self.min_val, "is not close to ", min_found)

  def get_regression_val(self, data_line):
    separator_position = data_line.find('|')
    return float(data_line[:separator_position])

  def get_action(self, pred_line):
    separator_position = pred_line.find(':')
    #print(pred_line[:separator_position - 1 ])
    return float(pred_line[:separator_position])

if __name__ == "__main__":
  predict_file = "predict.txt"
  data_file = "data.txt"
  max_val = 100.0
  min_val = 0.0
  zero_one_width = 0.1

  # Parse options - get predict and data file names
  args = sys.argv[1:]
  opts, args = getopt.getopt(args, "p:d:m:i:z",["predict_file=", "data_file=", "max=", "min=", "zero_one="])
  for opt, arg in opts:
    if opt in ('-p', '--predict_file'):
      predict_file = arg
    elif opt in ('-d', '--data_file'):
      data_file = arg
    elif opt in ('-m', '--max'):
      max_val = float(arg)
    elif opt in ('-i', '--min'):
      min_val = float(arg)
    elif opt in ('-z', '--zero_one'):
      zero_one_width = float(arg)


  # Print join lines to stdout
  fileJoiner = PredictDataJoiner_ap(data_file, predict_file, min_val, max_val, zero_one_width)
  fileJoiner.join()