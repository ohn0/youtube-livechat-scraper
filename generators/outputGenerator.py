import constants.scraper_constants as cons
import json
import uuid
class outputGenerator:
    outputName = ''
    def __init__(self, fileName=None):
        if(fileName == None):
            self.outputName = uuid.uuid4().hex
        self.outputName = fileName

    def generate(self, content, outputType):
        if outputType == cons.OUTPUT_JSON:
            self.generateJsonDataset(content)
        elif outputType == cons.OUTPUT_TEXT:
            self.generateCleanDataset(content);
        elif outputType == cons.OUTPUT_RAW:
            self.generateRaw(content)
        else:
            print("unable to generate output, invalid outputType")

    def generateCleanDataset(self, dataset):
        filename = self.outputName+".txt"
        resultSet = []
        with open(filename, 'w', encoding='utf-8') as writer:
            for content in dataset:
                if(cons.PURCHASE_AMOUNT in content[cons.CONTENT]):
                    resultSet.append(f'({content[cons.OCCURENCE_TIMESTAMP]} {content[cons.AUTHOR]} purchased superchat({content[cons.CONTENT][cons.PURCHASE_AMOUNT][cons.SIMPLE_TEXT]}) with message:\n\t{content[cons.CONTENT][cons.MESSAGE]}\n')
                elif(cons.MEMBERSHIP_CHAT in content[cons.CONTENT]):
                    resultSet.append(f'({content[cons.OCCURENCE_TIMESTAMP]}) {content[cons.AUTHOR]} : {content[cons.CONTENT][cons.MEMBERSHIP_CHAT]}\n')
                elif(cons.MEMBERSHIP_JOIN in content[cons.CONTENT]):
                    resultSet.append(f'({content[cons.OCCURENCE_TIMESTAMP]}) ({content[cons.AUTHOR]}) joined membership!\n')
                elif(cons.MESSAGE in content[cons.CONTENT]):
                    resultSet.append(f'({content[cons.OCCURENCE_TIMESTAMP]}) {content[cons.AUTHOR]} : {content[cons.CONTENT][cons.MESSAGE]}\n')
            writer.writelines(resultSet)    
    
    def generateJsonDataset(self, dataset):
        dataset = json.dumps(dataset)
        filename = self.outputName+".json"
        with open(filename, 'w', encoding='utf-8') as jsonWriter:
            jsonWriter.write(dataset)

    def generateRaw(self, content):
        jsonContent = json.dumps(content)
        with open(self.outputName+".txt", 'w+', encoding='utf-8') as writer:
            writer.write(jsonContent)