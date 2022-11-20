import constants.scraperConstants as cons
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
                if(cons.purchaseAmount in content[cons.content]):
                    resultSet.append(f'({content[cons.occurrenceTimestamp]} {content[cons.author]} purchased superchat({content[cons.content][cons.purchaseAmount][cons.simpleText]}) with message:\n\t{content[cons.content][cons.message]}\n')
                elif(cons.membershipChat in content[cons.content]):
                    resultSet.append(f'({content[cons.occurrenceTimestamp]}) {content[cons.author]} : {content[cons.content][cons.membershipChat]}\n')
                elif(cons.membershipJoin in content[cons.content]):
                    resultSet.append(f'({content[cons.occurrenceTimestamp]}) ({content[cons.author]}) joined membership!\n')
                elif(cons.message in content[cons.content]):
                    resultSet.append(f'({content[cons.occurrenceTimestamp]}) {content[cons.author]} : {content[cons.content][cons.message]}\n')
            writer.writelines(resultSet)    
    
    def generateJsonDataset(self, dataset):
        dataset = json.dumps(dataset)
        filename = self.outputName+".json"
        with open(filename, 'w', encoding='utf-8') as jsonWriter:
            jsonWriter.write(dataset)

    def generateRaw(self, content):
        jsonContent = json.dumps(content)
        with open(self.outputName, 'w+', encoding='utf-8') as writer:
            writer.write(jsonContent)