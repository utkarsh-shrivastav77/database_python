from sqlalchemy import Column, String, Integer, create_engine,select,func
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine('mysql+mysqlconnector://root:MyPassword@localhost:3306/red30', echo=True)

mapper_registry = registry()
Base = mapper_registry.generate_base()

class sales(Base):
    __tablename__ = 'sales'
    order_num = Column(Integer, primary_key=True)
    order_type = Column(String(length = 20))
    customer_name = Column(String(length = 255))
    product_category = Column(String(length = 50))
    product_num = Column(Integer)
    product_name = Column(String(length = 100))
    quantity = Column(Integer)
    price = Column(Integer)
    discount = Column(Integer)
    order_total = Column(Integer)

    def __repr__(self):
        return "<Sales(order_num = '{0}', order_type = '{1}', customer_name = '{2}', product_category = '{3}', product_num = '{4}', product_name = '{5}', quantity = '{6}', price = '{7}', discount ='{8}', order_total = '{9}')>".format(self.order_num, self.order_type, self, self.customer_name, self.product_category, self, self.product_num, self.product_name, self.quantity, self, self.price, self, self.discount, self.order_total)

Base.metadata.create_all(engine)

with Session(engine) as session:
    max_query = select(func.max(sales.order_total))
    max_order = session.execute(max_query).scalar()
    # Here the saclar is used to retrieve the single value from the given results
    print(max_order)




