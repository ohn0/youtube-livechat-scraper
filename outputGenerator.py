import constants as cons
class outputGenerator:
    outputName = ''
    def __init__(self):
        self.outputName = ''

    def generate(self, content, outputType):
        if outputType == cons.OUTPUT_JSON:
            self.generateJsonDataset(content)
        elif outputType == cons.OUTPUT_TEXT:
            self.generateCleanDataset(content);
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
                elif(cons.membershipJoin     in content[cons.content]):
                    resultSet.append(f'({content[cons.occurrenceTimestamp]}) ({content[cons.author]}) joined membership!\n')
                elif(cons.message in content[cons.content]):
                    resultSet.append(f'({content[cons.occurrenceTimestamp]}) {content[cons.author]} : {content[cons.content][cons.message]}\n')
            writer.writelines(resultSet)    
    
    def generateJsonDataset(self, dataset):
        filename = self.outputName+".json"
        with open(filename, 'w', encoding='utf-8') as jsonWriter:
            jsonWriter.write(dataset)