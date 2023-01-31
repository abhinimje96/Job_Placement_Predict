import numpy as np
import pickle as pkl
import json
import config

class JobPlacement():
    def __init__(self, gender, ssc_percentage, ssc_board, hsc_percentage, hsc_board, hsc_subject, degree_percentage, undergrad_degree,
       work_experience, emp_test_percentage, specialisation, mba_percent ):
       self.gender= gender
       self.ssc_percentage= ssc_percentage
       self.ssc_board= ssc_board
       self.hsc_percentage= hsc_percentage
       self.hsc_board= hsc_board
       self.hsc_subject= hsc_subject
       self.degree_percentage= degree_percentage
       self.undergrad_degree= undergrad_degree
       self.work_experience= work_experience
       self.emp_test_percentage= emp_test_percentage
       self.specialisation= specialisation
       self.mba_percent= mba_percent

    def __load_model(self):
        with open(config.MODEL_PATH, 'rb') as f:
            self.model = pkl.load(f)

        with open(config.JSON_PATH, 'r') as f:
            self.project_data = json.load(f)
            print(self.project_data)

    def get_placement_result(self):
        self.__load_model()

        test_array = np.zeros(self.model.n_features_in_)
        test_array[0] = self.project_data['Gender'][self.gender]
        test_array[1] = self.ssc_percentage
        test_array[2] = self.project_data['Ssc_board'][self.ssc_board]
        test_array[3] = self.hsc_percentage
        test_array[4] = self.project_data['Hsc_board'][self.hsc_board]
        hsc_subject = 'hsc_subject_' + self.hsc_subject
        index_hsc = self.project_data['Column Name'].index(hsc_subject)
        test_array[index_hsc] = 1
        test_array[5] = self.degree_percentage
        test_array[6] = self.project_data['Work_experience'][self.work_experience]
        test_array[7] = self.emp_test_percentage
        test_array[8] = self.mba_percent
        undergrad_degree = 'undergrad_degree_' + self.undergrad_degree
        index_ug = self.project_data['Column Name'].index(undergrad_degree)
        test_array[index_ug] = 1 
        specialisation = 'specialisation_' + self.specialisation
        index_spe = self.project_data['Column Name'].index(specialisation)
        test_array[index_spe] = 1 

        result = self.model.predict([test_array])[0]
        result_dict = {1:"Placed", 0: "Not Placed"}
        predict_placement_result = result_dict[result]

        return predict_placement_result