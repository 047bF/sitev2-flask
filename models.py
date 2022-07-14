from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class SizeHistories(db.Model):
    __tablename__ = 'size_histories'
    id = db.Column(db.Integer, primary_key=True)
    unique_unique_id = db.Column(db.Integer)
    avail_avail_id = db.Column(db.Integer)
    size_size_id = db.Column(db.Integer)
    size = relationship(
        'Sizes',
        primaryjoin="foreign(SizeHistories.size_size_id) == Sizes.size_id",
        lazy='select',
        uselist=True
    )

    def __repr__(self):
        return f"id : {self.id}, mod_uniq: {self.unique_unique_id}"

    def json(self):
        output = {"id": self.id,
                  "unique_unique": self.unique_unique_id,
                  "avail_avail": self.avail_avail_id,
                  "size": self.size_size_id
                  }
        return output


class Sizes(db.Model):
    __tablename__ = 'sizes'
    size_id = db.Column(db.Integer, primary_key=True)
    size_value = db.Column(db.String)
    size_label = db.Column(db.String)
    gen_gen_id = db.Column(db.Integer)
    from_universal_size = db.Column(db.Integer)
    to_universal_size = db.Column(db.Integer)

    def __repr__(self):
        return f"id : {self.size_id}"

    def json(self):
        output = {"id": self.size_id,
                  "size_value": self.size_value,
                  "size_label": self.size_label,
                  "gen_gen_id": self.gen_gen_id
                  }
        return output


class UniqueDetails(db.Model):
    __tablename__ = 'unique_details'

    unique_id = db.Column(db.Integer, primary_key=True)
    mod_site_uniq = db.Column(db.String(120))
    navi_date = db.Column(db.DateTime())
    insert_date = db.Column(db.DateTime())
    price = db.Column(db.Float)
    sale_price = db.Column(db.Float)
    is_collab = db.Column(db.Boolean())
    first_to_show = db.Column(db.Boolean())
    brand_name = db.Column(db.String(50))
    mod_name = db.Column(db.String(120))
    site_name = db.Column(db.String(50))
    site_link = db.Column(db.String(100))
    site_prelink = db.Column(db.String(30))
    site_postlink = db.Column(db.String(50))
    site_piclink = db.Column(db.String(100))
    picture_link = db.Column(db.String(255))
    picture_link_2 = db.Column(db.String(255))

    sizes = relationship(
        'SizeHistories',
        primaryjoin="UniqueDetails.unique_id == foreign(SizeHistories.unique_unique_id)",
        lazy='subquery',
        uselist=True
    )

    def __repr__(self):
        return f"id : {self.unique_id}, mod_uniq: {self.mod_site_uniq}"

    @hybrid_property
    def all_sizes(self):
        return [p.json() for p in self.sizes if p.avail_avail_id == 1]

    def json(self):
        output = {"unique_id": self.unique_id,
                  "link": self.site_prelink + self.mod_site_uniq,
                  "brand_name": self.brand_name,
                  "mod_name": self.mod_name,
                  "price": self.price,
                  "site_name": self.site_name,
                  "site_link": self.site_link,
                  "picture_link": self.site_piclink + self.picture_link,
                  "is_collab": self.is_collab,
                  "first_to_show": self.first_to_show,
                  "navi_date": str(self.navi_date),
                  "insert_date": str(self.insert_date),
                  "sizes": self.all_sizes
                  }
        if self.sale_price != 0:
            output["sale_price"] = self.sale_price
        if self.picture_link_2:
            output['picture_link_2'] = self.site_piclink + self.picture_link_2
        if self.site_name == 'SUPERSTEP' or self.site_name == 'BRANDSHOP':
            output["link"] = output['link'].replace("---", "/#").replace("--", "/")
        elif self.site_name == 'SVMOSCOW':
            output['link'] = output['link'].replace("---", "/").replace("--", "/")
        elif self.site_name == 'KITH EU' or self.site_name == 'KITH US':
            output['link'] += self.site_postlink[:-2]
            output['picture_link'] = output['picture_link'].replace('600x.jpg', '1000x.jpg')
        elif self.site_postlink:
            output['link'] += self.site_postlink

        return output


class PriceHistories(db.Model):
    __tablename__ = 'price_histories'
    id = db.Column(db.Integer, primary_key=True)
    unique_unique_id = db.Column(db.Integer)
    avail_avail_id = db.Column(db.Integer)
    navi_date = db.Column(db.DateTime())
    insert_date = db.Column(db.DateTime())
    number_history = db.Column(db.Integer)
    price = db.Column(db.Float)
    sale_price = db.Column(db.Float)
    val_val_id = db.Column(db.Integer)

    def __repr__(self):
        return f"id : {self.id}, mod_uniq: {self.unique_unique_id}"

    def json(self):
        output = {"unique_unique": self.unique_unique_id,
                  "number_history": self.number_history,
                  "avail_avail": self.avail_avail_id,
                  "price": self.price,
                  "val_val": self.val_val_id,
                  "navi_date": str(self.navi_date),
                  "insert_date": str(self.insert_date)
                  }
        if self.sale_price != 0:
            output["sale_price"] = self.sale_price
        return output


class AllSizesView(db.Model):
    __tablename__ = 'universal_sizes'

    universal_id = db.Column(db.Integer, primary_key=True)
    universal_size = db.Column(db.Integer)
    eu_size = db.Column(db.String(10))
    us_size = db.Column(db.String(10))
    uk_size = db.Column(db.String(10))
    ru_size = db.Column(db.String(10))
    gen_gen_id = db.Column(db.Integer)

    def __repr__(self):
        return f"id : {self.universal_id}, universal_size: {self.universal_size}"

    def json(self):
        output = {"universal_size": self.universal_size,
                  "eu_size": self.eu_size,
                  "us_size": self.us_size,
                  "uk_size": self.uk_size,
                  "ru_size": self.ru_size,
                  "gen_gen_id": self.gen_gen_id
                  }
        return output
