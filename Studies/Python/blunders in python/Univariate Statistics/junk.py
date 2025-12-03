class junk():

    def __init__(self,tt):
        self.tt = tt
    
    def my_max(self,tt=None):
        if tt:
            return max(tt)
        else:
            return max(self.tt)
        

t1 = junk([1,2,3])
t2 = junk([1,2,3,6,8])
