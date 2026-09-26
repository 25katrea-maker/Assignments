import sys
from abc import ABC,abstractmethod
from typing import Dict,Type

class PaymentMethod(ABC):
  @abstractmethod
  def getDetails(self)->str:
    pass
  @abstractmethod
  def pay(self,amount:float)->bool:
    pass
  
class RazorpayCardPayment(PaymentMethod):
  def __init__(self,cardNumber:str,cardHolder:str,expiryDate:str):
    self.card_number=cardNumber
    self.card_holder=cardHolder
    self.expiry_date=expiryDate
    
  def getDetails(self)->str:
    masked=f"****-****-****-{self.card_number[-4:]}" if len(self.card_number)>=4 else self.card_number
    return f"Razorpay Card[Holder:{self.card_holder},Number:{masked}]"
  
  def pay(self,amount:float)->bool:
    print(f"->Processing payment of {amount:.2f}Rs by Razorpay Card")
    return True
    
class RazorpayUPIPayment(PaymentMethod):
  def __init__(self,upi_id:str):
    self.upi_id=upi_id
  def getDetails(self)->str:
    return f"Razorpay UPI [ID:{self.upi_id}]"
  def pay(self,amount:float)->bool:
    print(f"->Processing payment of {amount:.2f}Rs by Razorpay UPI")
    return True
  
class StripeCardPayment(PaymentMethod):
  def __init__(self,cardNumber:str,cardHolder:str,expiryDate:str):
    self.card_number=cardNumber
    self.card_holder=cardHolder
    self.expiry_date=expiryDate
    
  def getDetails(self)->str:
    masked=f"******-******-******-{self.card_number[-4:]}" if len(self.card_number)>=4 else self.card_number
    return f"Stripe Card[Holder:{self.card_holder},Number:{masked}]"
  def pay(self,amount:float)->bool:
      print(f"->Processing payment of {amount:.2f}Rs by Stripe Card")
      return True
    
class StripeUPIPayment(PaymentMethod):
  def __init__(self,upiId:str):
    self.upi_id=upiId
  def getDetails(self)->str:
      return f"Stripe UPI [ID:{self.upi_id}]"
  def pay(self,amount:float)->bool:
    print(f"->Processing payment of {amount:.2f}Rs by Stripe UPI")
    return True
  
class FactoryPaymentMethod(ABC):
  factory:Dict[str,Type[PaymentMethod]]={}
  
  @classmethod
  def getPaymentObject(cls,methodType:str,**kwargs)->PaymentMethod:
    methodType=methodType.lower().strip()
    if methodType in cls.factory:
      return cls.factory[methodType](**kwargs)
    raise ValueError(f"Ypur Payment method choice is Unsupported:'{methodType}'")

class RazorpayFactory(FactoryPaymentMethod):
  factory={
    "card":RazorpayCardPayment,
    "upi":RazorpayUPIPayment
  }
  
class StripeFactory(FactoryPaymentMethod):
  factory={
    "card":StripeCardPayment,
    "upi":StripeUPIPayment
  }
  
class Aggregator(ABC):
  def __init__(self,name:str,processingFee:float,factoryClass:Type[FactoryPaymentMethod]):
    self.name=name
    self.processingFee=processingFee
    self.factoryClass=factoryClass
    
  def callGetPaymentObject(self,methodType:str,amount:float,**kwargs)->bool:
    fee=amount*(self.processingFee/100)
    totalAmount=amount+fee
    print(f"\n[{self.name}Aggregator Summary]")
    print(f"Base Amount: Rs{amount:.2f}|Processing Fee({self.processingFee}%):{fee:.2f}")
    print(f"Total Amount Payable:{totalAmount:.2f}")
    
    paymentObj=self.factoryClass.getPaymentObject(methodType,**kwargs)
    print(f"Method details:{paymentObj.getDetails()}")
    return paymentObj.pay(totalAmount)
  
class RazorpayAggregator(Aggregator):
  def __init__(self):
    super().__init__(name="Razorpay",processingFee=2.0,factoryClass=RazorpayFactory)

class StripeAggregator(Aggregator):
  def __init__(self):
    super().__init__(name="Stripe",processingFee=2.9,factoryClass=StripeFactory)
 
class AggregatorFactory:
  factory:Dict[str,Type[Aggregator]]={
    "stripe":StripeAggregator,
    "razorpay":RazorpayAggregator
  }   
  
  @classmethod
  def getAggregatorObject(cls,aggregatorName:str)->Aggregator:
    aggregatorName=aggregatorName.lower().strip()
    if aggregatorName in cls.factory:
      return cls.factory[aggregatorName]()
    raise ValueError(f"The entered agggregator's name is Unsupported:'{aggregatorName}'")
  
def main():
  print("******")
  print(" PAYMENT PROCESSING SYSTEM ")
  print("******")
  
  aggInput=input("Please select the Aggregator (stripe/razorpay):").strip()
  try:
    aggregator=AggregatorFactory.getAggregatorObject(aggInput)
  except ValueError as e:
    print(f"Error:{e}")
    return
    
    
  methodInput=input('Please select a method(card/upi): ').strip().lower()
  
  kwargs={}
  if methodInput=="card":
   kwargs["card_number"]=input("Enter the card number:")
   kwargs["card_holder"]=input("Enter the card holder's name:")
   kwargs["expiry_date"]=input("Enter the expiry date(MM):") 
  elif methodInput=="upi":
    kwargs["upi_id"]=input("Enter the UPI ID: ")
  else:
    print("Error:Invalid payment method selected")
    sys.exit(1)
    
  try:
    amount=float(input("Please enter amount to be paid:"))
    if amount<=0:
      print("Error:Sorry,Amount must be greater than 0")
      return
  except ValueError:
    print("Error:Please enter a valid numerical amount")
    return
  

  try:
    success=aggregator.callGetPaymentObject(methodInput,amount,**kwargs)
    if success:
      print("\n Transaction Status:SUCCESS \n")
    else:
      print("\n Transaction Status:FAILED  \n")
  except Exception as e:
    print(f"An unexpected error occured:{e}")
  
  
if __name__=="__main__":
  main()