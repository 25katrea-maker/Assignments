def outPutDecorator(title):
  def decoratorWrapper(func):
    def wrapper(*args,**kwargs):
      result=func(*args,**kwargs)
      pos_arg=[str(arg) for arg in args]
      kw_arg=[f"{key}={val}" for key,val in kwargs.items()]
      inputStr=", ".join(pos_arg+kw_arg)
      
      print("########################")
      print(f'# {title}')
      print(f'# input:{inputStr}')
      print(f'# output:{result}')
      print("########################")
      
      return result
    return wrapper
  return decoratorWrapper

@outPutDecorator("Adding")
def add(a,b):
  return a+b


if __name__=="__main__":
  add(4,3)
