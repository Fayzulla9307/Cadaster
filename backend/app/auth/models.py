from app import db

class Roli(db.Model):
    __tablename__ = "Roli"
    
    id       = db.Column(db.Integer, nullable=False, primary_key = True)
    rol      = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Rol %r>' % (self.rol)

class Razresheniya(db.Model):
    __tablename__ = "Razresheniya"
    
    id       = db.Column(db.Integer, nullable=False, primary_key = True)
    id_roli  = db.Column(db.Integer, db.ForeignKey("Roli.id"))
    resurs   = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Razreshenie %r>' % (self.resurs)

class Polzovateli(db.Model):
    __tablename__ = "Polzovateli"
    id       = db.Column(db.Integer, nullable=False, primary_key = True)
    imya     = db.Column(db.String(100), nullable=False)
    parol    = db.Column(db.String(192), nullable=False)
    sol      = db.Column(db.String(100), nullable=False)
    rol_id   = db.Column(db.Integer, db.ForeignKey("Roli.id"))
    opisanie = db.Column(db.String(1000), nullable=True)
    rol      = db.relationship("Roli", foreign_keys=[rol_id])

    def __repr__(self):
        return '<Polzovatel %r>' % (self.imya)
