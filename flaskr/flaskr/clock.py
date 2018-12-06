from time import localtime


class Clock(object):
  def __init__(self):
    if  localtime()[6] == 0:
      self.day = "Monday"
    elif  localtime()[6] == 1:
      self.day = "Tuesday"
    elif  localtime()[6] == 2:
      self.day = "Wednesday"
    elif  localtime()[6] == 3:
      self.day = "Thursday"
    elif  localtime()[6] == 4:
      self.day = "Friday"
    elif  localtime()[6] == 5:
      self.day = "Satuday"
    elif  localtime()[6] == 6:
      self.day = "Sunday"
    else:
      pass
    self.hour =  localtime()[3]-7
    self.minute =  localtime()[4]
  def refresh(self):
    if  localtime()[6] == 0:
      self.day = "Monday"
    elif  localtime()[6] == 1:
      self.day = "Tuesday"
    elif  localtime()[6] == 2:
      self.day = "Wednesday"
    elif  localtime()[6] == 3:
      self.day = "Thursday"
    elif  localtime()[6] == 4:
      self.day = "Friday"
    elif  localtime()[6] == 5:
      self.day = "Satuday"
    elif  localtime()[6] == 6:
      self.day = "Sunday"
    else:
      pass
    self.hour =  localtime()[3]-7
    self.minute =  localtime()[4]
  def classtime(self):
    if self.minute <= 49 and self.hour != 12:
      return True
    else:
      return False

    
  def schoolday(self):
    if not self.day == "Sunday" and not self.day == "Saturday" and self.hour < 19 and self.hour > 8:
      return True
    else:
      return False
  def update(self):
    while True:
      self.refresh()
      if self.schoolday():
        if self.classtime():

	  return 'classtime'
         
        else:
	  return 'passing'

          
  

