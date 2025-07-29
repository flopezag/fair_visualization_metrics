from json import load
from os.path import dirname, join
import re


class Data(object):
    def __init__(self, json_file='example.json'):
        root_path = dirname(dirname(__file__))
        filename = join(root_path, 'data', json_file)

        with open(file=filename, mode='r') as f:
            self.raw_data = load(f)
            
        # used as default data_name when drawing graphs
        self.response_id = self.raw_data['responses'][0]["id"]
        
        self.__pattern__ = re.compile(pattern=r"RDA-([FAIR]).+-.*", flags=0)
        
        self.fair_maturity_model_data = dict()
        self.fairness_classification_per_indicator = dict()
        self.FMMClassification_data = dict()
        self.FMMClassification_data_length = int()
        self.FMMClassification_data_maximum = dict()
        self.FMMClassification_data_minimum = dict()
        self.FMMClassification_data_sum = dict()
        self.FMMClassification_data_normalized = dict()
        self.FMMClassification_data_len = dict()
        self.FMMClassification_data_threshold = dict()
        self.FMMClassification_data_compliance_level = dict()

        self.get_mqa_data()
        self.get_meloda_data()
        self.get_rda_human_readable_mapping()
        self.get_fair_maturity_model()
        self.get_fdm_classification()
        self.get_fairness_classification_per_indicator()
        self.classification_data_maximum_minimum()
        self.classification_data_normalized()
        self.classification_data_threshold()
        self.classification_data_compliance_level()
    
    def get_mqa_data(self) -> None:
        mqa_scores = {}
        mqa_scores['Findability'] = {}
        mqa_scores['Findability']['MQAF1'] = 30.0
        mqa_scores['Findability']['MQAF2'] = 30.0
        mqa_scores['Findability']['MQAF3'] = 20.0
        mqa_scores['Findability']['MQAF4'] = 20.0 #100 total

        mqa_scores['Accessibility'] = {}
        mqa_scores['Accessibility']['MQAA1'] = 50.0
        mqa_scores['Accessibility']['MQAA2'] = 20.0
        mqa_scores['Accessibility']['MQAA3'] = 30.0 #100 total

        mqa_scores['Interoperability'] = {}
        mqa_scores['Interoperability']['MQAI1'] = 20.0
        mqa_scores['Interoperability']['MQAI2'] = 10.0
        mqa_scores['Interoperability']['MQAI3'] = 10.0
        mqa_scores['Interoperability']['MQAI4'] = 20.0
        mqa_scores['Interoperability']['MQAI5'] = 20.0
        mqa_scores['Interoperability']['MQAI6'] = 30.0 #110 total

        mqa_scores['Reusability'] = {}
        mqa_scores['Reusability']['MQAR1'] = 20.0
        mqa_scores['Reusability']['MQAR2'] = 10.0
        mqa_scores['Reusability']['MQAR3'] = 10.0
        mqa_scores['Reusability']['MQAR4'] = 5.0
        mqa_scores['Reusability']['MQAR5'] = 20.0
        mqa_scores['Reusability']['MQAR6'] = 10.0 #75 total
    
        mqa_scores['Contextuality'] = {}
        mqa_scores['Contextuality']['MQAC1'] = 5.0
        mqa_scores['Contextuality']['MQAC2'] = 6.0
        mqa_scores['Contextuality']['MQAC3'] = 7.0
        mqa_scores['Contextuality']['MQAC4'] = 8.0 #26 total
        
        max_score = {}
        max_score['Findability'] = 100
        max_score['Accessibility'] = 100
        max_score['Interoperability'] = 110
        max_score['Reusability'] = 75
        max_score['Contextuality'] = 26

        Total_MQA_Points = 0.0
        mqa_model_data = {}
        normalised_mqa_model_data = {}

        #Loop through each MQA category Findability, Accessibility, etc...
        for catagory in mqa_scores.keys():
            score_value = 0.0
            check_count = 0.0
            val = "No"
            #Loop through each question in each category
            for question in mqa_scores[catagory].keys():
                #Count number of questions asked
                check_count += 1.0
                #Get resonse to question
                val = self.raw_data['responses'][0][question]
                #Count number of positive "Yes" responses for each category
                if val == 'Yes':
                    score_value += mqa_scores[catagory][question]
            
            #Create normalised value for yes reponses
            #normnlised value = number of yes responses in category / number of questions asked in category
            #val = round((score_value/check_count),2)
            normalised_mqa_model_data[catagory] = score_value/max_score[catagory]

            # NOT USED AT THE MOMENT - USING ABSOLUTE VALUES
            #mqa_model_data[catagory] = score_value
            #Total_MQA_Points += score_value        

        self.mqa_model_data = normalised_mqa_model_data
    
    def get_meloda_data(self) -> None:
        
        meloda_scores = {}
        meloda_scores['MELODA1'] = {}
        meloda_scores['MELODA2'] = {}
        meloda_scores['MELODA3'] = {}
        meloda_scores['MELODA4'] = {}
        meloda_scores['MELODA5'] = {}
        meloda_scores['MELODA6'] = {}
        meloda_scores['MELODA7'] = {}
        meloda_scores['MELODA8'] = {}

        meloda_scores['MELODA1']['Private use'] = 1
        meloda_scores['MELODA1']['Non-commercial reuse'] = 3
        meloda_scores['MELODA1']['Commercial reuse or no restrictions'] = 6

        meloda_scores['MELODA2']['Web access or unique URL parameters to dataset'] = 1
        meloda_scores['MELODA2']['Web Access unique with parameters to single data'] = 3 
        meloda_scores['MELODA2']['API or query language'] = 6

        meloda_scores['MELODA3']['Closed standard reusable and open non reusable'] = 1
        meloda_scores['MELODA3']['Open standard reusable'] = 3
        meloda_scores['MELODA3']['Open standard, individual metadata'] = 6

        meloda_scores['MELODA4']['Own data model standardization'] = 1
        meloda_scores['MELODA4']['Own ad hoc data model standardization published (harmonization)'] = 3
        meloda_scores['MELODA4']['Local standardization'] = 6
        meloda_scores['MELODA4']['Global standardization'] = 10

        meloda_scores['MELODA5']['No geographic information'] = 1 
        meloda_scores['MELODA5']['Simple or complex text field'] = 3
        meloda_scores['MELODA5']['Coordinates or full geographical information'] = 6

        meloda_scores['MELODA6']['Longer than 1 month'] = 1
        meloda_scores['MELODA6']['Monthly. Updating period ranges from 1 month to 1 day'] = 3
        meloda_scores['MELODA6']['Daily. Updating period ranges from 1 day to 1 hour'] = 6
        meloda_scores['MELODA6']['Hour. Updating period ranges from 1 hour to 1 minute'] = 10 
        meloda_scores['MELODA6']['Seconds. Updating period is lower than 1 minute'] = 15

        meloda_scores['MELODA7']['No information about the reputation of the data source'] = 1
        meloda_scores['MELODA7']['Statistics or reports published on users opinions'] = 3
        meloda_scores['MELODA7']['Indicators or rankings on reputation of the data source'] = 6

        meloda_scores['MELODA8']['Communication / dissemination not systematic'] = 1
        meloda_scores['MELODA8']['Available resources on updates (i.e., RSS feed)'] = 3
        meloda_scores['MELODA8']['Proactive dissemination / push dissemination (information automatic and timely)'] = 6

        meloda_model = {
            'MELODA1': 'License of data set',
            'MELODA2': 'Access to data',
            'MELODA3': 'Technical standard',
            'MELODA4': 'Standardization',
            'MELODA5': 'Geolocation content',
            'MELODA6': 'Updating frequency',
            'MELODA7': 'Reputation',
            'MELODA8': 'Dissemination'
        }

        self.meloda_model_data = {}

        # Precompute max values for each meloda_model[key] for later use in normalisation of results
        max_values = {key: max(meloda_scores[key].values()) for key in meloda_model}

        # Iterate over keys in meloda_model
        for key in meloda_model:
            # Calculate the rounded normalised score for each category from the WFIP questionaire store it in meloda_model_data
            self.meloda_model_data[meloda_model[key]] = round(meloda_scores[key][self.raw_data['responses'][0][key]] / max_values[key], 2)

    def get_rda_human_readable_mapping(self) -> None:
        self.rda_mapping = {
            'RDA-F1-01M': "Metadata is identified by a persistent identifier",
            'RDA-F1-01D': "Data is identified by a persistent identifier",
            'RDA-F1-02M': "Metadata is identified by a globally unique identifier",
            'RDA-F1-02D': "Data is identified by a globally unique identifier",
            'RDA-F2-01M': "Rich metadata is provided to allow discovery",
            'RDA-F3-01M': "Metadata includes the identifier for the data",
            'RDA-F4-01M': "Metadata is offered in such a way that it can be harvested and indexed",
            "RDA-A1-01M": "Metadata contains information to enable the user to get access to the data",
            "RDA-A1-02M": "Metadata can be accessed manually (i.e. with human intervention)",
            "RDA-A1-02D": "Data can be accessed manually (i.e. with human intervention)",
            "RDA-A1-03M": "Metadata identifier resolves to a metadata record",
            "RDA-A1-03D": "Data identifier resolves to a digital object",
            "RDA-A1-04M": "Metadata is accessed through standardised protocol",
            "RDA-A1-04D": "Data is accessible through standardised protocol",
            "RDA-A1-05D": "Data can be accessed automatically (i.e. by a computer program)",
            "RDA-A1.1-01M": "Metadata is accessible through a free access protocol",
            "RDA-A1.1-01D": "Data is accessible through a free access protocol",
            "RDA-A1.2-01D": "Data is accessible through an access protocol that supports authentication and authorisation",
            "RDA-A2-01M": "Metadata is guaranteed to remain available after data is no longer available",
            "RDA-I1-01M": "Metadata uses knowledge representation expressed in standardised format",
            "RDA-I1-01D": "Data uses knowledge representation expressed in standardised format",
            "RDA-I1-02M": "Metadata uses machine-understandable knowledge representation",
            "RDA-I1-02D": "Data uses machine-understandable knowledge representation",
            "RDA-I2-01M": "Metadata uses FAIR-compliant vocabularies",
            "RDA-I2-01D": "Data uses FAIR-compliant vocabularies",
            "RDA-I3-01M": "Metadata includes references to other metadata",
            "RDA-I3-01D": "Data includes references to other data",
            "RDA-I3-02M": "Metadata includes references to other data",
            "RDA-I3-02D": "Data includes qualified references to other data",
            "RDA-I3-03M": "Metadata includes qualified references to other metadata",
            "RDA-I3-04M": "Metadata include qualified references to other data",
            "RDA-R1-01M": "Plurality of accurate and relevant attributes are provided to allow reuse",
            "RDA-R1.1-01M": "Metadata includes information about the licence under which the data can be reused",
            "RDA-R1.1-02M": "Metadata refers to a standard reuse licence",
            "RDA-R1.1-03M": "Metadata refers to a machine-understandable reuse licence",
            "RDA-R1.2-01M": "Metadata includes provenance information according to community-specific standards",
            "RDA-R1.2-02M": "Metadata includes provenance information according to a cross-community language",
            "RDA-R1.3-01M": "Metadata complies with a community standard",
            "RDA-R1.3-01D": "Data complies with a community standard",
            "RDA-R1.3-02M": "Metadata is expressed in compliance with a machine-understandable community standard",
            "RDA-R1.3-02D": "Data is expressed in compliance with a machine-understandable community standard"
        }


    def get_fair_maturity_model(self) -> None:
        fair_maturity_model = {
            'FDMFE1[SQ001]': 'RDA-F1-01M',
            'FDMFE1[SQ002]': 'RDA-F1-01D',
            'FDMFE1[SQ003]': 'RDA-F1-02M',
            'FDMFE1[SQ004]': 'RDA-F1-02D',
            'FDMFE1[SQ005]': 'RDA-F2-01M',
            'FDMFE1[SQ006]': 'RDA-F3-01M',
            'FDMFE1[SQ007]': 'RDA-F4-01M',
            'FDMAE1[SQ001]': 'RDA-A1-02M',
            'FDMAE1[SQ002]': 'RDA-A1-02D',
            'FDMAE1[SQ003]': 'RDA-A1-03M',
            'FDMAE1[SQ004]': 'RDA-A1-03D',
            'FDMAE1[SQ005]': 'RDA-A1-04M',
            'FDMAE1[SQ006]': 'RDA-A1-04D',
            'FDMAE1[SQ007]': 'RDA-A1.1-01M',
            'FDMAE1[SQ008]': 'RDA-A2-01M',
            'FDMAI1[SQ001]': 'RDA-A1-01M',
            'FDMAI1[SQ002]': 'RDA-A1.1-01D',
            'FDMAI1[SQ003]': 'RDA-A1-05D',
            'FDMAU1[SQ001]': 'RDA-A1.2-01D',
            'FDMRE1[SQ001]': 'RDA-R1-01M',
            'FDMRE1[SQ002]': 'RDA-R1.1-01M',
            'FDMRE1[SQ003]': 'RDA-R1.3-01M',
            'FDMRE1[SQ004]': 'RDA-R1.3-01D',
            'FDMRE1[SQ005]': 'RDA-R1.3-02M',
            'FDMRI1[SQ001]': 'RDA-R1.1-02M',
            'FDMRI1[SQ002]': 'RDA-R1.1-03M',
            'FDMRI1[SQ003]': 'RDA-R1.2-01M',
            'FDMRI1[SQ004]': 'RDA-R1.3-02D',
            'FDMRU1[SQ001]': 'RDA-R1.2-02M',
            'FDMII1[SQ001]': 'RDA-I1-01M',
            'FDMII1[SQ002]': 'RDA-I1-01D',
            'FDMII1[SQ003]': 'RDA-I1-02M',
            'FDMII1[SQ004]': 'RDA-I1-02D',
            'FDMII1[SQ005]': 'RDA-I2-01M',
            'FDMII1[SQ006]': 'RDA-I3-01M',
            'FDMII1[SQ007]': 'RDA-I3-03M',
            'FDMIU1[SQ001]': 'RDA-I2-01D',
            'FDMIU1[SQ002]': 'RDA-I3-01D',
            'FDMIU1[SQ003]': 'RDA-I3-02M',
            'FDMIU1[SQ004]': 'RDA-I3-02D',
            'FDMIU1[SQ005]': 'RDA-I3-04M'
        }

        self.fair_maturity_model_data = {fair_maturity_model[key]: int(self.raw_data['responses'][0][key])
                                         for key in fair_maturity_model.keys()}

    def get_fdm_classification(self) -> None:
        fmm_classification = {
            'Essential': [
                'RDA-F1-01M', 'RDA-F1-01D', 'RDA-F1-02M', 'RDA-F1-02D', 'RDA-F2-01M', 'RDA-F3-01M', 'RDA-F4-01M',
                'RDA-A1-02M', 'RDA-A1-02D', 'RDA-A1-03M', 'RDA-A1-03D', 'RDA-A1-04M', 'RDA-A1-04D', 'RDA-A1.1-01M',
                'RDA-A2-01M', 'RDA-R1-01M', 'RDA-R1.1-01M', 'RDA-R1.3-01M', 'RDA-R1.3-01D', 'RDA-R1.3-02M'
            ],
            'Important': [
                'RDA-A1-01M', 'RDA-A1-05D', 'RDA-A1.1-01D', 'RDA-I1-01M', 'RDA-I1-01D', 'RDA-I1-02M', 'RDA-I1-02D',
                'RDA-I2-01M', 'RDA-I3-01M', 'RDA-I3-03M', 'RDA-R1.1-02M', 'RDA-R1.1-03M', 'RDA-R1.2-01M',
                'RDA-R1.3-02D'
            ],
            'Useful': [
                'RDA-A1.2-01D', 'RDA-I2-01D', 'RDA-I3-01D', 'RDA-I3-02M', 'RDA-I3-02D', 'RDA-I3-04M', 'RDA-R1.2-02M'
            ]
        }

        self.FMMClassification_data = {
            'Essential': self.__classification_per_category__(classes=fmm_classification, category='Essential'),
            'Important': self.__classification_per_category__(classes=fmm_classification, category='Important'),
            'Useful': self.__classification_per_category__(classes=fmm_classification, category='Useful')
        }

        self.FMMClassification_data_length = {
            'Essential': self.__len_classification_per_category__(category='Essential'),
            'Important': self.__len_classification_per_category__(category='Important'),
            'Useful': self.__len_classification_per_category__(category='Useful')
        }

    def get_fairness_classification_per_indicator(self):
        self.fairness_classification_per_indicator = self.__classification_per_indicator__()

    def __classification_per_category__(self, classes: dict, category: str) -> dict:
        result = {
            'F': 'Findable',
            'A': 'Accessible',
            'I': 'Interoperable',
            'R': 'Reusable'
        }

        # Create the structure
        aux1 = {x: dict() for x in [result[x] for x in result]}
        aux2 = {key: self.fair_maturity_model_data[key] for key in classes[category]}

        for key, value in aux2.items():
            category = self.__pattern__.findall(key)

            if category is None:
                raise Exception(f"Sorry, key is not expected: {key}")

            aux1[result[category[0]]][key] = value

        return aux1

    def __len_classification_per_category__(self, category: str) -> int:
        value = sum([len(self.FMMClassification_data[category][x]) for x in self.FMMClassification_data[category]])
        return value

    def __classification_per_indicator__(self) -> dict:
        result = {
            'F': 'Findable',
            'A': 'Accessible',
            'I': 'Interoperable',
            'R': 'Reusable'
        }

        final_data = {
            'Findable': dict(),
            'Accessible': dict(),
            'Interoperable': dict(),
            'Reusable': dict()
        }

        for key, value in self.fair_maturity_model_data.items():
            aux = result[self.__pattern__.findall(key)[0]]

            if aux is None:
                raise Exception(f"Sorry, key is not expected: {key}")

            final_data[aux][key] = value

        return final_data

    def classification_data_maximum_minimum(self):
        for x in list(self.FMMClassification_data.keys()):
            self.FMMClassification_data_minimum[x] = dict()
            self.FMMClassification_data_maximum[x] = dict()
            self.FMMClassification_data_sum[x] = dict()
            self.FMMClassification_data_len[x] = dict()

            aux = self.FMMClassification_data[x]

            self.FMMClassification_data_minimum[x] = \
                {y: min(aux[y].values()) if len(aux[y].values()) != 0 else None for y in aux.keys()}

            self.FMMClassification_data_maximum[x] = \
                {y: max(aux[y].values()) if len(aux[y].values()) != 0 else None for y in aux.keys()}

            self.FMMClassification_data_sum[x] = \
                {y: sum(aux[y].values()) if len(aux[y].values()) != 0 else None for y in aux.keys()}

            self.FMMClassification_data_len[x] = \
                {y: len(aux[y]) if len(aux[y].values()) != 0 else None for y in aux.keys()}

    def classification_data_normalized(self):
        """
        Normalize the data of a list in the range [a, b], where 'a' is 0 and 'b' is 1 | 2
        :return:
        """
        a = 0.0
        b_values = {
            'Essential': 1.0,
            'Important': 2.0,
            'Useful': 2.0
        }
        min_ajk = 1.0
        max_ajk = 5.0

        for i in list(self.FMMClassification_data.keys()):
            self.FMMClassification_data_normalized[i] = dict()

            b = b_values[i]
            n = self.FMMClassification_data_len[i]
            ajk = self.FMMClassification_data_sum[i]

            for j in list(n.keys()):
                if n[j] is not None:
                    aux = ajk[j] - n[j] * min_ajk
                    aux = aux / (n[j] * (max_ajk - min_ajk))
                    aux = a + aux * (b - a)
                    self.FMMClassification_data_normalized[i][j] = aux
                else:
                    self.FMMClassification_data_normalized[i][j] = None

    def classification_data_threshold(self):
        threshold = {
            'Essential': 1.0,
            'Important': 2.0,
            'Useful': 2.0
        }

        for i in list(self.FMMClassification_data_normalized.keys()):
            self.FMMClassification_data_threshold[i] = dict()

            for j in list(self.FMMClassification_data_normalized[i].keys()):
                self.FMMClassification_data_threshold[i][j] = (
                    1 if self.FMMClassification_data_normalized[i][j] == threshold[i] else 0)

    def classification_data_compliance_level(self):
        threshold = {
            'Essential': 1.0,
            'Important': 2.0,
            'Useful': 2.0
        }

        keys = list(list(self.fairness_classification_per_indicator.keys()))

        n = self.FMMClassification_data_normalized
        h = self.FMMClassification_data_threshold

        aux = {k: n['Essential'][k] for k in keys}

        for i in keys:
            # In case that the FAIR principle has no indicators we fix the value of the normalized to the
            # maximum value --> ['Essential': 1, 'Important': 2, 'Useful': 2]
            if n['Important'][i] is None:
                n_value_important = threshold['Important']
            else:
                n_value_important = n['Important'][i]

            if n['Useful'][i] is None:
                n_value_useful = threshold['Useful']
            else:
                n_value_useful = n['Useful'][i]

            if aux[i] is None:
                n_value_essential = threshold['Essential']
            else:
                n_value_essential = aux[i]

            aux[i] = (n_value_essential +
                      h['Essential'][i] * n_value_important +
                      h['Essential'][i] * h['Important'][i] * n_value_useful)

        self.FMMClassification_data_compliance_level = aux


if __name__ == '__main__':
    d = Data()
    print(d.FMMClassification_data)
