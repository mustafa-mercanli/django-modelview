

class DBRouter:

    def db_for_read(self,model,**hints):
        return getattr(model,"_db","default")
    
    def db_for_write(Self,model,**hints):
        return getattr(model,"_db","default")

    def allow_relation(self,a,b,**hints):
        return True
    
    def allow_migrate(self,a,b,**hints):
        return True

