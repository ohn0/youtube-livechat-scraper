"""module for generating output given scraped contents, can be
text, json, or raw json(scraped content without any modifications)"""
import json
import uuid

import livechat_scraper.constants.scraper_constants as cons
class OutputGenerator:
    """class that handles converting scraped content to a specified 
    output type and generating the output file."""
    def __init__(self, file_name=None):
        if file_name is None:
            self.output_name = uuid.uuid4().hex
        self.output_name = file_name

    def generate(self, content, output_type):
        """public method to generate the output, given the scraped content."""
        if output_type == cons.OUTPUT_JSON:
            self.__generate_json_dataset(content)
        elif output_type == cons.OUTPUT_TEXT:
            self.__generate_clean_dataset(content)
        elif output_type == cons.OUTPUT_RAW:
            self.__generate_raw(content)
        else:
            print("unable to generate output, invalid output type")

    def __generate_clean_dataset(self, dataset):
        file_name = self.output_name+".txt"
        result_set = []
        with open(file_name, 'w', encoding='utf-8') as writer:
            for content in dataset:
                if cons.PURCHASE_AMOUNT in content[cons.CONTENT]:
                    result_set.append(f'({content[cons.OCCURENCE_TIMESTAMP]} {content[cons.AUTHOR]}\
                        purchased superchat({content[cons.CONTENT][cons.PURCHASE_AMOUNT][cons.SIMPLE_TEXT]})\
                        with message:\n\t{content[cons.CONTENT][cons.MESSAGE]}\n')
                elif cons.MEMBERSHIP_CHAT in content[cons.CONTENT]:
                    result_set.append(f'({content[cons.OCCURENCE_TIMESTAMP]}) \
                        {content[cons.AUTHOR]} : {content[cons.CONTENT][cons.MEMBERSHIP_CHAT]}\n')
                elif cons.MEMBERSHIP_JOIN in content[cons.CONTENT]:
                    result_set.append(f'({content[cons.OCCURENCE_TIMESTAMP]})\
                         ({content[cons.AUTHOR]}) joined membership!\n')
                elif cons.MESSAGE in content[cons.CONTENT]:
                    result_set.append(f'({content[cons.OCCURENCE_TIMESTAMP]})\
                        {content[cons.AUTHOR]} : {content[cons.CONTENT][cons.MESSAGE]}\n')
            writer.writelines(result_set)

    def __generate_json_dataset(self, dataset):
        dataset = json.dumps(dataset)
        file_name = self.output_name+".json"
        with open(file_name, 'w', encoding='utf-8') as json_writer:
            json_writer.write(dataset)

    def __generate_raw(self, content):
        json_content = json.dumps(content)
        with open(self.output_name+".txt", 'w+', encoding='utf-8') as writer:
            writer.write(json_content)
