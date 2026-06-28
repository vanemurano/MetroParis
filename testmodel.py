from model.model import Model

model=Model()
model.buildGraph()

print(model.getMinMaxWeight())