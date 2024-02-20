from sqlalchemy import Column, String, Integer, create_engine, ForeignKey,select
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine('mysql+mysqlconnector://root:MyPassword@localhost:3306/projects', echo = True)


#In SQLAlchemy, metadata refers to an object that stores information about database tables, columns, and other structural elements of a database. It acts as a catalog of database objects and their properties, allowing SQLAlchemy to interact with databases effectively.
mapper_registry = registry()
#mapper_registry.metadata

Base = mapper_registry.generate_base()
# What is Base? In SQLAlchemy ORM (Object-Relational Mapping), the "Base" typically refers to the base class from which all mapped classes in your application inherit. It's a central component of SQLAlchemy ORM that provides a foundation for defining database models and interacting with the database.

class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    description = Column(String(length=50))

    def __repr__(self):
        return "<Project(title ='{0},description ='{1}')>".format(self.title, self)

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    description = Column(String(length=50))
    # Here we describe the tasks table is related to the projects table
    project = relationship("Project")

    def __repr__(self):
        return "<Task(description= '{0}')>".format(self.description)


Base.metadata.create_all(engine)

with Session(engine) as session:
    Organize_closet = Project(title='Organize closet', description='Organize closet by color and style')
    session.add(Organize_closet)
    session.flush()
    # In many object-relational mapping (ORM) frameworks, like SQLAlchemy in Python, session.flush() is used to synchronize in-memory changes with the database without committing a transaction. This means that any pending inserts, updates, or deletes are sent to the database, but the transaction is not committed yet. This can be useful when you want to ensure that changes are visible to other parts of your application or when you need to generate primary key values for newly inserted objects.
    tasks = [
        Task(project_id=Organize_closet.project_id,description='Decide what clothes you have to donate'),
        Task(project_id=Organize_closet.project_id,description='Organize summer clothes'),
        Task(project_id=Organize_closet.project_id,description='Organize winter clothes')
    ]
    session.bulk_save_objects(tasks)
    session.commit()

with Session(engine) as session:
    smt = select(Project).where(Project.title == 'Organize closet')
    results = session.execute(smt)
    Organize_closet = results.scalar()
    # The above command return the first column of the first row from a result set.

    smt  = select(Task).where(Task.project_id == Organize_closet.project_id)
    results = session.execute(smt)
    for task in results:
        print(task)



