class iterate():
    def init(self):
        self.length=1

    def iterated(self, n):
        if n==1:
            return self.length
        elif n%2==0:
            self.length+=1
            return self.iterated(n/2)
        elif n!=1:
            self.length+=1
            return self.iterated(3*n+1)


iterate()