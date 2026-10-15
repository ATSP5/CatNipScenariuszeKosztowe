from ProjectFolders import ProjectFolders
from TableReader import TableReader
from DataScanner import DataScanner
from DemoCostData import DemoCostData
from PlnFormat import PlnFormat
from CostModelLoader import CostModelLoader
from ScenarioAdvisor import ScenarioAdvisor
from ScenarioEngine import ScenarioEngine
from ScenariuszeKosztowe import ScenariuszeKosztowe

def main():
	folders = ProjectFolders()
	reader = TableReader()
	scanner = DataScanner()
	generator = DemoCostData()
	formatter = PlnFormat()

	data_1 = folders.folders()
	data_2 = reader.reader()
	data_3 = scanner.scanner()
	data_4 = generator.generator()
	data_5 = formatter.formatter()
	model = CostModelLoader(data_1, data_2, data_4, data_3)
	data_6 = model.model()
	advisor = ScenarioAdvisor(data_5)
	data_7 = advisor.advisor()
	engine = ScenarioEngine(data_6)
	data_8 = engine.engine()
	result = ScenariuszeKosztowe(data_8, data_7, data_5)
	result.show()
	pass

if __name__ == "__main__":
	main()
